# USAGE
# python pi_facial_landmarks.py

# import the necessary packages
from imutils import face_utils
import dlib
import cv2
import datetime
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
p = "/home/pi/Downloads/install-dlib-example/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
cap = cv2.VideoCapture(0)
cap.set(3,1280) # set Width
cap.set(4,960) # set Height
# load the input image and convert it to grayscale
while True:
	ret, img = cap.read()
	img = cv2.flip(img, -1) # 
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	now = datetime.datetime.now()
	rects = detector(gray, 0)
	# loop over the face detections
	for (i, rect) in enumerate(rects):
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
		for (x, y) in shape:
			cv2.circle(img, (x, y), 2, (0, 255, 0), -1)
	k = cv2.waitKey(3) & 0xff
	cv2.imshow('video',img) # video
    
	if k == 27: # press 'ESC' to quit 
		break

cap.release()
cv2.destroyAllWindows()

