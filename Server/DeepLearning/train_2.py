from DeepLearning.ndivia_model_2 import *
from DeepLearning.InputData import *
import tensorflow as tf


csv_file = 'csv/2018-05-28_track_2.csv'
input_data = InputData(csv_file)

rate_ = 1e-5
dir_name = "track_2_sameple2"
model_name = "track_2_sample2_epcho"
log_path = "logs/"+model_name+'/'
save_path = 'saved/'+ dir_name + "/"+model_name

load = True
load = False
load_path = 'saved/track_2_sameple2/track_2_sample2_epcho-24'


sess = tf.Session()
m1 = Model(sess, "m1", rate = rate_, logs_path = log_path )

epcho_ = 0

if load:
    m1.saver.restore(sess, load_path)
    epcho_ = int(load_path.split("-")[1])
    print("Load start")
else:
    sess.run(tf.global_variables_initializer())
    print("Un Load start")



print('Learning Started!')

coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)

total_epcho = 25
first_cost = None
temp_cost = 1

'''
for step  in range(epcho_+1, epcho_ + total_epcho):
    print("%d Epcho " % (step))

    try:
        img_addr, steering, speed = sess.run(
            [input_data.batch_addr, input_data.batch_steering, input_data.batch_speed])
        x_data = input_data.make_x_data(img_addr)
        summary, optimize, cost = m1.train(x_data, steering)
        m1.writer.add_summary(summary, global_step=step)

        if temp_cost > cost:
            print("Re new Model")
            print("EX_cost : %f,  cost : %f" % (temp_cost, cost))
            temp_cost = cost
            m1.saver.save(sess, save_path + "_best", global_step=step)

        #m1.saver.save(sess, save_path, global_step=step)
        predicted_value, real_value, accuracy = m1.get_accuracy(x_data, steering)
        print("epcho : %d,  Accuracy : %f,   Lose : %f " % (step, accuracy, cost))
        print("Predicted : ", predicted_value, "\n")
        print("Real : ", real_value, "\n\n")

    except KeyboardInterrupt:
        break

'''

for epcho in range(epcho_+1, epcho_ + total_epcho):
    print("%d Epcho " % (epcho))

    try:
        for batch in range(input_data.total_batch_size):

            img_addr, steering, speed = sess.run(
                [input_data.batch_addr, input_data.batch_steering, input_data.batch_speed])
            x_data = input_data.make_x_data(img_addr)
            summary, optimize, cost = m1.train(x_data, steering)
            m1.writer.add_summary(summary, global_step=batch)

            if temp_cost > cost:
                print("Re new Model")
                print("EX_cost : %d,  cost : %f"%(temp_cost, cost))
                temp_cost = cost
                m1.saver.save(sess, save_path+"_best", global_step=epcho)

            m1.saver.save(sess, save_path, global_step=epcho)
            predicted_value, real_value, accuracy = m1.get_accuracy(x_data, steering)
            print("epcho : %d, batch : %d,   Accuracy : %f,   Lose : %f " % (epcho, batch + 1, accuracy, cost))
            print("Predicted : ", predicted_value, "\n")
            print("Real : ", real_value, "\n\n")
    except KeyboardInterrupt:
        break

coord.request_stop()
coord.join(threads)
print('stop batch')
print('Learning Finished!')
