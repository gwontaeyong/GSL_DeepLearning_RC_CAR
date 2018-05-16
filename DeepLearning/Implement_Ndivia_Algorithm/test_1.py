import cv2 as cv
import numpy as np
import tensorflow as tf
import os

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

# loss summary
loss_summ = tf.summary.scalar("loss", loss)

# 저장에 관련된 saver
# Saver()의 인자로 변수 리스트를 주면 해당 변수만 저장
# 인자를 안주면 saver 생성 시점까지 초기화 된 변수만 저장(이 코드 위의 변수들)
# 최적화 코드 위에 적었더니 에러가 발생했음
saver = tf.train.Saver()

# 정확도 기록
correct_prediction = tf.equal(tf.argmax(outputLayer, 1), tf.argmax(Y_Lable, 1))
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
    logs_path = "./logs/tb_test5"
    merged_summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter(logs_path)
    writer.add_graph(sess.graph)

    # 저장된 학습 데이터 불러오기
    # restore(세션, 파일경로)
    # initializer를 주석처리한다. -> restore실행시 ckpt에 저장된 값으로 변수들을 초기화 시켜주기 때문에

    sess.run(tf.global_variables_initializer())
    s = 0
    #load_path = 'saved/ckpt_test-71400'
    #saver.restore(sess, load_path)
    #s = int(load_path[16:21])

    for step in range(s+1, s+30001):
    
        # 텐서보드
        # 원래코드 : sess.run(train_step, feed_dict={X: X_data, Y_Lable: Y_data})
        # summary도 텐서플로우이기 때문에 run 해야해서 추가
        # 마지막으로 add_summary(summary, x축)를 해준다
        summary, _ = sess.run([merged_summary, train_step], feed_dict={X: X_data, Y_Lable: Y_data})
        writer.add_summary(summary, global_step=step)

        if step % 100 == 0:

            # 학습 데이터 저장하기
            # saver.save(세션, 파일명, 스텝(생략가능))
            # ex) saved/ckpt_test-스텝 파일 생성
            save_path = 'saved/ckpt_test2'
            saver.save(sess, save_path, global_step=step)

            print(sess.run(accuracy, feed_dict={X: X_data, Y_Lable: Y_data}))

    pred = sess.run(tf.argmax(outputLayer, 1), feed_dict={X: X_data})
    print(pred)