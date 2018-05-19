import cv2 as cv
import numpy as np
import tensorflow as tf
import os


class Model:
    def __init__(self, sess, name, rate=0.005, logs_path="./logs/sample4_1"):
        self.sess = sess
        self.name = name
        self.height = 140
        self.wedith = 320
        self.nb_class = 9
        self.learning_rate = rate
        self.logs_path = logs_path

        # X데이터와 Y데이터를 담을 placeholder
        self.X = tf.placeholder(tf.float32, [None, self.height * self.wedith])
        self.Y = tf.placeholder(tf.int32, shape=[None,1])

        self.Y_one_hot = tf.one_hot(self.Y, self.nb_class)
        self.Y_one_hot = tf.reshape(self.Y_one_hot, [-1, self.nb_class])

        self.training = tf.placeholder(tf.bool)

        self._build_net()

    def _build_net(self):

        with tf.variable_scope(self.name):
            # Convolutional Layer #1
            # 140 * 320 * 1 => 70 * 160 * 24

            X_img = tf.reshape(self.X, shape=[-1, self.height, self.wedith, 1])

            conv1 = tf.layers.conv2d(inputs=X_img, filters=24, kernel_size=[5, 5], padding="SAME",
                                     activation=tf.nn.relu)
            pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], padding="SAME", strides=2)
            dropout1 = tf.layers.dropout(inputs=pool1, rate=0.3, training=self.training)

            # Convolutional Layer #2
            # 70 * 160 * 24 => 35 * 80 * 36
            conv2 = tf.layers.conv2d(inputs=dropout1, filters=36, kernel_size=[5, 5], padding="SAME",
                                     activation=tf.nn.relu)
            pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], padding="SAME", strides=2)
            dropout2 = tf.layers.dropout(inputs=pool2, rate=0.3, training=self.training)

            # Convolutional Layer #3
            # 35 * 80 * 36 => 18 * 40 * 48
            conv3 = tf.layers.conv2d(inputs=dropout2, filters=48, kernel_size=[5, 5], padding="SAME",
                                     activation=tf.nn.relu)
            pool3 = tf.layers.max_pooling2d(inputs=conv3, pool_size=[2, 2], padding="SAME", strides=2)
            dropout3 = tf.layers.dropout(inputs=pool3, rate=0.3, training=self.training)

            # Convolutional Layer #4
            # 18 * 40 * 48 => 9 * 20 * 64
            conv4 = tf.layers.conv2d(inputs=dropout3, filters=64, kernel_size=[3, 3], padding="SAME",
                                     activation=tf.nn.relu)
            pool4 = tf.layers.max_pooling2d(inputs=conv4, pool_size=[2, 2], padding="SAME", strides=2)
            dropout4 = tf.layers.dropout(inputs=pool4, rate=0.3, training=self.training)

            # Convolutional Layer #5
            # 9 * 20 * 64 => 5 * 10 * 64
            conv5 = tf.layers.conv2d(inputs=dropout4, filters=64, kernel_size=[3, 3], padding="SAME",
                                     activation=tf.nn.relu)
            pool5 = tf.layers.max_pooling2d(inputs=conv5, pool_size=[2, 2], padding="SAME", strides=2)
            dropout5 = tf.layers.dropout(inputs=pool5, rate=0.3, training=self.training)

            # Convolutional Layer #6
            # 5 * 10 * 64 => 3 * 8 * 64
            conv6 = tf.layers.conv2d(inputs=dropout5, filters=64, kernel_size=[3, 3], padding="VALID",
                                     activation=tf.nn.relu)
            dropout6 = tf.layers.dropout(inputs=conv6, rate=0.3, training=self.training)

            # FC Layer #1
            # 3 * 8 * 64 = 1536 => 600
            flat = tf.reshape(dropout6, [-1, 3 * 8 * 64])
            dense7 = tf.layers.dense(inputs=flat, units=600, activation=tf.nn.relu)
            dropout7 = tf.layers.dropout(inputs=dense7, rate=0.5, training=self.training)

            # FC Layer #2
            # 600 => 100
            dense8 = tf.layers.dense(inputs=dropout7, units=100, activation=tf.nn.relu)
            dropout8 = tf.layers.dropout(inputs=dense8, rate=0.5, training=self.training)

            # FC Layer #3
            # 50 => 10
            #dense9 = tf.layers.dense(inputs=dropout8, units=10, activation=tf.nn.relu)
            #dropout9 = tf.layers.dropout(inputs=dense9, rate=0.5, training=self.training)

            # Y : 6가지
            # 100 => 6
            self.logits = tf.layers.dense(inputs=dropout8, units=self.nb_class)

        # 최적화
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels= self.Y_one_hot))
        self.optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(self.cost)

        # loss summary
        self.cost_summ = tf.summary.scalar("cost", self.cost)

        # 저장에 관련된 saver
        # Saver()의 인자로 변수 리스트를 주면 해당 변수만 저장
        # 인자를 안주면 saver 생성 시점까지 초기화 된 변수만 저장(이 코드 위의 변수들)
        self.saver = tf.train.Saver()

        # 정확도 기록
        correct_prediction = tf.equal(tf.argmax(self.logits, 1), tf.argmax(self.Y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        # accuracy summary
        self.accuracy_summ = tf.summary.scalar("accuracy", self.accuracy)

        # 텐서보드
        # summary들을 merge 하고 파일 경로를 지정해준다
        # 세션의 그래프를 추가한다
        # 커맨드창에서 실행 : tensorboard --logdir=파일경로
        # => 파일경로를 C드라이브 부터 주던지 or cmd에서 디렉토리 이동 후 logs_path의 경로를 주던지
        # 그 후 커맨드창에 나타난 url을 인터넷으로 접속 (http://127.0.0.1:6006)
        self.merged_summary = tf.summary.merge_all()
        self.writer = tf.summary.FileWriter(self.logs_path)
        self.writer.add_graph(self.sess.graph)

    def predict(self, x_test, training=False):
        return self.sess.run(tf.argmax(self.logits, 1), feed_dict={self.X: x_test, self.training: training})

    def get_accuracy(self, x_test, y_test, training=False):
        return self.sess.run(self.accuracy, feed_dict={self.X: x_test, self.Y: y_test, self.training: training})

    def train(self, x_data, y_data, training=True):
        return self.sess.run([self.merged_summary, self.optimizer],
                             feed_dict={self.X: x_data, self.Y: y_data, self.training: training})