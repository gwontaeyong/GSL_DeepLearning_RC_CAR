import io
import struct
from PIL import Image
import cv2 as cv
import numpy as np
import socket

from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication

class Runnable(QThread):
    predicSteering = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.cv_image
    def run(self):
        count = 0
        app = QCoreApplication.instance()
        self.predicSteering.emit(self.cv_image)
        app.quit()