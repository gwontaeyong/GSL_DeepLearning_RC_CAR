
import time
import picamera
from datetime import datetime

with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    date = datetime.today().strftime("%m:%d_%H_%M_%S")
    #+str(rc_car.angle)+"_"+str(rc_car.speed)
    path = "/home/GSL/raspberry/images/"+date+".jpg"
    camera.capture(path)