

class SystemController():

    _connected_master = None

    @classmethod
    def set_system_time(cls, system_time):
        ...

    @classmethod
    def register_master(cls):
        ...

    @classmethod
    def deregister_master(cls):
        ...

    @classmethod
    def get_status(cls):
        return None
