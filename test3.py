# USAGE
# python pi_facial_landmarks.py

# import the necessary packages
from imutils import face_utils
import dlib
import cv2
import datetime
import time
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
p = "/home/pi/Downloads/install-dlib-example/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
# load the input image and convert it to grayscale
prev = 0
i = 0
while True:
	ret, img = cap.read()
	print("Video Read : "+str(time.time()))
	img = cv2.flip(img, -1) # 
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	print("Convert Image : "+str(time.time()))
	if(i == 100):
		rects = detector(gray, 0)
		i =0
	# loop over the face detections
		for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)
			(bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
			cv2.rectangle(img, (bX, bY), (bX+bW, bY+bH), (0,255,0),1)
		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
			print("Detect Face : "+str(time.time()))
			cv2.imwrite(str(time.time())+".png", gray[bY:bY+bH,bX:bX+bW])
			print("Extract Face : "+str(time.time()))
	k = cv2.waitKey(3) & 0xff
	cv2.imshow('video',img) # video
	print("Print Video : "+str(time.time()))
	if k == 27: # press 'ESC' to quit 
		break
	i+=1
cap.release()
cv2.destroyAllWindows()

