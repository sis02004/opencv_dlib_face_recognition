import cv2 as cv
import numpy as np
import time

cap = cv.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
prev = 9
while(True):
    now = time.time()
    sec = now - prev
    prev = now
    fps = 1/(sec)
    ret, img_color = cap.read()
    #img_color = cv.flip(img_color, -1)
    gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
    if ret == False:
        continue;
    cv.imshow('bgr', img_color)
    #cv.imshow('gray', gray)
    print("FPS : "+str(fps))
    if cv.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv.destroyAllWindows()
