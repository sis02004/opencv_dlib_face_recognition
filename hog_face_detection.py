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
    img = cv2.flip(img, -1) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    now = datetime.datetime.now()
    # loop over the face detections
    for rect in rects:
	(bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
	cv2.rectangle(img, (bX, bY), (bX + bW, bY + bH), (0, 255, 0), 1)
	shape = predictor(gray, rect)
	shape = face_utils.shape_to_np(shape)
    k = cv2.waitKey(3) & 0xff
    cv2.imshow('video',img) # video
    if k == 27: # press 'ESC' to quit 
        break
cap.release()
cv2.destroyAllWindows()
