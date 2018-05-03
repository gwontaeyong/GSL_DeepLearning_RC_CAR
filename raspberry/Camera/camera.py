import time
import picamera
 
with picamera.PiCamera() as camera:
    
    camera.rotation = 180
    camera.capture('./image.jpg')
