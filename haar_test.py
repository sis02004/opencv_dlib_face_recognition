import numpy as np
import cv2
import datetime
import time
# Cascades 

fourcc = cv2.VideoWriter_fourcc(*'XVID')
faceCascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3,1280) # set Width
cap.set(4,960) # set Height
record = False
prev = 0
while True:
    ret, img = cap.read()
    img = cv2.flip(img, -1) # 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    now = time.time()
    sec = now - prev
    prev = now
    fps = 1/(sec)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    k = cv2.waitKey(3) & 0xff
    cv2.imshow('video',img) # video
    print("FPS : "+str(fps))
    if k == 13:
        print("Start Recording")
        record = True
        video = cv2.VideoWriter("Haar"+str(now)+".avi", fourcc, 10.0, (img.shape[1], img.shape[0]))
    elif k == 32:
        print("Stop Recording")
        record = False
        video.release()
    elif k == 27: # press 'ESC' to quit 
        break
    if record == True:
        print("Recording...")
        video.write(img)
cap.release()
cv2.destroyAllWindows()
