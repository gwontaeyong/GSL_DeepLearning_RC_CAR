from DeepLearning.ndivia_model import *
from DeepLearning.InputData import *

import tensorflow as tf


input_data = InputData("output.csv")
model_name = "sample4_1-4000"
load_path = 'saved/'+model_name

sess = tf.Session()

m1 = Model(sess, "m1")
m1.saver.restore(sess, load_path)


coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

total_epcho = 1

for epcho in range(total_epcho):
    print("%d Epcho "%(epcho+1))

    for batch in range(input_data.total_batch_size):
        print("%d Batch " % (batch + 1), "\n")
        img_addr, steering, speed = sess.run([input_data.batch_addr, input_data.batch_steering, input_data.batch_speed])
        x_data = input_data.make_x_data(img_addr)
        predict, value, accuracy = m1.get_accuracy(x_data, steering)
        print("Value = ", value, "\n")
        print("Predict : ", predict, "\n")
        print(" Accuracy : ", accuracy, "\n")
    print("====================================================================================================")

coord.request_stop()
coord.join(threads)





