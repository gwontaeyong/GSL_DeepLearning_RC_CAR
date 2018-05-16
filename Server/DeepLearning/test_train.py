from ndivia_model import *
import csv
import tensorflow as tf
import csv
import cv2 as cv
import numpy as np
import os


class InputData():
    def __init__(self, csv_file_name):
        self.X_data = []
        self.Y_data = None
        self.read_csv_file(csv_file_name)

    def read_csv_file(self, file_name):
        xy = np.loadtxt(file_name, delimiter=',', dtype=str)
        x_address_data = xy[:, [0]]
        y_csv_data = xy[:, [1]]
        x_address_data = np.reshape(x_address_data, [-1])
        self.make_x_data(x_address_data)
        self.make_y_data(y_csv_data)

    def im_trim(self, img):  # 함수로 만든다
        img_trim = img[100:240, 0:320]  # trim한 결과를 img_trim에 담는다
        return img_trim  # 필요에 따라 결과물을 리턴

    def make_x_data(self, x_address):
        for address in x_address:
            image_data = cv.imread(address, cv.IMREAD_GRAYSCALE)  # read_Image
            image_data = self.im_trim(image_data)
            reshape_image_data = np.reshape(image_data, [140, 320, 1])
            self.X_data.append(reshape_image_data)

    def make_y_data(self, y_csv_data):
        y_steering_data = []
        tf.cast(y_csv_data, tf.float32)
        self.Y_data = tf.reshape(tf.one_hot(y_csv_data, 9), [-1, 9])


input_data = InputData("output.csv")
sess = tf.Session()

print(input_data.X_data)
print(sess.run(input_data.Y_data))
print(np.shape(sess.run(input_data.Y_data)))
print(input_data.Y_data)

Y = tf.placeholder(tf.float32, shape=[None, 9])
print(Y)
save_path = 'saved/sample4_1'
load_path = 'saved/sample4_1-300'

'''
sess = tf.Session()


m1 = Model(sess, "m1")

# 저장된 학습 데이터 불러오기
#  restore(세션, 파일경로)
# initializer를 주석처리한다. -> restore실행시 ckpt에 저장된 값으로 변수들을 초기화 시켜주기 때문에
sess.run(tf.global_variables_initializer())
s = 0

# m1.saver.restore(sess, load_path)
# s = int(load_path.split("-",[1]))

print('Learning Started!')

for step in range(s + 1, s + 2001):

    summary, _ = m1.train(input_data.X_data, input_data.Y_data)
    m1.writer.add_summary(summary, global_step=step)

    if step % 100 == 0:
        print("Accuracy : ", m1.get_accuracy(input_data.X_data, input_data.Y_data))

        # 학습 데이터 저장하기
        # saver.save(세션, 파일명, 스텝(생략가능))
        # ex) saved/ckpt_test-스텝 파일 생성
        m1.saver.save(sess, save_path, global_step=step)

print('Learning Finished!')
print("Predict : ", m1.predict(input_data.X_data))
'''