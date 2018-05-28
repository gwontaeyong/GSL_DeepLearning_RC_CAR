import argparse
import socket
import sys


from PyQt5.QtWidgets import QApplication
#from GUI_Interface.window import Window_GUI
from GUI_Interface.drive_predict_window import Window_GUI
from Low_Server.stream_server_QT_thread import StreamServer
from Low_Server.command_server_QT_thread import CmdServer


if __name__ == "__main__":
    #호스트, 포트 번호 선언

    parser = argparse.ArgumentParser()
<<<<<<< HEAD

    parser.add_argument('-shost', type=str, default=socket.gethostbyname(socket.gethostname()))
=======
    default_host = socket.gethostbyname(socket.gethostname())
    model_path = "../DeepLearning/saved/sample4/sample4_1-4000"
    default_host = "192.168.0.5"

    parser.add_argument('-host', type=str, default= default_host)
>>>>>>> 534cea4... save
    parser.add_argument('-sp', type=int, default="8002")
    parser.add_argument('-chost', type=str, default=socket.gethostbyname(socket.gethostname()))
    parser.add_argument('-cp', type=int, default="8001")
    parser.add_argument('-load', type=str, default=model_path)

    FLAGS, _ = parser.parse_known_args()


    shost = FLAGS.shost
    sport = FLAGS.sp
    chost = FLAGS.chost
    cport = FLAGS.cp
    load_path = FLAGS.load

    '''
    sess = tf.Session()
    m1 = Model(sess, "m1")
    m1.saver.restore(sess, load_path)
    '''

    print("Compare Server Strat")

    streaming_server = StreamServer(shost, sport)
    cmd_server = CmdServer(chost, cport, load_path)

    #streaming_server.changePixmap.connect(ex.setImage)
    streaming_server.predicSteering.connect(cmd_server.send_cmd)
    #cmd_server.change_steering_label.connect(ex.repaint_steering_labels)
    #cmd_server.change_speed_label.connect(ex.repaint_speed_labels)

    streaming_server.start()
    cmd_server.start()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            break;



