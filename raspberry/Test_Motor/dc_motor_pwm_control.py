import RPi.GPIO as gpi
import sys
import time


gpi.setmode(gpi.BCM)


pin = 26  # DC모터
pin_pwm = 19  # DC모터
pwm = 500 #원래
pwm = 15

gpi.setup(pin, gpi.OUT)
gpi.setup(pin_pwm, gpi.OUT)


gpi.output(pin, False)
motor_1 = gpi.PWM(pin_pwm, pwm)
motor_1.start(0)

print("motor start")

try:
    while True:
        pwm = int(input("input"))
        motor_1.ChangeDutyCycle(pwm)
finally:
    motor_1.stop()
    gpi.cleanup()
    sys.exit()