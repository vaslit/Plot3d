from PySide6.QtWidgets import QApplication
from Device import Device, ConnectException, DataException
from PySide6.QtCore import Signal
import serial
import time
from struct import unpack
from PySide6.QtCore import Qt
import numpy as np
import math
from tof import utils
class TOFCam(Device):

    dataUpdated = Signal(np.ndarray)

    def __init__(self, port, baudrate, k, fps, w, h, fov_h, fov_v):
        Device.__init__(self, t=0.1)
        self.w = w
        self.h = h
        self.fov_h = fov_h
        self.fov_v = fov_v
        self.k = k
        self.fps = fps
        self.port = port
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.one_byte_time = 0
        self.buffer = b''
        self.t = 0
        self.last_frame_id = 0
        self._raw_data = b''
        self.header_bytes = b'\x00\xff'
        self.points = np.zeros((w*h, 3), dtype=float)
        self.points3d = np.zeros((w*h, 3), dtype=float)

    def conn(self):
        #print('Try connect to PLC')
        try:
            self.ser.open()
            if not self.ser.is_open:
                raise ConnectException
            else:
                self.sendCmd("AT+DISP=3\r")
                time.sleep(0.1)
                self.sendCmd("AT+UNIT={}\r".format(self.k))
                time.sleep(0.1)
                self.sendCmd(f"AT+FPS={self.fps}\r")
                self.ser.flushInput()
                self.ser.flushOutput()
                self.ser.timeout = 0.001
                self.one_byte_time = 1 / (self.ser.baudrate / self.ser.bytesize + 2 + self.ser.stopbits)
        except Exception:
            raise ConnectException

    def disconnect(self):
        try:
            if self.ser.is_open:
                self.ser.close()
        except Exception:
            self.connectionOK = False

    def after_connect(self):
        pass

    def after_disconnect(self):
        pass

    def action(self):
        try:
            self.read_data()
        except Exception as e:
            print(e)
            raise DataException

        #self.dataUpdated.emit()

    def connection_error(self):
        print('connection error')

    def data_error(self):
        print('Data read error')
        self.connectionOK = False

    def read_data(self):
        length = max(1, self.ser.in_waiting)
        data = self.ser.read(length)
        t = 0
        if data:
            t = time.time()
            if length == 1 and not self.buffer:
                self.buffer += data
                return
            self.buffer += data
        if self.buffer and (time.time() - t > self.one_byte_time * 2):
            try:
                self.on_recv(self.buffer)
            except Exception as e:
                print(e)
                raise DataException
            self.buffer = b''

    def on_recv(self, data):
        return self.decodeData(data)

    def decodeData(self, data: bytes):
        '''
            @data bytes, protocol:
                         |    header(2B)    | len(2B) | command(1B) | output_mode(1B)     | sensor temp(1B) | driver temp(1B) |
                         |     0xCC  0xA0      |  >=18   |             | 0:Depth only, 1:+IR |    uint8        | uint8           |
                         -------------------------------------------------------------------------------------------------------
                         |    exposure time(4B)    | errcode(1B) | reserved1(1B) | res_rows(1B) | res_cols(1B) |
                         |[23:20][19:12][11:8][7:0]|             |       0x0     |     uint8    |     uint8    |
                         ---------------------------------------------------------------------------------------
                         |    Frame ID(2B)    | ISP ver(1B) | reserved3(1B) | frame data((len-16)B) | checksum(1B) | tail(1B) |
                         |     [11:0]         |     0x23    |       0x0     | xxxxxxxxxxxxxxxxxxxxx | sum of above |   0xDD   |

            @return haveFrame, dict {
                "frameID": {
                    "res": tunple(w, h)
                    "frameData": []
                }
            }
        '''
        # append data
        self._raw_data += data
        # find header
        header = self.header_bytes
        idx = self._raw_data.find(header)
        if idx < 0:
            return False
        self._raw_data = self._raw_data[idx:]
        # print(raw_data)
        # check data length 2Byte
        dataLen = unpack("H", self._raw_data[2: 4])[0]
        # print("len: "+str(dataLen))
        frameLen = len(header) + 2 + dataLen + 2
        frameDataLen = dataLen - 16

        if len(self._raw_data) < frameLen:
            return False
        # get data
        frame = self._raw_data[:frameLen]
        # print(frame.hex())
        self._raw_data = self._raw_data[frameLen:]

        frameTail = frame[-1]
        # print("tail: "+str(hex(frameTail)))
        _sum = frame[-2]
        # print("checksum: "+str(hex(_sum)))
        # check sum
        # spi has no checksum but i add one
        if frameTail != 0xdd and _sum != sum(frame[:frameLen - 2]) % 256:
            return False

        frameID = unpack("H", frame[16:18])[0]
        # print("frame ID: "+str(frameID), "last frame ID: "+str(self.last_frame_id))
        if frameID == self.last_frame_id:
            # print("same frame ID")
            return True
        self.last_frame_id = frameID

        resR = unpack("B", frame[14:15])[0]
        resC = unpack("B", frame[15:16])[0]
        res = (resR, resC)
        frameData = np.frombuffer(frame[20:20+frameDataLen],dtype=np.uint8)#.reshape(shape=(100,100))
        #frameData = np.flip(frameData, 1)
        #frameData = np.flip(frameData, 1).reshape(shape=(10000,))
        inds = np.where(frameData<255)
        self.points = np.zeros((len(inds[0]), 3), dtype=np.uint32)
        self.points[:, 0] = 100-np.array(inds,dtype=np.uint32) // self.w
        self.points[:, 1] = 100-np.array(inds,dtype=np.uint32) % self.w
        self.points[:, 2] = frameData[inds].astype(np.uint32) * self.k
        # frameData = [unpack("B", frame[20 + i:21 + i])[0]
        #              for i in range(0, frameDataLen, 1)]
        #self.points[:, 2] = np.array(frameData, dtype=float)
        self.depth_to_pc()


        return True

    def depth_to_pc(self):
        self.points3d = np.zeros((self.points.shape[0],3), dtype=float)
        a_h = self.fov_h / 2
        a_v = self.fov_v / 2
        c_x = (self.w - 1) / 2
        c_y = (self.h - 1) / 2
        t_v = math.tan((np.pi * a_v / 180.0)) / c_x
        t_h = math.tan((np.pi * a_h / 180.0)) / c_y
        self.points3d[:, 2] = self.points[:, 2]
        self.points3d[:, 0] = self.points[:, 2] * (self.points[:, 0] - c_x) * t_h
        self.points3d[:, 1] = self.points[:, 2] * (self.points[:, 1] - c_y) * t_v
        self.dataUpdated.emit(self.points3d)
        print(f"emit frame data")
    # def write_data(self, DB_number, PLC_write_byte_index_start, array):
    #         self.client.write_area(snap7.types.Areas.DB, self.write_db, PLC_write_byte_index_start, array)
    def sendCmd(self, cmd):
        send_bytes = utils.str_to_bytes(cmd, escape=True, encoding="ASCII")
        # print(send_bytes)
        # print(len(send_bytes))
        # self.send(send_bytes)
        self.ser.write(send_bytes)

    def rotation_matrix(self, axis, theta):
        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(axis)
        axis = axis / math.sqrt(np.dot(axis, axis))
        a = math.cos(theta / 2.0)
        b, c, d = -axis * math.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    cam = TOFCam("COM3", 115200, 3, 15, 100, 100, 70, 60)
    cam.start()
    sys.exit(app.exec())


