import threading
import time

#show RC_CAR's status 
class Panel_Thread(threading.Thread, ):

    def __init__(self, rc_car):
        super(Panel_Thread, self).__init__()
        self.rc_car = rc_car
        self.flag = True
        print("Panel_Thread start")

    def run(self):
        while self.flag:
            print("speed : ", self.rc_car.speed, "direct : ", self.rc_car.angle)
            time.sleep(1)

    def __del__(self):
        print('Panel del')