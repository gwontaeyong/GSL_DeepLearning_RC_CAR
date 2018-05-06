import RPi.GPIO as gpi
import sys
import time


gpi.setmode(gpi.BCM)
servo_pin = 18  # 서보모터

gpi.setup(servo_pin, gpi.OUT)

servo = gpi.PWM(servo_pin, 50)
servo.start(7.5)

print("motor start")

try:
    while True:
        pwm = float(input("input"))
        servo.ChangeDutyCycle(pwm)
        if pwm == 0:
            break
finally:
    servo.stop()
    gpi.cleanup()

#	sys.exit()
