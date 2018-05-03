import threading, time
import socket
import select
import RPi.GPIO as gpi


class RC_car:
    def __init__(self, motor_pin1, motor_pin2, servo_pin):
        gpi.setmode(gpi.BCM)

        # servo value
        self.angle = 7.5  # 7.5 = midle
        self.center = 7.5  # center value
        self.left = 5  # left value
        self.right = 9  # right value
        self.servo_pwm = 50  # servo pwm value
        self.servo_motor_pin = servo_pin
    
        # dcmotor value
        self.speed = 0  # dutycycle -> 0 - >  60 ~ 80
        self.max_speed = 70 #maxspeed
        self.min_speed = 20 #차량이 움직일수 있는 최소 dutycycle
        self.rate = 2
        self.dc_pwm = 20  # DCmotor pwm
        self.dc_motor_pin1 = motor_pin1
        self.dc_motor_pin2 = motor_pin2

        # 핀 아웃 설정
        gpi.setup(self.dc_motor_pin1, gpi.OUT)
        gpi.setup(self.dc_motor_pin2, gpi.OUT)
        gpi.setup(self.servo_motor_pin, gpi.OUT)
        gpi.output(self.dc_motor_pin2, False)

        # DC모터,SERVO모터 생성
        self.servo = gpi.PWM(servo_pin, self.servo_pwm)
        self.motor = gpi.PWM(self.dc_motor_pin1, self.dc_pwm)
        
        # DC모터, SERVO모터 실행
        self.motor.start(self.speed) #speed 0으로 모터 시작
        self.servo.start(self.angle) #centor 로 서보모터 시작
        
        print("make RC CAR")

    def doing_cmd(self, cmd):

        if cmd == 'u':
            self.speed_up()
        elif cmd == 'd':
            self.speed_down()
        elif cmd == 'l':
            self.turn_left()
        elif cmd == 'r':
            self.turn_right()
        elif cmd == 'ul':
            self.speed_up()
            self.turn_left()
        elif cmd == 'ur':
            self.speed_up()
            self.turn_right()
        elif cmd == 'dl':
            self.speed_down()
            self.turn_left()
        elif cmd == 'dr':
            self.speed_down()
            self.turn_right()
        elif cmd == 'stop':
            self.angle = self.center
            self.speed = 0
            self.servo.ChangeDutyCycle(self.angle)
            self.motor.ChangeDutyCycle(self.speed)

    # 좌회전
    def turn_left(self):
        if (self.angle <= self.left):
            self.angle = self.left
        else:
            self.angle -= 0.5
        self.servo.ChangeDutyCycle(self.angle)

    # 우회전
    def turn_right(self):
        if(self.angle >= self.right):
            self.angle = self.right
        else:
            self.angle += 0.5
        self.servo.ChangeDutyCycle(self.angle)

    # 중앙 정렬
    def turn_center(self):
        self.angle = self.center
        self.servo.ChangeDutyCycle(self.angle)

    def speed_up(self):
        if self.speed == 0:
            self.speed = self.min_speed
        elif self.speed >= self.min_speed and self.speed < self.max_speed:
            self.speed += self.rate
        elif self.speed >= self.max_speed:
            self.speed = self.max_speed
        self.motor.ChangeDutyCycle(self.speed)

    def speed_down(self):
        if self.speed <= self.min_speed:
            self.speed = 0
        elif self.speed > self.min_speed and self.speed <= self.max_speed:
            self.speed -= self.rate
        self.motor.ChangeDutyCycle(self.speed)

    def __del__(self):
        print("DC Motor del")
       



class Panel_Thread(threading.Thread):
    def __init__(self):
        super(Panel_Thread, self).__init__()
        print("Panel_Thread start")
        global rc_car

    def run(self):
        while True:
            print("speed : ", rc_car.speed, "direct : ", rc_car.angle)
            # time.sleep(1)

    def __del__(self):
        print('판넬 종료')

   

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
       

    def run(self):

        try:
            # 서버로 연결
            self.client_socket.connect((self.host, self.port))
            print("connected")

            # 명령 받기
            while True:                                
                ready = select.select([self.client_socket], [], [], 0.5)

                if ready[0]:
                    response = self.client_socket.recv(256).decode()
                else:
                    response = 'stop'
                    
                threading.Thread(target=rc_car.doing_cmd, args=(response,)).start()

        except ConnectionRefusedError:
            print("서버에 연결 할 수 없습니다.")

    def __del__(self):
        print("소켓 스레드 종료")
        self.client_socket.close()


key = 'g'
dc_motor_pin1 = 19  # DC모터 pwm 사용 pin
dc_motor_pin2 = 26  # DC모터 pin2
servo_pin1 = 18  # 서보모터


host = '192.168.0.37'  # 서버 주소
port = 8001  # 서버 연겨 포트

rc_car = RC_car(dc_motor_pin1, dc_motor_pin2, servo_pin1)  # RC카 핀, pwm, speed, direct 를 가진 클래스

panel = Panel_Thread()  # RC카의 속도, 방향을 출력해주는 쓰레드
panel.daemon = True
tcp_thread = TCP_Thread(host, port)
tcp_thread.daemon = True

try:
    tcp_thread.start()
    panel.start()

    while True:
        if key == 'q':
            break

except ConnectionResetError:
    print("클라이언트가 연결을 종료 하였습니다.")

except KeyboardInterrupt:
    print("종료합니다.")

finally:
    print("finally")
    rc_car.motor.stop()
    gpi.cleanup()
    tcp_thread.client_socket.close()


