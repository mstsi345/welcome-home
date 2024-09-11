
from picamera2 import Picamera2
from gpiozero import MotionSensor
from time import sleep
from datetime import datetime

name = 'Anita' #replace with your name

picam = Picamera2()
picam.resolution = (512, 304)
now = datetime.now().strftime('%Y%m%d_%H%M%S')

# take pictures
picam.start_and_capture_files(f'./dataset/{name}/{now}_'+'{:03d}.png',
    num_files=30, initial_delay=3, delay=1)
    
sleep(3)

picam.close()
