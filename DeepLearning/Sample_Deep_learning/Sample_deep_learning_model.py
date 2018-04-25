import tensorflow as tf
import cv2 as cv
import numpy as np

'''
이미지 크기는 240 x 320 이다.
이를 3장 입력하고
각각의 이미지를 240 x 320 x 1 로 크기를 변경하여
3(3장을 의미) x 240 x 320 x 1 크기의 X데이터로 만든다.

Convolution : 240 x 320 x 1크기의 이미지를 4개의 층으로 생성한다.
->
4 x 4 사이즈의 커널을 4개 만든다.
240 x 320 x 4 크기 층을 만든다.

Pooling : 2 x 2 커널을 사용하여 120 x 160 x 4 크기로 MaxPooling 한다.
-> 2 x 2 크기의 커널을 생성하고 Stride 를 2로 두어 MaxPooling 한다.

Plat : Pooling한 데이터를 [120 * 160 * 4, 3] 크기로  일차원화 한다.
-> [120 * 160 * 4, 3] 크기의 Weight 배열을 만든다.
-> [3]크기의 bias를 만든다.
-> Pool 링한 데이터 를 [-1, 120 * 160 * 4] 크기로 변경한다. = Flat
-> Flat x Weight + bias 를 통하여 [-1, 3] 크기로 만든다.  
-> -1 은 데이터의 입력 된수가 X_data숫자를 동적으로 설정하기 위해서 지정한것이다.
-> 여기서는 3이 된다. (X_data를 3개 입력하였기 때문에)

[?, ?, ?] 크기로 생성된 데이터를 One_hot 을 통하여 큰 숫자 하나를 선택한다.
'''

#X데이터와 Y데이터를 담을 placeholder
X = tf.placeholder(tf.float32, shape=[None, 240, 320, 1])
Y_Lable = tf.placeholder(tf.float32, [None,3])

#Y data
Y_data = [[1,0,0],
          [0,0,1],
          [0,1,0]]

#이미지를 읽어 데이터를 담을 X_data 배열
X_data = []

#make image data set
#left, right , straight
#image size = 240*320
#image_data's Shape = [240, 320]

'''
이미지를 읽어 shape를 변형하고 이를 X_data배열에 넣는다.

left, right, straight 데이터를 넣는다.

'''

#left 데이터
image_data = cv.imread('left.jpg',cv.IMREAD_GRAYSCALE) #read_Image
reshape_image_data = np.reshape(image_data, [240,320,1])
X_data.append(reshape_image_data)

#right 데이터
image_data = cv.imread('right.jpg',cv.IMREAD_GRAYSCALE) #read_Image
reshape_image_data = np.reshape(image_data, [240,320,1])
X_data.append(reshape_image_data)

#straight 데이터
image_data = cv.imread('straight.jpg',cv.IMREAD_GRAYSCALE) #read_Image
reshape_image_data = np.reshape(image_data, [240,320,1])
X_data.append(reshape_image_data)

#커널 생성 커널 사이즈는  4x4이고 총 4개의 커널
#바이어스는 커널의 갯수만큼 4개를 생성한다.
kernel1 = tf.Variable(tf.truncated_normal(shape=[4,4,1,4], stddev=0.1))
bias1 = tf.Variable(tf.truncated_normal(shape = [4], stddev= 0.1))
conv1 = tf.nn.conv2d(X, kernel1, strides=[1,1,1,1], padding='SAME') + bias1
activation1 = tf.nn.relu(conv1)
pool1 = tf.nn.max_pool(activation1, ksize=[1,2,2,1], strides = [1,2,2,1], padding = 'SAME')

#Flat 한 데이터 형식으로 바꾸기
w1 = tf.Variable(tf.truncated_normal(shape=[120*160*4, 3]))
b1 = tf.Variable(tf.truncated_normal(shape=[3]))
pool_flat = tf.reshape(pool1, [-1,120*160*4])
outputLayer = tf.matmul(pool_flat, w1) + b1

#최적화
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y_Lable, logits=outputLayer))
train_step = tf.train.AdamOptimizer(0.005).minimize(loss)

#정확도 기록
correct_prediction = tf.equal(tf.argmax(outputLayer, 1), tf.argmax(Y_Lable, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


with tf.Session() as sess:
    print("start")
    sess.run(tf.global_variables_initializer())
    for i in range(1000):
        sess.run(train_step, feed_dict={X:X_data, Y_Lable: Y_data})

        if i%100 == 0:
            print(sess.run(accuracy, feed_dict={X:X_data, Y_Lable: Y_data}))

    pred = sess.run(tf.argmax(outputLayer, 1), feed_dict={X:X_data})
    print(pred)
