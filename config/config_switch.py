from abc import ABCMeta, abstractmethod
from access.switch_access import Switch_Access

class Config_Switch():
    __metaclass__ = ABCMeta

    def __init__(self, conn):
        if not isinstance(conn, Switch_Access):
            print ('wrong connection. parent of conn is %s'%conn.__class__.__bases__)
            return

        if not conn.is_login():
            conn.fail('Have not login yet')
            return

        self.conn = conn
        self.__ready = True
        self._enter_priv_mode()

    def is_ready(self):
        return self.__ready

    def _back_config_mode(self):
        self._back_priv_mode()
        self.conn.exec_command('configure\n')

    def _enter_priv_mode(self):
        self.conn.exec_command('enable\n')

    def _back_priv_mode(self):
        self.conn.exec_command('end\n', read_output=False)

    def reload_with_factory_config(self):
        self.factory_config()
        self.reload()

    def reload_with_saving_config(self):
        self.save_config()
        self.reload()

    @abstractmethod
    def factory_config(self):
        pass

    @abstractmethod
    def save_config(self):
        pass

    @abstractmethod
    def reload(self):
        pass

    @abstractmethod
    def config_mgmt(self, mgmt_ip, mask, gateway_ip):
        pass

    def exit(self):
        self._back_priv_mode()
        self.conn.exec_command('exit\n', read_output=False)

    def close(self):
        self.conn.close()

    def log(self, message=''):
        self.conn.log(message)

    def fail(self, message=''):
        self.conn.fail(message)
