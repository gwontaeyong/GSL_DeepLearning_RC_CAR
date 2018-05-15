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

# dropout을 지정할 placeholder
training = tf.placeholder(tf.bool)

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

folder_path = ['5.0', '5.5', '6.0', '6.5', '7.0']
''''''
for i in folder_path:
    full_filename = os.path.join(images_path, i)
    print(full_filename)
    for i in range(3):
        filename = str(i + 1) + '.jpg'
        test = os.path.join(full_filename, filename)
        print(test)
        # left 데이터
        image_data = cv.imread(test, cv.IMREAD_GRAYSCALE)  # read_Image
        print(image_data)
        image_data = im_trim(image_data)
        reshape_image_data = np.reshape(image_data, [140, 320, 1])
        X_data.append(reshape_image_data)

# straight 데이터
image_data = cv.imread('images/7.5/1.jpg', cv.IMREAD_GRAYSCALE)  # read_Image
image_data = im_trim(image_data)
reshape_image_data = np.reshape(image_data, [140, 320, 1])
X_data.append(reshape_image_data)

image_data = cv.imread('images/7.5/2.jpg', cv.IMREAD_GRAYSCALE)  # read_Image
image_data = im_trim(image_data)
reshape_image_data = np.reshape(image_data, [140, 320, 1])
X_data.append(reshape_image_data)


# Convolutional Layer #1
# 140 * 320 * 1 => 70 * 160 * 24
conv1 = tf.layers.conv2d(inputs=X, filters=24, kernel_size=[5, 5], padding="SAME", activation=tf.nn.relu)
pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], padding="SAME", strides=2)
dropout1 = tf.layers.dropout(inputs=pool1, rate=0.3, training=training)

# Convolutional Layer #2
# 70 * 160 * 24 => 35 * 80 * 36
conv2 = tf.layers.conv2d(inputs=dropout1, filters=36, kernel_size=[5, 5], padding="SAME", activation=tf.nn.relu)
pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], padding="SAME", strides=2)
dropout2 = tf.layers.dropout(inputs=pool2, rate=0.3, training=training)

# Convolutional Layer #3
# 35 * 80 * 36 => 18 * 40 * 48
conv3 = tf.layers.conv2d(inputs=dropout2, filters=48, kernel_size=[5, 5], padding="SAME", activation=tf.nn.relu)
pool3 = tf.layers.max_pooling2d(inputs=conv3, pool_size=[2, 2], padding="SAME", strides=2)
dropout3 = tf.layers.dropout(inputs=pool3, rate=0.3, training=training)

# Convolutional Layer #4
# 18 * 40 * 48 => 9 * 20 * 64
conv4 = tf.layers.conv2d(inputs=dropout3, filters=64, kernel_size=[3, 3], padding="SAME", activation=tf.nn.relu)
pool4 = tf.layers.max_pooling2d(inputs=conv4, pool_size=[2, 2], padding="SAME", strides=2)
dropout4 = tf.layers.dropout(inputs=pool4, rate=0.3, training=training)

# Convolutional Layer #5
# 9 * 20 * 64 => 5 * 10 * 64
conv5 = tf.layers.conv2d(inputs=dropout4, filters=64, kernel_size=[3, 3], padding="SAME", activation=tf.nn.relu)
pool5 = tf.layers.max_pooling2d(inputs=conv5, pool_size=[2, 2], padding="SAME", strides=2)
dropout5 = tf.layers.dropout(inputs=pool5, rate=0.3, training=training)

# Convolutional Layer #6
# 5 * 10 * 64 => 3 * 8 * 64
conv6 = tf.layers.conv2d(inputs=dropout5, filters=64, kernel_size=[3, 3], padding="VALID", activation=tf.nn.relu)
dropout6 = tf.layers.dropout(inputs=conv6, rate=0.3, training=training)

# FC Layer #1
# 3 * 8 * 64 = 1536 => 100
flat = tf.reshape(dropout6, [-1, 3 * 8 * 64 ])
dense7 = tf.layers.dense(inputs=flat, units=100, activation=tf.nn.relu)
dropout7 = tf.layers.dropout(inputs=dense7, rate=0.5, training=training)

# FC Layer #2
# 100 => 50
dense8 = tf.layers.dense(inputs=dropout7, units=50, activation=tf.nn.relu)
dropout8 = tf.layers.dropout(inputs=dense8, rate=0.5, training=training)

# FC Layer #3
# 50 => 10
dense9 = tf.layers.dense(inputs=dropout8, units=10, activation=tf.nn.relu)
dropout9 = tf.layers.dropout(inputs=dense9, rate=0.5, training=training)

# Y : 6가지
# 50 => 6
dense = tf.layers.dense(inputs=dropout9, units=6)

# 최적화
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=dense, labels=Y_Lable))
train_step = tf.train.AdamOptimizer(0.005).minimize(loss)

# loss summary
loss_summ = tf.summary.scalar("loss", loss)

# 저장에 관련된 saver
# Saver()의 인자로 변수 리스트를 주면 해당 변수만 저장
# 인자를 안주면 saver 생성 시점까지 초기화 된 변수만 저장(이 코드 위의 변수들)
# 최적화 코드 위에 적었더니 에러가 발생했음
saver = tf.train.Saver()

# 정확도 기록
correct_prediction = tf.equal(tf.argmax(dense, 1), tf.argmax(Y_Lable, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# accuracy summary
accuracy_summ = tf.summary.scalar("accuracy", accuracy)

with tf.Session() as sess:
    print("start")

    # 텐서보드
    # summary들을 merge 하고 파일 경로를 지정해준다
    # 세션의 그래프를 추가한다
    # 커맨드창에서 실행 : tensorboard --logdir=파일경로
    # => 파일경로를 C드라이브 부터 주던지 or cmd에서 디렉토리 이동 후 logs_path의 경로를 주던지
    # 그 후 커맨드창에 나타난 url을 인터넷으로 접속 (http://127.0.0.1:6006)
    logs_path = "./logs/sample3-7"
    merged_summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter(logs_path)
    writer.add_graph(sess.graph)

    # 저장된 학습 데이터 불러오기
    # restore(세션, 파일경로)
    # initializer를 주석처리한다. -> restore실행시 ckpt에 저장된 값으로 변수들을 초기화 시켜주기 때문에

    sess.run(tf.global_variables_initializer())
    s = 0
    # load_path = 'saved/ckpt_test-71400'
    # saver.restore(sess, load_path)
    # s = int(load_path[16:21])

    for step in range(s + 1, s + 1501):

        # 텐서보드
        # 원래코드 : sess.run(train_step, feed_dict={X: X_data, Y_Lable: Y_data})
        # summary도 텐서플로우이기 때문에 run 해야해서 추가
        # 마지막으로 add_summary(summary, x축)를 해준다
        summary, _ = sess.run([merged_summary, train_step], feed_dict={X: X_data, Y_Lable: Y_data, training:True})
        writer.add_summary(summary, global_step=step)

        if step % 100 == 0:
            # 학습 데이터 저장하기
            # saver.save(세션, 파일명, 스텝(생략가능))
            # ex) saved/ckpt_test-스텝 파일 생성
            save_path = 'saved/sample3-7'
            saver.save(sess, save_path, global_step=step)

            print(sess.run(accuracy, feed_dict={X: X_data, Y_Lable: Y_data, training:False}))


    pred = sess.run(tf.argmax(dense, 1), feed_dict={X: X_data, training: False})
    print(pred)