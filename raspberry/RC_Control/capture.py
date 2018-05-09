<<<<<<< HEAD
import picamera
import threading
import time
import os
from datetime import datetime

class Capture(threading.Thread):

    def __init__(self, path, time, rc_car ):
        super(Capture, self).__init__()
        print("capture start")
        #make camera object
        self.camera = picamera.PiCamera()
        #setting camera
        self.camera.rotation = 180 #rotate 180
        self.camera.resolution = (320, 240)#make picture size to 240x320
        self.pause_time = time #interval time
        self.is_dir(path)
        self.path = path # path the data be stored
        self.flag = True #thread flag
        self.rc_car = rc_car

    def run(self):
        while self.flag:
            get_filename = datetime.today().strftime("date_%H:%M:%S_streering_")+str(self.rc_car.angle)+"_speed_"+str(self.rc_car.speed)+".jpg"
            filepath = os.path.join(self.path, get_filename)
            #print("speed : ", rc_car.speed, "direct : ", rc_car.angle)
            self.camera.capture(filepath)
            time.sleep(self.pause_time)
    
    def is_dir(self, path):
        if not os.path.isdir("./" + path + "/"):
            os.mkdir("./" + path + "/")
    
    def __del__(self):
=======
import picamera
import threading
import time
import os
from datetime import datetime

class Capture(threading.Thread):

    def __init__(self, path, time, rc_car ):
        super(Capture, self).__init__()
        print("capture start")
        #make camera object
        self.camera = picamera.PiCamera()
        #setting camera
        self.camera.rotation = 180 #rotate 180
        self.camera.resolution = (320, 240)#make picture size to 240x320
        self.pause_time = time #interval time
        self.is_dir(path)
        self.path = path # path the data be stored
        self.flag = True #thread flag
        self.rc_car = rc_car

    def run(self):
        while self.flag:
            get_filename = datetime.today().strftime("date_%H:%M:%S_streering_")+str(self.rc_car.angle)+"_speed_"+str(self.rc_car.speed)+".jpg"
            filepath = os.path.join(self.path, get_filename)
            #print("speed : ", rc_car.speed, "direct : ", rc_car.angle)
            self.camera.capture(filepath)
            time.sleep(self.pause_time)
    
    def is_dir(self, path):
        if not os.path.isdir("./" + path + "/"):
            os.mkdir("./" + path + "/")
    
    def __del__(self):
>>>>>>> 9bf5a7977fb5d85d3d0cf55790e78db2b33f8128
        print("capture end")