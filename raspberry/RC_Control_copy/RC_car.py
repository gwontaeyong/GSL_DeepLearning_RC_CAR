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
        self.max_speed = 100 #maxspeed
        self.min_speed = 60 #차량이 움직일수 있는 최소 dutycycle
        self.dc_pwm = 500  # DCmotor pwm
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
        gpi.cleanup()

