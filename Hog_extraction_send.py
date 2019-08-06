from picamera.array import PiRGBArray
from picamera import PiCamera
import dlib
import cv2
import time
import socket
import io
import numpy
import os
from gtts import gTTS
import openface.openface.align_dlib as openface
import sys
camera = PiCamera()

camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))
rec=cv2.face.LBPHFaceRecognizer_create()
rec.read("/home/pi/Downloads/trainer (14).yml")
predictor_model = "/home/pi/Downloads/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
face_pose_predictor = dlib.shape_predictor(predictor_model)
face_aligner = openface.AlignDlib(predictor_model)
time.sleep(0.1)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.4', 8000))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	img = frame.array
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 0)
	vis = img.copy()
	
	for i, d in enumerate(rects) :
		cv2.rectangle(vis, (d.left(), d.bottom()), (d.right(), d.top()), (0, 255, 0), 2)
		#when a person is detected, the frame number and the order of the person are stored in grayscale

		if not (d.top()>0 and d.bottom()>0 and d.left()>0 and d.right()>0) :
			continue
		pose_landmarks = face_pose_predictor(gray, d)
		alignedFace = face_aligner.align(534, gray, d, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
		result , image = cv2.imencode(".jpg", alignedFace, params=[cv2.IMWRITE_JPEG_QUALITY,100])
		id,conf=rec.predict(alignedFace)
		if(conf < 45):
			cv2.putText(vis, str(id)+" : "+str(round(conf,2)), (d.left(), d.bottom()), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 0))
			
		else:
			cv2.putText(vis, str(id)+" : "+str(round(conf,2)), (d.left(), d.bottom()), cv2.FONT_HERSHEY_PLAIN, 0.9, (0, 0, 255))
			id = 9999
		data = numpy.array(image)
		stringData = data.tostring()
		personal_id = str(id)
		client_socket.sendall((personal_id+(str(len(stringData)))).encode().ljust(16) + stringData)
		
	cv2.imshow("Frame", vis)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
	
	#if no person is detected, continue
	if len(rects) == 0:
		continue

	#exit when ESC is input
	if key == 27:
		cv2.destroyWindow()
		break
