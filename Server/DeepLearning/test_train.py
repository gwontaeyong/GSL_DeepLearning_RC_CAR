from DeepLearning.ndivia_model import *
from DeepLearning.InputData import *

import tensorflow as tf
import cv2 as cv
import numpy as np

inputData = InputData("output.csv")

save_path = 'saved/sample4_1'
load_path = 'saved/sample4_1-2000'

sess = tf.Session()

# 저장된 학습 데이터 불러오기
#  restore(세션, 파일경로)
# initializer를 주석처리한다. -> restore실행시 ckpt에 저장된 값으로 변수들을 초기화 시켜주기 때문에
# m1.saver.restore(sess, load_path)
# s = int(load_path.split("-")[1])

m1 = Model(sess, "m1")

sess.run(tf.global_variables_initializer())
s = 0

print('Learning Started!')

coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)


for step in range(s + 1, s + 2001):

    img_addr, steering, speed = sess.run([inputData.batch_addr, inputData.batch_steering, inputData.batch_speed])
    x_data = inputData.make_x_data(img_addr)
    summary, _ = m1.train(x_data, steering)
    m1.writer.add_summary(summary, global_step=step)

    if step % 100 == 0:
        print("Accuracy : ", m1.get_accuracy(x_data, steering))
        # 학습 데이터 저장하기
        # saver.save(세션, 파일명, 스텝(생략가능))
        # ex) saved/ckpt_test-스텝 파일 생성
        m1.saver.save(sess, save_path, global_step=step)

coord.request_stop()
coord.join(threads)
print('stop batch')

print('Learning Finished!')
print("Predict : ", m1.predict(x_data))
