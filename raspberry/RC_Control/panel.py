<<<<<<< HEAD
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
=======
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
>>>>>>> 9bf5a7977fb5d85d3d0cf55790e78db2b33f8128
        print('Panel del')