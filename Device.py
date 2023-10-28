from abc import ABC, abstractmethod
import numpy as np
from PySide6.QtCore import Signal, QThread
from time import sleep
import debugpy
class DataException(Exception):
    pass


class ConnectException(Exception):
    pass

class Device(QThread):
    # define Python user-defined exceptions

    connected = Signal()
    disconnected = Signal()
    connectionOK = False
    dataOK = False
    do_exit = False

    @abstractmethod
    def conn(self):
        pass
    @abstractmethod
    def disconnect(self):
        pass
    @abstractmethod
    def after_connect(self):
        pass
    @abstractmethod
    def after_disconnect(self):
        pass
    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def connection_error(self):
        pass

    @abstractmethod
    def data_error(self):
        pass

    def run(self):
        #debugpy.debug_this_thread()
        while(True):
            #print('cycle')
            tmp = self.connectionOK
            if self.connectionOK is True:
                try:
                    self.action()
                except DataException:
                    self.data_error()
                except ConnectException:
                    self.connection_error()
                    self.connectionOK = False
            else:
                try:
                    self.conn()
                    self.connectionOK = True
                    print("Connection Ok!")
                    self.after_connect()
                    self.connected.emit()
                except ConnectException:
                    self.connection_error()
                    self.connectionOK = False
            if tmp is True and self.connectionOK is False:
                self.disconnected.emit()
            if self.do_exit:
                self.disconnect()
                break
            sleep(self.t)

    def __init__(self,t):
        self.t = t
        QThread.__init__(self)
