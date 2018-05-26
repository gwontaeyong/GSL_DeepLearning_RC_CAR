from DeepLearning.ndivia_model import *
from DeepLearning.InputData import *
import tensorflow as tf


inputData = InputData("output.csv")

model_name = "test_model"
save_path = 'saved/' + model_name
load = True
#loas = False
load_path = 'saved/sample4_1-4000'

s = 0

sess = tf.Session()
m1 = Model(sess, "m1")


if load:
    m1.saver.restore(sess, load_path)
    s = int(load_path.split("-")[1])
else:
    sess.run(tf.global_variables_initializer())
    print("Test")



print('Learning Started!')

coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

for step in range(s + 1, s + 2001):

    img_addr, steering, speed = sess.run([inputData.batch_addr, inputData.batch_steering, inputData.batch_speed])
    x_data = inputData.make_x_data(img_addr)

    summary, optimize, cost = m1.train(x_data, steering)

    m1.writer.add_summary(summary, global_step=step)

    if step % 100 == 0:
        predicted_value, real_value, accuracy = m1.get_accuracy(x_data, steering)
        print("step : %d,   Accuracy : %f,   Lose : %f "%(step+1, accuracy, cost))
        print("Predicted : ", predicted_value, "\n")
        print("Real : ", real_value, "\n\n")


m1.saver.save(sess, save_path, global_step=step)
coord.request_stop()
coord.join(threads)
print('stop batch')
print('Learning Finished!')
