from picamera.array import PiRGBArray
from picamera import PiCamera
import dlib
import cv2
import time
import socket
import struct
import io
import numpy

#count the order of persons in a frame
cnt = 0

camera = PiCamera()

camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))
rec=cv2.face.LBPHFaceRecognizer_create()
rec.read("/home/pi/Downloads/trainer (9).yml")
detector = dlib.get_frontal_face_detector()
time.sleep(0.1)
#count the number of frames which a person has
count = 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.99', 8000))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	img = frame.array
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#gray = cv2.equalizeHist(gray)
	rects = detector(gray, 0)
	vis = img.copy()
	
	for i, d in enumerate(rects) :
		cv2.rectangle(vis, (d.left(), d.bottom()), (d.right(), d.top()), (0, 255, 0), 2)
		cnt = cnt + 1
		#id,conf=rec.predict(gray[y:y+h,x:x+w])
		#cv2.putText(img,str(id),(x,y+h),font,0.45,(0,0,255))
		#when a person is detected, the frame number and the order of the person are stored in grayscale
		result , image = cv2.imencode(".jpg", gray[int(float(d.top())*0.9):int(float(d.bottom())*1.1), int(float(d.left())*0.9):int(float(d.right())*1.1)], params=[cv2.IMWRITE_JPEG_QUALITY,100])
		id,conf=rec.predict(gray[int(float(d.top())*0.9):int(float(d.bottom())*1.1), int(float(d.left())*0.9):int(float(d.right())*1.1)])
		if(conf < 50):
			print(str(id))
		else:
			print('No Match')
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
	else:
		count += 1
		cnt = 0

	#exit when ESC is input
	if key == 27:
		cv2.destroyWindow()
		break

