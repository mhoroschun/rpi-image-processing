#!/usr/bin/python3

from picamera import PiCamera
import time
import io
import pprint
import boto3

camera = PiCamera()

W, H = 640, 480

camera.resolution = (W, H)
camera.framerate = 10

camera.start_preview(fullscreen=False, window=(20,20,640,480))
       
rekognition = boto3.client('rekognition')

while True:
    
    camera.annotate_text = "Detecting..."

    frame_to_decode = io.BytesIO()
    camera.capture(frame_to_decode, 'jpeg')
    frame_to_decode.seek(0)

    # Send to AWS Rekognition to detect faces.
    response = rekognition.detect_faces(
        Image={
            'Bytes': frame_to_decode.read()
        },
        Attributes=["ALL"]
    )
    
    # Print out API response to console        
    pprint.pprint(response)

    # Select out some attributes and display them on the screen
    if response and response['FaceDetails'] and response['FaceDetails'][0]:
        camera.annotate_text = (
            str(response['FaceDetails'][0]['AgeRange']['Low']) + " - " +
            str(response['FaceDetails'][0]['AgeRange']['High']) + " year old " +
            response['FaceDetails'][0]['Gender']['Value']
        )
        if response['FaceDetails'][0]['Emotions'][0]:
            camera.annotate_text += (
                "(" + response['FaceDetails'][0]['Emotions'][0]['Type'] + ")"
            )
    else:
        camera.annotate_text = "Is anyone there?"

    time.sleep(1)


