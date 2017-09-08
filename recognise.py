#!/usr/bin/python

from picamera import PiCamera
import time
import io
import pprint
import boto3
import threading
import signal
import sys

done = False

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        done = True
        sys.exit(0)
        
signal.signal(signal.SIGINT, signal_handler)

camera = PiCamera()

W, H = 640, 480

camera.resolution = (W, H)
camera.framerate = 10


class MonitorThread(threading.Thread):
    def run (self):

        camera.start_preview(fullscreen=False, window=(20,20,640,480))
       
        while not done:
          time.sleep(1)



class AnalysisThread(threading.Thread):

    def run (self):
        rekognition = boto3.client('rekognition')

        while not done:
            frame_to_decode = io.BytesIO()

            camera.capture(frame_to_decode, 'jpeg')
            frame_to_decode.seek(0)
            camera.annotate_text = "Detecting..."
            response = rekognition.detect_faces(
                Image={
                    'Bytes': frame_to_decode.read()
                },
                Attributes=["ALL"]
            )
            
            pprint.pprint(response)

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


monitor = MonitorThread()
analyzer = AnalysisThread()
monitor.start()
analyzer.start()
monitor.join()

