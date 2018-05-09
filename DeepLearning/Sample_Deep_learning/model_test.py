'''
학습이 완료된 데이터를 불러와서 테스트 하기 위한 용도
Sample_deep_learning_model2.py 파일에서 학습 관련 코드만 제거함
'''
import cv2 as cv
import numpy as np
import tensorflow as tf
import os

def im_trim(img):  # 함수로 만든다
    img_trim = img[100:240, 0:320]  # trim한 결과를 img_trim에 담는다
    return img_trim  # 필요에 따라 결과물을 리턴

# X데이터와 Y데이터를 담을 placeholder
X = tf.placeholder(tf.float32, shape=[None, 140, 320, 1])
Y_Lable = tf.placeholder(tf.float32, [None, 6])

X_data = []
# Y data
Y_data = [[1, 0, 0, 0, 0, 0],
          [1, 0, 0, 0, 0, 0],
          [1, 0, 0, 0, 0, 0],
          [0, 1, 0, 0, 0, 0],
          [0, 1, 0, 0, 0, 0],
          [0, 1, 0, 0, 0, 0],
          [0, 0, 1, 0, 0, 0],
          [0, 0, 1, 0, 0, 0],
          [0, 0, 1, 0, 0, 0],
          [0, 0, 0, 1, 0, 0],
          [0, 0, 0, 1, 0, 0],
          [0, 0, 0, 1, 0, 0],
          [0, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 0, 1],
          [0, 0, 0, 0, 0, 1],
          ]

# 이미지를 읽어 데이터를 담을 X_data 배열

# make image data set
# left, right , straight
# image size = 240*320
# image_data's Shape = [240, 320]

'''
이미지를 읽어 shape를 변형하고 이를 X_data배열에 넣는다.

left, right, straight 데이터를 넣는다.

'''
images_path = 'images'

folder_path =['5.0','5.5','6.0','6.5','7.0']
''''''
for i in folder_path:
    full_filename = os.path.join(images_path, i)
    print(full_filename)
    for i in range(3):
        filename = str(i + 1) + '.jpg'
        test = os.path.join(full_filename,filename)
        print(test)
        # left 데이터
        image_data = cv.imread(test, cv.IMREAD_GRAYSCALE)  # read_Image
        print(image_data)
        image_data = im_trim(image_data)
        reshape_image_data = np.reshape(image_data, [140, 320, 1])
        X_data.append(reshape_image_data)

# left 데이터
image_data = cv.imread('images/7.5/1.jpg', cv.IMREAD_GRAYSCALE)  # read_Image
image_data = im_trim(image_data)
reshape_image_data = np.reshape(image_data, [140, 320, 1])
X_data.append(reshape_image_data)
# left 데이터
image_data = cv.imread('images/7.5/2.jpg', cv.IMREAD_GRAYSCALE)  # read_Image
image_data = im_trim(image_data)
reshape_image_data = np.reshape(image_data, [140, 320, 1])
X_data.append(reshape_image_data)

# 커널 생성 커널 사이즈는  4x4이고 총 4개의 커널
# 바이어스는 커널의 갯수만큼 4개를 생성한다.
kernel1 = tf.Variable(tf.truncated_normal(shape=[4, 4, 1, 4], stddev=0.1))
bias1 = tf.Variable(tf.truncated_normal(shape=[4], stddev=0.1))
conv1 = tf.nn.conv2d(X, kernel1, strides=[1, 1, 1, 1], padding='SAME') + bias1
activation1 = tf.nn.relu(conv1)
pool1 = tf.nn.max_pool(activation1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# Flat 한 데이터 형식으로 바꾸기
w1 = tf.Variable(tf.truncated_normal(shape=[70 * 160 * 4, 6]))
b1 = tf.Variable(tf.truncated_normal(shape=[6]))
pool_flat = tf.reshape(pool1, [-1, 70 * 160 * 4])
outputLayer = tf.matmul(pool_flat, w1) + b1

# 최적화
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y_Lable, logits=outputLayer))
train_step = tf.train.AdamOptimizer(0.005).minimize(loss)

# 저장에 관련된 saver
# Saver()의 인자로 변수 리스트를 주면 해당 변수만 저장
# 인자를 안주면 saver 생성 시점까지 초기화 된 변수만 저장(이 코드 위의 변수들)
# 최적화 코드 위에 적었더니 에러가 발생했음
saver = tf.train.Saver()

# 정확도 기록
correct_prediction = tf.equal(tf.argmax(outputLayer, 1), tf.argmax(Y_Lable, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    print("start")

    # 저장된 학습 데이터 불러오기
    # restore(세션, 파일경로)
    # initializer를 주석처리한다. -> restore실행시 ckpt에 저장된 값으로 변수들을 초기화 시켜주기 때문에

    #sess.run(tf.global_variables_initializer())

    load_path = 'saved/ckpt_test-39300'
    saver.restore(sess, load_path)


    pred = sess.run(tf.argmax(outputLayer, 1), feed_dict={X: X_data})
    print(pred)