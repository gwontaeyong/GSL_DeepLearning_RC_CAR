import RPi.GPIO as gpi

class RC_car:
    def __init__(self, motor_pin1, motor_pin2, servo_pin):
        gpi.setmode(gpi.BCM)

        # servo value
        self.center = 7.5  # center value
        self.angle = self.center #value of rc_car
        self.left = 5.5  # left value
        self.right = 9  # right value
        servo_pwm = 50  # servo pwm value
        servo_motor_pin = servo_pin

        # dcmotor value
        self.speed = 0  # dutycycle -> 0 - >  60 ~ 80
        self.max_speed = 50 #maxspeed
        self.min_speed = 20 #차량이 움직일수 있는 최소 dutycycle
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
        self.motor.stop()
        self.servo.stop()
        gpi.cleanup()
        
