import socket
import sys
import keyboard
import argparse
import threading

def send_commend(conn):
    while True:
        data = conn.recv(7).decode()
        if data:
            print(data)



if __name__ == "__main__":
    #호스트, 포트 번호 선엉
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', type=str, default= socket.gethostbyname(socket.gethostname()))
    parser.add_argument('-p', type=int, default= "8001")
    FLAGS, _ = parser.parse_known_args()

    host = FLAGS.host
    port = FLAGS.p

    print(host)
    print(port)
    #소켓 생성
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.bind((host, port))
    mySocket.listen(1)

    #연결 받기
    conn, addr = mySocket.accept()
    print("Connection from: " + str(addr))

    thread_rcvmsg = threading.Thread(target=send_commend(conn))
    thread_rcvmsg.start()
    print("Test")

    while True:
        data = "test"
        conn.send(data.encode())

    conn.close()


