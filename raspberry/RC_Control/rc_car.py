import RPi.GPIO as gpi

class RC_car:
    def __init__(self, motor_pin1, motor_pin2, servo_pin):
        gpi.setmode(gpi.BCM)

        # servo value
        self.ANGLES = [5.6, 6.0, 6.4, 6.8, 7.2, 7.6, 8.0, 8.4, 8.6]
        self.center = 4  # center value
        self.angle = 4 #value of rc_car
        self.left = 0  # left value
        self.right = len(self.ANGLES)-1  # right value
        
        

        servo_pwm = 50  # servo pwm value
        servo_motor_pin = servo_pin

        # dcmotor value
        self.speed = 0  # dutycycle -> 0 - >  60 ~ 80
        self.max_speed = 50 #maxspeed
        self.min_speed = 10 #차량이 움직일수 있는 최소 dutycycle
        self.speed_rate = 3

        dc_pwm = 15  # DCmotor pwm
        dc_motor_pin1 = motor_pin1
        dc_motor_pin2 = motor_pin2

        # 핀 아웃 설정
        gpi.setup(dc_motor_pin1, gpi.OUT)
        gpi.setup(dc_motor_pin2, gpi.OUT)
        gpi.setup(servo_motor_pin, gpi.OUT)

        # DC모터,SERVO모터 생성
        gpi.output(dc_motor_pin2, False)
        self.servo = gpi.PWM(servo_motor_pin, servo_pwm)
        self.motor = gpi.PWM(dc_motor_pin1, dc_pwm)
        
        # DC모터, SERVO모터 실행
        self.motor.start(self.speed) #speed 0으로 모터 시작
        self.servo.start(self.ANGLES[self.angle]) #centor 로 서보모터 시작
        
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
            self.servo.ChangeDutyCycle(self.ANGLES[self.angle])
            self.motor.ChangeDutyCycle(self.speed)

    # left_
    def turn_left(self):

        self.angle -= 1
        
        if (self.angle <= self.left):
            self.angle = self.left
        
        self.servo.ChangeDutyCycle(self.ANGLES[self.angle])

    # right_
    def turn_right(self):

        self.angle += 1

        if(self.angle >= self.right):
            self.angle = self.right
            
        self.servo.ChangeDutyCycle(self.ANGLES[self.angle])        

    # straight
    def turn_center(self):
        self.angle = self.center
        self.servo.ChangeDutyCycle(self.angle)

    
    def speed_up(self):
        
        if self.speed == 0:
            self.speed = self.min_speed
        else:
            self.speed += self.speed_rate

        if self.speed > self.max_speed:
            self.speed = self.max_speed

        self.motor.ChangeDutyCycle(self.speed)

    def speed_down(self):

        self.speed -= self.speed_rate

        if self.speed < self.min_speed:
            self.speed = 0

        self.motor.ChangeDutyCycle(self.speed)

    def __del__(self):
        print("DC Motor del")
        self.motor.stop()
        self.servo.stop()
        gpi.cleanup()