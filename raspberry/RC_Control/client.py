<<<<<<< HEAD
#!/bin/python

import socket
import threading
import time

tLock = threading.Lock()
poweroff = False

def receving(name, sock):
    while not poweroff:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print (str(data))
        except:
            pass
        finally:
            tLock.release()

host = '192.168.0.37'
port = 8000

server = ('192.168.0.37', 8000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)
rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

alias = input("Username: ")
time.sleep(0.2)

message = input(alias + ">>> ")
while message != 'q':
    if message != "":
        s.send(message.encode())
    tLock.acquire()
    message = input(alias + ">>> ")
    tLock.release()
    time.sleep(0.2)

poweroff = True
rT.join()
=======
#!/bin/python

import socket
import threading
import time

tLock = threading.Lock()
poweroff = False

def receving(name, sock):
    while not poweroff:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print (str(data))
        except:
            pass
        finally:
            tLock.release()

host = '192.168.0.37'
port = 8000

server = ('192.168.0.37', 8000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)
rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

alias = input("Username: ")
time.sleep(0.2)

message = input(alias + ">>> ")
while message != 'q':
    if message != "":
        s.send(message.encode())
    tLock.acquire()
    message = input(alias + ">>> ")
    tLock.release()
    time.sleep(0.2)

poweroff = True
rT.join()
>>>>>>> 9bf5a7977fb5d85d3d0cf55790e78db2b33f8128
s.close()