import threading, time
import socket
class TCP_Thread(threading.Thread):
    global rc_car
    global key
    global panel

    def __init__(self, host, port):
        super(TCP_Thread, self).__init__()
        self._stop_event = threading.Event()
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP 소켓 생성
        self.flag = True

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):

        try:
            # 서버로 연결
            self.client_socket.connect((self.host, self.port))
            print("connected")

            # 명령 받기
            while self.flag:

                response = self.client_socket.recv(256).decode()

                if response:
                    threading.Thread(target=rc_car.doing_cmd, args=(response,)).start()

        except ConnectionRefusedError:
            print("서버에 연결 할 수 없습니다.")

    def __del__(self):
        print("소켓 스레드 종료")

# github test
