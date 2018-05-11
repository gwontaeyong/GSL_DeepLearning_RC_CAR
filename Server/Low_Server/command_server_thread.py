import socket
import threading


class CmdServer(threading.Thread):
    def __init__(self, host, port, labels):
        super(CmdServer, self).__init__()
        self.cmd_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)
        self.buf_size = 3
        self.flag = True
        self.cmd_server.bind(server_address)
        self.cmd_server.listen(1)
        self.labels = labels
        self.ex_index = 4

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
                self.repaint_steering_labels(int(str(reply.decode()).split("_")[0]), "green")

    def repaint_steering_labels(self, index, color):
        print("index ", index)
        if index != self.ex_index:
            self.labels[self.ex_index].setStyleSheet('QLabel { '
                                                     'background-color:white;'
                                                     '}')

            self.labels[index].setStyleSheet('QLabel { '
                                                'background-color:' + color + ';'
                                                '}')
        self.ex_index = index

    def __del__(self):
        print("cmd_server is close")


if __name__ == "__main__":
    cmd_server = CmdServer("", 8001)
    cmd_server.start()
