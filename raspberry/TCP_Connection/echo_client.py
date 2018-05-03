import socket 
import sys



host = '192.168.0.37'
port = 8001
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP 소켓 생성

try:
    client_socket.connect((host,port))
    print("connected")
    while True:
        response = client_socket.recv(1024).decode()
        if response:
            print(type(response))
            print("resonpse : ", response)
except KeyboardInterrupt:
	client_socket.close()

finally:
    client_socket.close()

print('disconnected')
