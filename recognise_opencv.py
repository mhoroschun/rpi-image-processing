#!/usr/bin/python3
from picamera.array import PiRGBArray
from picamera import PiCamera

import time
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml')

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.face.createLBPHFaceRecognizer()

# Init the camera and grab a ref to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera,(640,480))

# Allow Camera to Warm up
time.sleep(0.1)

trained_faces = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #check_face_images = []
    for (x,y,w,h) in faces:
        #print(x,y,w,h)
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]
        #check_face_images.append(roi_color)

        if trained_faces == 0:
            recognizer.train([roi_gray], np.array([trained_faces]))
            trained_faces += 1
        else:
            nbr_predicted,conf = recognizer.predict(roi_gray)
            print('Person {}, conf: {}'.format(nbr_predicted,conf))
        
        #eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in eyes:
        #    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    
    #i = 0
    #for face in alltime_faces:
        
    #    i += 1
    #    cv2.imshow("Face " + str(i), face)
    
    cv2.imshow("Frame", image)

    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)
    rawCapture.seek(0)

    if key == ord("q"):
        break

cv2.destroyAllWindows()

