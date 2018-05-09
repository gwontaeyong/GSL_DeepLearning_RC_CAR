import socket
import threading

class CmdServer(threading.Thread):

    def __init__(self, host, port):
        super(CmdServer, self).__init__()
        self.cmd_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)
        self.buf_size = 256
        self.flag = True
        self.cmd_server.bind(server_address)
        self.cmd_server.listen(1)

    def run(self):
        print("waiting cmd_client")
        self.conn, addr = self.cmd_server.accept()
        print("start cmd_server")
        print("connect with %s"%self.conn)
        self.client_recv()

    def __del__(self):
        print("cmd_server is close")

    def client_send(self, cmd):
        self.conn.send(cmd.encode())

    def client_recv(self):

        while True:
            reply = self.conn.recv(self.buf_size)
            if not reply:
                break
            else:
                print("received", reply.decode())


if __name__ == "__main__":
    cmd_server = CmdServer("",8001)
    cmd_server.start()