import threading, time
import socket
import select
import RPi.GPIO as gpi
import picamera
import sys, tty, termios, time
from datetime import datetime

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
        self.max_speed = 50 #maxspeed
        self.min_speed = 20 #차량이 움직일수 있는 최소 dutycycle
        self.dc_pwm = 15  # DCmotor pwm
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

        if cmd == '8':
            self.speed_up()
        elif cmd == '5':
            self.speed_down()
        elif cmd == '4':
            self.turn_left()
        elif cmd == '6':
            self.turn_right()
        else:
            print("else")
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
        
    '''
    # 좌회전
    def turn_left(self):
        self.angle = self.left
        self.servo.ChangeDutyCycle(self.angle)

    # 우회전
    def turn_right(self):
        self.angle = self.right
        self.servo.ChangeDutyCycle(self.angle)
    '''
    # 중앙 정렬
    def turn_center(self):
        self.angle = self.center
        self.servo.ChangeDutyCycle(self.angle)

    def speed_up(self):
        if self.speed == 0:
            self.speed = self.min_speed
        elif self.speed >= self.min_speed and self.speed < self.max_speed:
            self.speed += 5
        elif self.speed >= self.max_speed:
            self.speed = self.max_speed
        self.motor.ChangeDutyCycle(self.speed)

    def speed_down(self):
        if self.speed <= self.min_speed:
            self.speed = 0
        elif self.speed > self.min_speed and self.speed <= self.max_speed:
            self.speed -= 5
        self.motor.ChangeDutyCycle(self.speed)

    def __del__(self):
        print("DC Motor del")
        

class Camera(threading.Thread):
    def __init__(self):
        super(Camera, self).__init__()
        global rc_car
        self.camera = picamera.PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = (320, 240)

    def run(self):
        while True:
            #print("speed : ", rc_car.speed, "direct : ", rc_car.angle)
            path = "/home/GSL/raspberry/images/"+datetime.today().strftime("%m:%d_%H:%M:%S")+str(rc_car.angle)+"_"+str(rc_car.speed)+".jpg"
            self.camera.capture(path)
            time.sleep(1)
            
class Panel_Thread(threading.Thread):

    def __init__(self):
        super(Panel_Thread, self).__init__()
        
        time.sleep(2)
        self._stop_event = threading.Event()
        self.flag = True
        print("Panel_Thread start")
        global rc_car

    def run(self):
        while True:
            print("speed : ", rc_car.speed, "direct : ", rc_car.angle)
            time.sleep(1)

    def __del__(self):
        print('판넬 종료')

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch


dc_motor_pin1 = 19  # DC모터 pwm 사용 pin
dc_motor_pin2 = 26  # DC모터 pin2
servo_pin1 = 18  # 서보모터



rc_car = RC_car(dc_motor_pin1, dc_motor_pin2, servo_pin1)  # RC카 핀, pwm, speed, direct 를 가진 클래스

panel = Panel_Thread()  # RC카의 속도, 방향을 출력해주는 쓰레드
camera = Camera()

panel.daemon = True
camera.daemon = True

try:
    panel.start()
    camera.start()

    while True:
    # Keyboard character retrieval method is called and saved
    # into variable
        
        char = 's'
        char = getch()   
        
        rc_car.doing_cmd(char)
       
        # The "x" key will break the loop and exit the program
        
        if(char == "x"):
            print("Program Ended")
            break
        
        

except Exception as e:
    print("에러 발생")
    print(e)

except KeyboardInterrupt:
    print("종료합니다.")

finally:
    print("finally")
    rc_car.motor.stop()
    gpi.cleanup()
    

