import numpy as np
import cv2 as cv
import threading

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import pyqtSlot


class DataControl(QThread):

    change_predict_speed_label = pyqtSignal(int, str)
    change_predict_steering_label = pyqtSignal(int, str)
    send_cmd_ras = pyqtSignal(str)

    def __init__(self, model = False):
        super().__init__()
        self.flag = False
        self.model = model
        self.lock = threading.Lock()

    def run(self):
        while True:
            if self.flag:
                self.lock.acquire()
                print("result : ", self.predict_steering(self.image))
                self.lock.release()

    def predict_steering(self, image):
        x_data = self.make_x_data(image)

        try:
            result = self.model.predict(x_data)
            cmd = str(result[0])+"_0"
            print(cmd)
            self.change_predict_steering_label.emit(result[0], "red")
            self.send_cmd_ras.emit(cmd)


        except Exception as e:
            print(e)
            pass

        return result

    def make_x_data(self, image):
        img = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        img = img[100:240, 0:320]
        img = np.reshape(img, [-1])
        return [img]

    @pyqtSlot(np.ndarray)
    def put_image(self, image):
        self.flag = True
        self.image = image


