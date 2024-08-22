from gpiozero import MotionSensor
from time import sleep
from datetime import datetime

from face_prediction import *
import pygame

pygame.mixer.init()

pir = MotionSensor(4)

try:
	while True:
		pir.wait_for_motion()
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print(f'{now} - Motion detected!')
		
		result = faceRecog()
		
		if result == 'Anita':
			print("It's Anita!")
			pygame.mixer.music.load("/home/anita/Documents/Welcome_Home_Project/welcome_home/welcome_anita.mp3")
			pygame.mixer.music.play()
		elif result == 'WC':
			print("It's WC!")
			pygame.mixer.music.load("/home/anita/Documents/Welcome_Home_Project/welcome_home/welcome_WC.mp3")
			pygame.mixer.music.play()
		else:
			print('You are a stranger!')
			pygame.mixer.music.load("/home/anita/Documents/Welcome_Home_Project/welcome_home/stranger.mp3")
			pygame.mixer.music.play()
		
		sleep(5)
		
except KeyboardInterrupt:
	pass
