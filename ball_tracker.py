#!/usr/bin/env python3

'''
Track a green ball using OpenCV.

    Original: https://raw.githubusercontent.com/simondlevy/OpenCV-Python-Hacks/master/greenball_tracker.py
    modified by Matthew Horoschun to use Raspberry Pi Camera API 

    Copyright (C) 2015 Conan Zhao and Simon D. Levy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as 
    published by the Free Software Foundation, either version 3 of the 
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License 
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import cv2
import numpy as np

# For OpenCV2 image display
IMAGE_WINDOW_NAME = 'Final Image' 
MASK_WINDOW_NAME = 'Mask' 

def track(image):

    '''Accepts BGR image as Numpy array
       Returns: (x,y) coordinates of centroid if found
                (-1,-1) if no centroid was found
                None if user hit ESC
    '''

    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image for only green colors
    lower_green = np.array([37,60,10])
    upper_green = np.array([90,250,220])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)

    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)

    # Assume no centroid
    ctr = (-1,-1)

    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:

        ctr = (centroid_x, centroid_y)

        # Put white circle in at centroid in image
        cv2.circle(image, ctr, 50, (255,255,255), 5)

    # Display full-color image
    cv2.imshow(IMAGE_WINDOW_NAME, image)
    cv2.imshow(MASK_WINDOW_NAME, mask)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None
    
    # Return coordinates of centroid
    return ctr

# Test with input from Raspberry Pi camera
if __name__ == '__main__':

    from picamera.array import PiRGBArray
    from picamera import PiCamera
    import time

    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera,(640,480))
 
    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        image = frame.array

        if not track(image):
                break

        if cv2.waitKey(1) & 0xFF == 27:
            break

        rawCapture.truncate(0)
        rawCapture.seek(0)


