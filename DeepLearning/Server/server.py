import socket
import sys
import threading


sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.0.37', 8001)
sckt.bind(server_address)
sckt.listen(1)

conn, addr = sckt.accept()

print("start")
def client_send():
    while True:
        message = input("Text: ")
        if message:
            conn.send(message.encode())


def client_recv():
    while True:
        reply = conn.recv(1024)
        if not reply:
            break
        else:
            print("received", reply.decode())


thread_send = []
thread_rcv = []
num_threads = 1

threading.Thread(target=client_recv).start()
threading.Thread(target=client_send).start()