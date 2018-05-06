import socket
import sys
import threading

sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 9999)
sckt.connect((server_address))


def client_send():
    while True:
        message = input("Text: ")
        sckt.send(message.encode())


def client_recv():
    while True:
        reply = sckt.recv(1024)
        print("received", reply.decode())


thread_send = []
thread_rcv = []
num_threads = 1

threading.Thread(target=client_send).start()
client_recv()
