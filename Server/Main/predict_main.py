import argparse
import socket
import sys
import tensorflow as tf

from PyQt5.QtWidgets import QApplication


from GUI_Interface.drive_window import Window_GUI

from Low_Server.stream_server_QT_thread import StreamServer
from Low_Server.command_server_QT_thread import CmdServer
from Low_Server.data_control_thread import DataControl

from DeepLearning.ndivia_model import Model

if __name__ == "__main__":
    #호스트, 포트 번호 선언

    app = QApplication(sys.argv)
    ex = Window_GUI()

    parser = argparse.ArgumentParser()
    default_host = socket.gethostbyname(socket.gethostname())

    default_host = "192.168.0.5"

    parser.add_argument('-host', type=str, default= default_host)
    parser.add_argument('-sp', type=int, default="8002")
    parser.add_argument('-cp', type=int, default="8001")
    parser.add_argument('-load', type=str, default="../DeepLearning/saved/sample4_1-2000")

    FLAGS, _ = parser.parse_known_args()
    print("host = ", default_host)

    host = FLAGS.host
    sport = FLAGS.sp
    cport = FLAGS.cp
    load_path = FLAGS.load


    sess = tf.Session()
    m1 = Model(sess, "m1")
    m1.saver.restore(sess, load_path)

    print("Compare Server Strat")

    streaming_server = StreamServer(host, sport)
    cmd_server = CmdServer(host, cport, False)
    data_control = DataControl(m1)

    streaming_server.changePixmap.connect(ex.setImage)
    streaming_server.sendImage.connect(data_control.put_image)

    data_control.change_predict_steering_label.connect(ex.repaint_rc_steering_labels)
    data_control.send_cmd_ras.connect(cmd_server.send_cmd)

    streaming_server.start()
    cmd_server.start()
    data_control.start()

    sys.exit(app.exec())


