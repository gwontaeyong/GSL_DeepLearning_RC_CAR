import numpy as np
import cv2 as cv
import tensorflow as tf
import sys

class InputData():

    def __init__(self, csv_file_name, batch_size = 100):
        self.batch_addr = None
        self.batch_steering = None
        self.batch_speed = None

        self.data_size = self.file_len(csv_file_name)
        self.batch_size = batch_size
        self.total_batch_size = self.data_size//self.batch_size
        self.read_data_batch(csv_file_name)

    def im_trim(self, img):  # 함수로 만든다
        img_trim = img[100:240, 0:320]  # trim한 결과를 img_trim에 담는다
        return img_trim  # 필요에 따라 결과물을 리턴

    def make_x_data(self, byte_x_address):
        X_data = []

        for address in byte_x_address:
            image_data = cv.imread(str(address, 'utf-8'), cv.IMREAD_GRAYSCALE)  # read_Image
            image_data = self.im_trim(image_data)
            X_data.append(np.reshape(image_data, [-1]))

        return X_data

    def read_data(self, file_name):
        try:
            csv_file = tf.train.string_input_producer([file_name], name='filename_queue')
            textReader = tf.TextLineReader()
            _, line = textReader.read(csv_file)
            addr, steering, speed = tf.decode_csv(line, record_defaults=[[""], [0], [0]], field_delim=',')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            exit()
        return addr, steering, speed

    def read_data_batch(self, file_name):

        addr, steering, speed = self.read_data(file_name)
        self.batch_addr, batch_steering, batch_speed = tf.train.batch([addr, steering, speed], batch_size=self.batch_size)
        self.batch_steering = tf.reshape(batch_steering, [-1, 1])
        self.batch_speed = tf.reshape(batch_speed, [-1, 1])

    def file_len(self, fname):

        with open(fname) as f:
            for i, l in enumerate(f):
                pass

            return i + 1