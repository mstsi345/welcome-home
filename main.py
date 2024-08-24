from gpiozero import MotionSensor
from time import sleep
from datetime import datetime
import pygame

from face_prediction import *
from dbWrapper import DBWrapper

pygame.mixer.init()
db = DBWrapper()

pir = MotionSensor(4)

try:
	while True:
		pir.wait_for_motion()
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print(f'{now} - Motion detected!')
		
		# save to DB
		result = faceRecog()
		pred_result = result['pred_result']
		confidence = result['confidence']
		db.insert_data(pred_result=pred_result, confidence=confidence, act_result='')
		
		# play corresponding sound effect
		if pred_result == 'Anita':
			print("It's Anita!")
			pygame.mixer.music.load("/home/anita/Documents/Welcome_Home_Project/welcome_home/welcome_anita.mp3")
			pygame.mixer.music.play()
		elif pred_result == 'WC':
			print("It's WC!")
			pygame.mixer.music.load("/home/anita/Documents/Welcome_Home_Project/welcome_home/welcome_WC.mp3")
			pygame.mixer.music.play()
		elif pred_result == 'Unknown':
			print('You are a stranger!')
			pygame.mixer.music.load("/home/anita/Documents/Welcome_Home_Project/welcome_home/stranger.mp3")
			pygame.mixer.music.play()
		else:
			print('No face is detected!')
		
		sleep(5)
		
except KeyboardInterrupt:
	pass
