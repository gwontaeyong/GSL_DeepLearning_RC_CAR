import threading, time
import RPi.GPIO as gpi
import picamera
import argparse
import sys, tty, termios, time, select

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

    # left_
    def turn_left(self):
        if (self.angle <= self.left):
            self.angle = self.left
        else:
            self.angle -= 0.5
        self.servo.ChangeDutyCycle(self.angle)

    # right_
    def turn_right(self):
        if(self.angle >= self.right):
            self.angle = self.right
        else:
            self.angle += 0.5
        self.servo.ChangeDutyCycle(self.angle)        

    # straight
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
        

#capture class
class Capture(threading.Thread):
    def __init__(self,path, time ):
        super(Capture, self).__init__()
        global rc_car
        self.camera = picamera.PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = (320, 240)
        self.pause_time = time
        self.path = path
    def run(self):
        while True:
            #print("speed : ", rc_car.speed, "direct : ", rc_car.angle)
            self.camera.capture(self.path)
            time.sleep(self.pause_time)
            
#show RC_CAR's status 
class Panel_Thread(threading.Thread):

    def __init__(self):
        super(Panel_Thread, self).__init__()
        global rc_car
        print("Panel_Thread start")

    def run(self):
        while True:
            print("speed : ", rc_car.speed, "direct : ", rc_car.angle)
            time.sleep(1)

    def __del__(self):
        print('판넬 종료')

#get commend
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch

if __name__ == "__main__":
    
    #get parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=str)
    FLAGS, _ = parser.parse_known_args()

    path = FLAGS.path

    #set GPIO pin for DC, Servo Motor
    dc_motor_pin1 = 19  # DC모터 pwm 사용 pin
    dc_motor_pin2 = 26  # DC모터 pin2
    servo_pin1 = 18  # 서보모터

    #make RC_CAR object
    rc_car = RC_car(dc_motor_pin1, dc_motor_pin2, servo_pin1)  # RC카 핀, pwm, speed, direct 를 가진 클래스

    #make Thread panel, camera
    panel = Panel_Thread()  
    camera = Capture(path, 1)

    panel.daemon = True
    camera.daemon = True

    #get command from keyboard
    # 8 : speed_up 
    # 5 : speed_down 
    # 4 : left
    # 6 : right
    try:
        panel.start()
        camera.start()

        while True:
        
            char = getch()   
            
            rc_car.doing_cmd(char)
                    
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
        