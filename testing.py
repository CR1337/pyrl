import logging

logging.basicConfig(
    filename="testlog.log",
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

d = {
    'test': None
}

logging.debug("debug message")
logging.info("info message")
logging.warning("warning message")
logging.error("error message")
try:
    print(d['not_existing'])
except Exception:
    logging.exception("exception message")
logging.critical("critical message")
