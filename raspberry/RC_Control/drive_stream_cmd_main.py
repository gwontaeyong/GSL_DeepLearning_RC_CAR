from rc_car import RC_car
from panel import Panel_Thread
from streaming_client import StreamClient
from cmd_client import CmdClient

import sys, tty, termios, time, select
import argparse
import datetime

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
    #Streaming host, port
    parser.add_argument('-shost', type=str, default="192.168.0.37")
    parser.add_argument('-sp', type=int, default="8002")
    parser.add_argument('-chost', type=str, default="192.168.0.37")
    parser.add_argument('-cp', type=int, default="8001")
    FLAGS, _ = parser.parse_known_args()

    shost = FLAGS.shost
    sport = FLAGS.sp
    chost = FLAGS.chost
    cport = FLAGS.cp


    #set GPIO pin for DC, Servo Motor
    dc_motor_pin1 = 19  # DC모터 pwm 사용 pin
    dc_motor_pin2 = 26  # DC모터 pin2
    servo_pin1 = 18  # 서보모터

    #make RC_CAR object
    rc_car = RC_car(dc_motor_pin1, dc_motor_pin2, servo_pin1)  # RC카 핀, pwm, speed, direct 를 가진 클래스

    #make Thread panel, streaming client
    #panel = Panel_Thread(rc_car)  
    streaming_client = StreamClient(shost, sport)
    cmd_client = CmdClient(chost, cport, rc_car)

    #get command from keyboard
    # 8 : speed_up 
    # 5 : speed_down 
    # 4 : left
    # 6 : right
    try:
        #panel.start()
        streaming_client.start()
        cmd_client.start()

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
        #thread ending
        #panel.flag = False
        streaming_client.flag = False
        cmd_client.flag = False
        