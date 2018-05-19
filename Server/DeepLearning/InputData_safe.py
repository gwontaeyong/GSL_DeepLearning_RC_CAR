import numpy as np
import cv2 as cv
import tensorflow as tf
import sys

class InputData():

    def __init__(self, csv_file_name, sess):
        self.X_data = []
        self.Y_data = None

    def read_csv_file(self, file_name):
        xy = np.loadtxt(file_name, delimiter=',', dtype=str)
        x_address_data = xy[:, [0]]
        self.Y_data = xy[:, [1]]
        x_address_data = np.reshape(x_address_data, [-1])
        self.make_x_data(x_address_data)
        self.make_y_data(self.Y_data)

    def im_trim(self, img):  # 함수로 만든다
        img_trim = img[100:240, 0:320]  # trim한 결과를 img_trim에 담는다
        return img_trim  # 필요에 따라 결과물을 리턴

    def make_x_data(self, x_address):
        for address in x_address:
            image_data = cv.imread(address, cv.IMREAD_GRAYSCALE)  # read_Image
            image_data = self.im_trim(image_data)
            self.X_data.append(np.reshape(image_data, [-1]))

    def make_y_data(self, y_csv_data):
        tf.cast(y_csv_data, tf.int32)
        self.Y_data = y_csv_data.astype(np.int32)
