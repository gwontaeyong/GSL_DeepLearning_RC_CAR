import socket
import numpy as np
import cv2 as cv
import tensorflow as tf

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import pyqtSlot

from DeepLearning.ndivia_model import *

class CmdServer(QThread):
    change_rc_speed_label = pyqtSignal(int, str)
    change_rc_steering_label = pyqtSignal(int, str)
    change_predict_speed_label = pyqtSignal(int, str)
    change_predict_steering_label = pyqtSignal(int, str)

    def __init__(self, host, port, model):
        super().__init__()

        self.cmd_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)
        self.buf_size = 3
        self.flag = True
        self.cmd_server.bind(server_address)
        self.cmd_server.listen(1)
        self.ex_steering = 4
        self.ex_speed = 0
        self.model = model



    def run(self):
        print("waiting cmd_client")
        self.conn, addr = self.cmd_server.accept()
        print("start cmd_server")
        print("connect with %s" % self.conn)
        self.recv_cmd()

    @pyqtSlot(np.ndarray)
    def send_cmd(self, image):
        x_data = self.make_x_data(image)
        try:
            result = self.model.predict(x_data)
            print(result[0])
            self.change_predict_steering_label.emit(result[0], "red")
            #self.conn.send(str(result[0]).encode())
        except Exception as e:
            print(e)



    def recv_cmd(self):
        while self.flag:
            reply = self.conn.recv(self.buf_size)
            if not reply:
                break
            else:
                data = str(reply.decode()).split("_")
                steering_index = int(data[0])
                speed_index = int(data[1])
                self.change_rc_steering_label.emit(steering_index, "green")
                self.change_rc_speed_label.emit(speed_index, "green")

    def make_x_data(self, image):

        result = []
        img = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        img = img[100:240, 0:320]
        img = np.reshape(img, [-1])
        result.append(img)

        return result

    def __del__(self):
        print("cmd_server is close")
        self.wait()
