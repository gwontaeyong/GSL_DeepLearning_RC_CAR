import threading, time
import socket
import select
import RPi.GPIO as gpi
import RC_car
import Panel_Thread
import TCP_Thread

'''
RC_car

servo pin = 18

servo = center = 7.5 
letf = 5
right = 10

motor pin = 19, 26
'''


key = 'g'
dc_motor_pin1 = 19  # DC모터 pwm 사용 pin
dc_motor_pin2 = 26  # DC모터 pin2
servo_pin1 = 18  # 서보모터


host = '192.168.0.37'  # 서버 주소
port = 8001  # 서버 연겨 포트

rc_car = RC_car.RC_car(dc_motor_pin1, dc_motor_pin2, servo_pin1)  # RC카 핀, pwm, speed, direct 를 가진 클래스

panel = Panel_Thread.Panel_Thread()  # RC카의 속도, 방향을 출력해주는 쓰레드
tcp_thread = TCP_Thread.TCP_Thread(host, port)

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
    panel.flag = False
    tcp_thread.flag = False

finally:
    print("finally")
    rc_car.motor.stop()
    tcp_thread.client_socket.close()
