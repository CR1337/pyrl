from threading import Lock
import subprocess
import string
from smbus2 import SMBus
from functools import wraps
from itertools import product

from ..util.exceptions import RLException


class BusError(RLException):
    pass


class WriteError(RLException):
    def __init__(self, bus_address, chip_address, register_address, value):
        self.bus_address = bus_address
        self.chip_address = chip_address
        self.register_address = register_address
        self.value = value


class ReadError(RLException):
    def __init__(self, bus_address, chip_address, register_address):
        self.bus_address = bus_address
        self.chip_address = chip_address
        self.register_address = register_address


def lock_bus(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        FuseController.LOCK.acquire(blocking=True)
        result = func(*args, **kwargs)
        FuseController.LOCK.release()
        return result
    return wrapper


class FuseController():
    # TODO: logging

    LOCK = Lock()
    I2C_BUS = 1

    LOCK_REGISTER_ADDRESS = 0x00
    FUSE_REGISTER_ADDRESSES = [0x14, 0x15, 0x16, 0x17]
    ERROR_REGISTER_ADDRESSES = [0x1d, 0x1e]

    LOCK_MASK = 0x10
    UNLOCK_MASK = 0x00
    REVERSE_LOCK_MASK = 0xff - LOCK_MASK
    REVERSE_UNLOCK_MASK = 0xff - UNLOCK_MASK

    try:
        BUS = SMBus(I2C_BUS)
    except OSError:
        raise BusError()

    @classmethod
    @lock_bus
    def _read_chip_addresses(cls):
        address_dump = str(
            subprocess.subprocess.check_output(
                f"/usr/sbin/i2cdetect -y {cls.I2C_BUS}",
                shell=True
            ),
            encoding='utf-8'
        )
        row_0x60 = [
            row for row in address_dump.split("\n")
            if row.startswith("60:")
        ][0]
        row_entries = [
            entry for entry in row_0x60.split(" ")[1:]
            if all(c in string.hexdigits for c in entry) and len(entry) > 0
        ]
        addresses = [
            int(address, 16) for address
            in row_entries
            if 0x60 <= int(address, 16) <= 0x6f
                and int(address, 16) not in [0x68, 0x6b]
        ]
        return {
            letter: address
            for letter, address in zip(
                string.ascii_lowercase,
                sorted(addresses)
            )
        }

    CHIP_ADDRESSES = _read_chip_addresses()
    FUSE_STATES = {
        letter: [
            'idle'
            for _ in range(16)
        ]
        for letter in CHIP_ADDRESSES.keys()
    }

    @classmethod
    def set_fuse_state(cls, address, value):
        cls.FUSE_STATES[address.letter][address.number] = value

    @classmethod
    def reset_fuse_states(cls):
        for letter in cls.FUSE_STATES.keys():
            for number in range(16):
                cls.FUSE_STATES[letter][number] = 'idle'

    @classmethod
    def _get_chip_address(cls, address):
        return cls.CHIP_ADDRESSES[address.letter]

    @classmethod
    def _get_fuse_register_address(cls, address):
        return cls.FUSE_REGISTER_ADDRESSES[address.number // 4]

    @classmethod
    def _get_fuse_register_mask(cls, address):
        mask = 0x00
        for i in range(address.range):
            mask += 1 << (((address.number + i) % 4) * 2)
        return mask

    @classmethod
    def _get_reverse_fuse_register_mask(cls, fuse_register_mask):
        return 0xff - fuse_register_mask

    @classmethod
    def _write(cls, chip_address, register_address, value):
        try:
            cls.BUS.write_byte_data(chip_address, register_address, value)
        except OSError:
            raise WriteError(
                cls.I2C_BUS,
                chip_address,
                register_address,
                value
            )

    @classmethod
    def _read(cls, chip_address, register_address):
        try:
            value = cls.BUS.read_byte_data(chip_address, register_address)
            return value
        except OSError:
            raise ReadError(
                cls.I2C_BUS,
                chip_address,
                register_address
            )

    @classmethod
    @lock_bus
    def light(cls, address):
        value = cls._read(
            cls._get_chip_address(address),
            cls._get_fuse_register_address(address)
        )
        fuse_register_mask = cls._get_fuse_register_address(address)
        value &= cls._get_reverse_fuse_register_mask(fuse_register_mask)
        value |= fuse_register_mask
        cls._write(
            cls._get_chip_address(address),
            cls._get_fuse_register_address(address),
            value
        )

    @classmethod
    @lock_bus
    def unlight(cls, address):
        value = cls._read(
            cls._get_chip_address(address),
            cls._get_fuse_register_address(address)
        )
        fuse_register_mask = cls._get_fuse_register_address(address)
        value &= cls._get_reverse_fuse_register_mask(fuse_register_mask)
        cls._write(
            cls._get_chip_address(address),
            cls._get_fuse_register_address(address),
            value
        )

    @classmethod
    @lock_bus
    def lock(cls):
        for chip_address in cls.CHIP_ADDRESSES.values():
            cls._write(
                chip_address,
                cls.LOCK_REGISTER_ADDRESS,
                cls.LOCK_MASK
            )

    @classmethod
    @lock_bus
    def unlock(cls):
        for chip_address in cls.CHIP_ADDRESSES.values():
            cls._write(
                chip_address,
                cls.LOCK_REGISTER_ADDRESS,
                cls.UNLOCK_MASK
            )

    @classmethod
    @lock_bus
    def get_errors(cls):
        return {
            letter: [
                False if (value & mask) == 0 else True
                for value, mask in product(
                    [
                        cls._read(chip_address, register_address)
                        for register_address in cls.ERROR_REGISTER_ADDRESSES
                    ],
                    range(8)
                )
            ]
            for letter, chip_address in cls.CHIP_ADDRESSES.items()
        }

    @classmethod
    def get_status(cls):
        return {
            'fuse_states': cls.FUSE_STATES,
            'fuse_errors': cls.get_errors()
        }

    @classmethod
    def is_locked(cls):
        for chip_address in cls.CHIP_ADDRESSES.values():
            value = cls._read(chip_address, cls.LOCK_REGISTER_ADDRESS)
            value &= cls.LOCK_MASK
            if value > 0:
                return True
        return False
