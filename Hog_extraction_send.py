from imutils import face_utils
import dlib
import cv2
import datetime
import time
import socket
import struct
import io
import numpy

p = "/home/pi/Downloads/install-dlib-example/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
# load the input image and convert it to grayscale
prev = 0
i = 0
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.99', 8000))
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]

while True:
	ret, img = cap.read()
	img = cv2.flip(img, -1) # 
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	rects = detector(gray, 0)
	for rect in rects:
		
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)
		(bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
		
		cv2.rectangle(img, (bX, bY), (bX+bW, bY+bH), (0,255,0),1)
		image = gray[bY:bY+bH,bX:bX+bW]
		result , image = cv2.imencode('.jpg', image, encode_param)
		data = numpy.array(image)
		stringData = data.tostring()
		
		client_socket.sendall((str(len(stringData))).encode().ljust(16) + stringData)
		
		
	k = cv2.waitKey(3) & 0xff
	cv2.imshow('video',img) # video
	print("Print Video : "+str(time.time()))
	if k == 27: # press 'ESC' to quit 
		break

cap.release()
cv2.destroyAllWindows()

