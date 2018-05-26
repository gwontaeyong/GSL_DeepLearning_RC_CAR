import argparse
import sys
import datetime

from PyQt5.QtWidgets import QApplication
from GUI_Interface.drive_record_window import Window_GUI

from Low_Server.stream_server_QT_thread import StreamServer
from Low_Server.command_server_QT_thread import CmdServer



if __name__ == "__main__":
    #호스트, 포트 번호 선언

    parser = argparse.ArgumentParser()
    defalut_host = '192.168.0.5'
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d')

    parser.add_argument('-host', type=str, default=defalut_host)
    parser.add_argument('-sp', type=int, default="8002")
    parser.add_argument('-cp', type=int, default="8001")
    parser.add_argument('-data_path', type=str, default=nowDate)

    FLAGS, _ = parser.parse_known_args()

    host = FLAGS.host
    sport = FLAGS.sp
    cport = FLAGS.cp
    data_path = FLAGS.data_path


    print("Data acquistion Strat")

    app = QApplication(sys.argv)
    ex = Window_GUI(data_path)

    streaming_server = StreamServer(host, sport)
    cmd_server = CmdServer(host, cport)

    streaming_server.changePixmap.connect(ex.setImage)
    cmd_server.change_rc_steering_label.connect(ex.repaint_steering_labels)
    cmd_server.change_rc_speed_label.connect(ex.repaint_speed_labels)

    streaming_server.start()
    cmd_server.start()

    sys.exit(app.exec())


