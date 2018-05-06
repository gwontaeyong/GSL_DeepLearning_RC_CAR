import threading
import socket
import time
import threading
import argparse
from rc_car import RC_car

class CmdClient(threading.Thread):

    def __init__(self, host, port, rc_car):
        super(CmdClient, self).__init__()
        print("make CmdClient")
        self.rc_car = rc_car
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5.0)
        self.server_address = (host, port)
        self.buf_size = 6
        self.flag = True

         
        
    def run(self):
        connection = None
        print("trying to connect with cmd_server")
        try:
            if not connection:
                connection = self.client_socket.connect((self.server_address))
            print("connected with cmd_server")
            #make cmd_rcv thread and start
            self.rcv_thread = threading.Thread(target=self.client_recv)
            self.rcv_thread.start()       
            #main thread to send speed and angle
            self.client_send()        

        except socket.timeout:
            print("cmd_server_timeout")
            self.flag = False 
        
            
            
    def client_send(self):
       
        while self.flag:
            try:
                data = str(self.rc_car.angle)+"_"+str(self.rc_car.speed)
                self.client_socket.send(data.encode())
            except (BrokenPipeError, ConnectionResetError):
                self.flag = False
                break
        

    def client_recv(self):
       
        while self.flag:
            try:
                reply = self.client_socket.recv(self.buf_size).decode()
                if reply == 'q':
                    self.flag = False
                if reply:
                    print("received", reply)
            except socket.timeout:
                pass
            except (BrokenPipeError, ConnectionResetError):
                self.flag = False
                break
        
                    
    def __del__(self):
        print("cmd_client is end")
        self.client_socket.close()
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    #Streaming host, port
    parser.add_argument('-host', type=str, default="192.168.0.37")
    parser.add_argument('-p', type=int, default="8001")
    FLAGS, _ = parser.parse_known_args()

    host = FLAGS.host
    port = FLAGS.p

    dc_motor_pin1 = 19  # DC모터 pwm 사용 pin
    dc_motor_pin2 = 26  # DC모터 pin2
    servo_pin1 = 18  # 서보모터

    #make RC_CAR object
    rc_car = RC_car(dc_motor_pin1, dc_motor_pin2, servo_pin1)  # RC카 핀, pwm, speed, direct 를 가진 클래스
    cmdclient = CmdClient(host, port, rc_car)
    cmdclient.start()

    try:
        while cmdclient.flag:
            pass 
    except KeyboardInterrupt:
        cmdclient.flag = False
    

    