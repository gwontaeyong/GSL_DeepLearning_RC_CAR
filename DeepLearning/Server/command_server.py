import socket
import sys
import keyboard
import argparse

def send_commend(*arg):

    data = ""
    for code in arg:
        data += code

    print(data)
    conn.send(data.encode())


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

    keyboard.add_hotkey('up', send_commend, args=('u'))
    keyboard.add_hotkey('down', send_commend, args=('d'))
    keyboard.add_hotkey('left', send_commend, args=('l'))
    keyboard.add_hotkey('right', send_commend, args=('r'))

    '''
    keyboard.add_hotkey('up+left', send_commend, args=('ul'))
    keyboard.add_hotkey('up+right', send_commend, args=('ur'))
    keyboard.add_hotkey('down+left', send_commend, args=('dl'))
    keyboard.add_hotkey('down+right', send_commend, args=('dr'))
    '''
    keyboard.wait()

    conn.close()


