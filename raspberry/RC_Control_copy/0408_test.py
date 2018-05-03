import threading, time
import socket
import select
import RPi.GPIO as gpi



class RC_car:

    def __init__(self, motor_pin1, motor_pin2, servo_pin1, servo_pin2):
        gpi.setmode(gpi.BCM)

        self.direct = 'c'
        self.speed = 0  # dutycycle -> 0 - >  60 ~ 80
        self.pwm = 9000  # DCmotor pwm

        self.dc_motor_pin1 = motor_pin1
        self.dc_motor_pin2 = motor_pin2
        self.servo_motor_pin1 = servo_pin1
        self.servo_motor_pin2 = servo_pin2

        # 핀 아웃 설정
        gpi.setup(self.dc_motor_pin1, gpi.OUT)
        gpi.setup(self.dc_motor_pin2, gpi.OUT)
        gpi.setup(self.servo_motor_pin1, gpi.OUT)
        gpi.setup(self.servo_motor_pin2, gpi.OUT)

        # DC모터 생성
        gpi.output(self.dc_motor_pin2, False)

        # DC모터 실행
        self.motor = gpi.PWM(self.dc_motor_pin1, self.pwm)
        self.motor.start(self.speed)

        print("make RC CAR")

    def doing_cmd(self, cmd):

        if cmd == 'u':
            self.speed_up()
        elif cmd == 'd':
            self.speed_down()
        elif cmd == 'l':
            self.direct = 'l'
        elif cmd == 'r':
            self.direct = 'r'
        elif cmd == 'ul':
            self.speed_up()
            self.direct = 'l'
        elif cmd == 'ur':
            self.speed_up()
            self.direct = 'r'
        elif cmd == 'dl':
            self.speed_down()
            self.direct = 'l'
        elif cmd == 'dr':
            self.speed_down()
            self.direct = 'r'
        elif cmd == 'stop':
            self.direct = 'c'

        self.choose_direct()


    def choose_direct(self):
        if self.direct == 'l':
            self.turn_left()
        elif self.direct == 'r':
            self.turn_right()
        else :
            self.turn_center()

    #좌회전
    def turn_left(self):
        gpi.output(self.servo_motor_pin1, True)
        gpi.output(self.servo_motor_pin2, False)

    # 우회전
    def turn_right(self):
        gpi.output(self.servo_motor_pin1, False)
        gpi.output(self.servo_motor_pin2, True)

    # 중앙 정렬
    def turn_center(self):
        gpi.output(self.servo_motor_pin1, True)
        gpi.output(self.servo_motor_pin2, True)

    def speed_up(self):
        if self.speed == 0 :
            self.speed = 60
        elif self.speed >= 60 and self.speed <80:
            self.speed += 5
        elif self.speed >=80:
            self.speed = 80

        self.motor.ChangeDutyCycle(self.speed)

    def speed_down(self):
        if self.speed <= 60 :
            self.speed = 0
        elif self.speed > 60 and self.speed <=80:
            self.speed -= 5
        self.motor.ChangeDutyCycle(self.speed)

    def __del__(self):
        print("DC Motor del")
        gpi.cleanup()

class Panel_Thread(threading.Thread):
    def __init__(self):
        super(Panel_Thread, self).__init__()
        self._stop_event = threading.Event()
        self.flag = True
        print("Panel_Thread start")
        global rc_car

    def run(self):
        while self.flag:
            print("speed : ", rc_car.speed, "direct : ", rc_car.direct)
            # time.sleep(1)

    def __del__(self):
        print('판넬 종료')

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


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
            self.client_socket.settimeout(0)
            print("connected")

            # 명령 받기
            while self.flag:
                ready = select.select([self.client_socket], [], [], 0.5)
                
                if ready[0]:
                    response = self.client_socket.recv(256).decode()
                else:
                    response = 'stop'
                
                if response == 'q':
                    key = 'q'
                    panel.flag = False
                    self.flag = False
                else:
                    threading.Thread(target=rc_car.doing_cmd, args=(response,)).start()
        except ConnectionRefusedError:
            print("서버에 연결 할 수 없습니다.")

    def __del__(self):
        print("소켓 스레드 종료")



key = 'g'
dc_motor_pin1 = 19  # DC모터 pwm 사용 pin
dc_motor_pin2 = 26  # DC모터 pin2
servo_pin1 = 6  # 서보모터
servo_pin2 = 13  # 서보모터

host = '192.168.0.37'  # 서버 주소
port = 8001  # 서버 연겨 포트

rc_car = RC_car(dc_motor_pin1, dc_motor_pin2, servo_pin1, servo_pin2)  # RC카 핀, pwm, speed, direct 를 가진 클래스

panel = Panel_Thread()  # RC카의 속도, 방향을 출력해주는 쓰레드
tcp_thread = TCP_Thread(host, port)

try:
    tcp_thread.start()
    panel.start()

    while True:
        if key == 'q' :
            break
except ConnectionResetError:
    print("클라이언트가 연결을 종료 하였습니다.")

except KeyboardInterrupt:
    print("종료합니다.")
    panel.flag = False
    tcp_thread.flag = False

finally:
    print("finally")
    rc_car.motor.stop()
    tcp_thread.client_socket.close()
    


