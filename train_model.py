#! /usr/bin/python

from imutils import paths
import face_recognition
import pickle
import cv2
import os
import time
import logging

# logging settings
log_format = "[%(levelname)s] %(asctime)s: %(message)s"
logging.basicConfig(level=logging.INFO, format = log_format)

logging.info("start processing faces...")
imagePaths = list(paths.list_images("dataset"))

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
start_time = time.time()
for (i, imagePath) in enumerate(imagePaths):
	logging.info("processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	# load the input image and convert it from RGB (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb,
		model="hog")

	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)

	# loop over the encodings
	for encoding in encodings:
		knownEncodings.append(encoding)
		knownNames.append(name)
		
proc_time = time.time() - start_time
proc_hour = proc_time // 3600
proc_min = (proc_time % 3600) // 60
proc_sec = (proc_time % 60)
logging.info(f"""takes {proc_hour:.0f} hours {proc_min:.0f} minutes {proc_sec:.0f} seconds 
				to train the model""")

# dump the facial encodings + names to disk
logging.info("serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
