from imutils import face_utils
import dlib
import numpy as np
import cv2
import datetime

cap = cv2.VideoCapture(0)
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
record = False
while True:
    flag = False
    ret, img = cap.read()
    org = img
    org = cv2.flip(org,-1)
    img = cv2.flip(img, -1) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    now = datetime.datetime.now()
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
		cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
		
    k = cv2.waitKey(3) & 0xff
    cv2.imshow('video',img) # video
    if k == 27: # press 'ESC' to quit 
        break
    if flag == True:
        print("saved")
        cv2.imwrite("/home/pi/project/detect/byungjun/byungjun_hog/byungjun_hog"+str(now)+".png", org);
    
cap.release()
cv2.destroyAllWindows()
