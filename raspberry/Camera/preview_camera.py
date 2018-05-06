import picamera
import time

cam = picamera.PiCamera()
cam.resolution = (320,240)
cam.rotation = 180
cam.start_preview()

try:
    while True:
        print("camping")
except KeyboardInterrupt:
    cam.stop_preview()

