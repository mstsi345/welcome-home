#! /usr/bin/python

# import the necessary packages
from imutils.video import FPS
from picamera2 import Picamera2, Preview
import face_recognition
import imutils
import pickle
import time
import cv2
from datetime import datetime, timedelta
import logging

# logging settings
log_format = "[%(levelname)s] %(asctime)s: %(message)s"
logging.basicConfig(level=logging.INFO, format = log_format)

def faceRecog():

	currentname = "unknown"
	encodingsP = "encodings.pickle"

	logging.info("loading encodings + face detector...")
	data = pickle.loads(open(encodingsP, "rb").read())

	# initialize the video stream and allow the camera sensor to warm up
	picam = Picamera2()
	config = picam.create_preview_configuration({'format': 'RGB888'})
	picam.configure(config)
	# picam.start_preview(Preview.DRM)
	picam.start()
	fps = FPS().start()
	
	# time.sleep(2.0)
	time_start = datetime.now()

	name_hist = []
	while True:
		# grab the frame from the threaded video stream and resize it
		# to 500px (to speedup processing)
		frame = picam.capture_array()
		frame = imutils.resize(frame, width=500)

		boxes = face_recognition.face_locations(frame)
		encodings = face_recognition.face_encodings(frame, boxes)
		names = []

		for encoding in encodings:
			matches = face_recognition.compare_faces(data["encodings"],
				encoding)
			name = "Unknown" #if face is not recognized, then print Unknown

			if True in matches:

				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				# loop over the matched indexes and maintain a count for
				# each recognized face
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

				# determine the recognized face with the largest number
				# of votes (note: in the event of an unlikely tie Python
				# will select first entry in the dictionary)
				name = max(counts, key=counts.get)

				if currentname != name:
					currentname = name
					print(currentname)

			names.append(name)
			name_hist.append(name)

		# loop over the recognized faces to annotate the name
		for ((top, right, bottom, left), name) in zip(boxes, names):
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 225), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				.8, (0, 255, 255), 2)

		cv2.imshow("Facial Recognition is Running", frame)
		key = cv2.waitKey(1) & 0xFF
			
		if datetime.now() > time_start + timedelta(seconds=5):
			# cleanup
			fps.stop()
			picam.close()
			# picam.stop_preview()
			cv2.destroyAllWindows()
			
			logging.info(name_hist)
			final_result = max(name_hist, key=lambda x: name_hist.count(x)) if name_hist else 'None'
			confidence = name_hist.count(final_result)/len(name_hist) if name_hist else float(0)
			logging.info(f"final_result: {final_result}, confidence: {confidence}")
			
			return {'pred_result': final_result, 'confidence': confidence}
			
		# update the FPS counter
		fps.update()


