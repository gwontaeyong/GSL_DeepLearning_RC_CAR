import threading, time
import io
import struct
import socket
import select
import RPi.GPIO as gpi
import picamera
import sys, tty, termios, time
from datetime import datetime

        

class StreamClient(threading.Thread):
    def __init__(self):
        super(StreamClient, self).__init__()
        self.camera = picamera.PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = (320, 240)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.0.37', 8000))
        self.connection = self.client_socket.makefile('wb')

    def run(self):
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (320, 240)      # pi camera resolution
                camera.framerate = 10               # 10 frames/sec
                camera.rotation = 180
                time.sleep(2)                       # give 2 secs for camera to initilize
                start = time.time()
                stream = io.BytesIO()
                
                # send jpeg format video stream
                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                    self.connection.write(struct.pack('<L', stream.tell()))
                    self.connection.flush()
                    stream.seek(0)
                    self.connection.write(stream.read())
                    if time.time() - start > 600:
                        break
                    stream.seek(0)
                    stream.truncate()
            self.connection.write(struct.pack('<L', 0))
        except KeyboardInterrupt:
            print("종료합니다.")
        finally:
            self.connection.close()
            self.client_socket.close()


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


streamclient = StreamClient()

streamclient.daemon = True

try:
    panel.start()
    streamclient.start()

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
    

