<<<<<<< HEAD
from rc_car import RC_car
from panel import Panel_Thread
from capture import Capture
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
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
    parser.add_argument('-path', type = str, default = nowDate)
    FLAGS, _ = parser.parse_known_args()

    path = FLAGS.path

    #set GPIO pin for DC, Servo Motor
    dc_motor_pin1 = 19  # DC모터 pwm 사용 pin
    dc_motor_pin2 = 26  # DC모터 pin2
    servo_pin1 = 18  # 서보모터

    #make RC_CAR object
    rc_car = RC_car(dc_motor_pin1, dc_motor_pin2, servo_pin1)  # RC카 핀, pwm, speed, direct 를 가진 클래스

    #make Thread panel, camera
    panel = Panel_Thread(rc_car)  
    camera = Capture(path, 1, rc_car)

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
                del rc_car
                break
    
    except Exception as e:
        print("에러 발생")
        print(e)

    except KeyboardInterrupt:
        print("종료합니다.")

    finally:
        #thread ending
        panel.flag = False
=======
from rc_car import RC_car
from panel import Panel_Thread
from capture import Capture
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
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
    parser.add_argument('-path', type = str, default = nowDate)
    FLAGS, _ = parser.parse_known_args()

    path = FLAGS.path

    #set GPIO pin for DC, Servo Motor
    dc_motor_pin1 = 19  # DC모터 pwm 사용 pin
    dc_motor_pin2 = 26  # DC모터 pin2
    servo_pin1 = 18  # 서보모터

    #make RC_CAR object
    rc_car = RC_car(dc_motor_pin1, dc_motor_pin2, servo_pin1)  # RC카 핀, pwm, speed, direct 를 가진 클래스

    #make Thread panel, camera
    panel = Panel_Thread(rc_car)  
    camera = Capture(path, 1, rc_car)

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
                del rc_car
                break
    
    except Exception as e:
        print("에러 발생")
        print(e)

    except KeyboardInterrupt:
        print("종료합니다.")

    finally:
        #thread ending
        panel.flag = False
>>>>>>> 9bf5a7977fb5d85d3d0cf55790e78db2b33f8128
        camera.flag = False