import argparse
import socket

from Low_Server.stream_server_thread import StreamServer
from Low_Server.command_server_thread import CmdServer

if __name__ == "__main__":
    #호스트, 포트 번호 선언
    parser = argparse.ArgumentParser()
    parser.add_argument('-shost', type=str, default= socket.gethostbyname(socket.gethostname()))
    parser.add_argument('-sp', type=int, default= "8002")
    parser.add_argument('-chost', type=str, default=socket.gethostbyname(socket.gethostname()))
    parser.add_argument('-cp', type=int, default="8001")
    FLAGS, _ = parser.parse_known_args()

    shost = FLAGS.shost
    sport = FLAGS.sp
    chost = FLAGS.chost
    cport = FLAGS.cp

    print("Compare Server Strat")

    streaming_server = StreamServer(shost, sport)
    cmd_server = CmdServer(chost, cport)
    streaming_server.start()
    cmd_server.start()




