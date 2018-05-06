import threading
import socket
import time
import picamera
import struct
import io
import sys, tty, termios, time, select
import argparse

class StreamClient(threading.Thread):
    def __init__(self, host , port):
        super(StreamClient, self).__init__()
        print("make StreamClient")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5)
        self.camera = picamera.PiCamera()
        self.camera.resolution = (320, 240)      # pi camera resolution
        self.camera.framerate = 10               # 10 frames/sec
        self.camera.rotation = 180               # reversre
        self.flag = True
        self.host = host
        self.port = port
        
        time.sleep(2)
        print("camera Setting is done")

    def run(self):
        connection = None
        try:
            print("trying to connect with streamming_server")
            if not connection :
                connection = self.client_socket.connect((self.host, self.port))
            print(" connected with streamming_server")
            send_image = self.client_socket.makefile('wb')
            stream = io.BytesIO()

            for foo in self.camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                try:
                    if not self.flag :
                        send_image.write(struct.pack('<L', 0))  
                        send_image.close()                
                        break

                    send_image.write(struct.pack('<L', stream.tell()))
                    send_image.flush()
                    stream.seek(0)
                    send_image.write(stream.read())
                    stream.seek(0)
                    stream.truncate()

                except (BrokenPipeError, ConnectionResetError):
                    print("connection with streaming_server is broken")
                    self.flag = False
                    break
                      
            self.camera.close()
            self.client_socket.close()       
            
        except socket.timeout:
            print("streaming_server_timeout")
            self.flag = False                  
            self.camera.close()

        

    def __del__(self):
        print("StreamClient end")

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-shost', type=str, default="192.168.0.37")
    parser.add_argument('-sp', type=int, default="8002")
    FLAGS, _ = parser.parse_known_args()

    shost = FLAGS.shost
    sport = FLAGS.sp
    
    streaming_client = StreamClient(shost, sport)
    streaming_client.start()

    try:
        while True:
            if not streaming_client.flag:
                break
            pass
    except KeyboardInterrupt:
        streaming_client.flag = False
    finally:
        print("program is end")
  