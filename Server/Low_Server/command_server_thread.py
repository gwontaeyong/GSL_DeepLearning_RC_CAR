import socket
from PyQt5.QtCore import QThread, pyqtSignal

class CmdServer(QThread):

    change_speed_label = pyqtSignal(int, str)
    change_steering_label = pyqtSignal(int, str)

    def __init__(self, host, port):
        super().__init__()

        self.cmd_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)
        self.buf_size = 3
        self.flag = True
        self.cmd_server.bind(server_address)
        self.cmd_server.listen(1)
        self.ex_steering = 4
        self.ex_speed = 0

    def run(self):
        print("waiting cmd_client")
        self.conn, addr = self.cmd_server.accept()
        print("start cmd_server")
        print("connect with %s" % self.conn)
        self.client_recv()

    def client_send(self, cmd):
        self.conn.send(cmd.encode())

    def client_recv(self):
        while self.flag:
            reply = self.conn.recv(self.buf_size)
            if not reply:
                break
            else:
                data = str(reply.decode()).split("_")
                steering_index = int(data[0])
                speed_index = int(data[1])
                self.change_steering_label.emit(steering_index, "green")
                self.change_speed_label.emit(speed_index, "green")

    def __del__(self):
        print("cmd_server is close")
        self.wait()

