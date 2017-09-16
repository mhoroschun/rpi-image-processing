# ltc-yr11-face
LTC Year 11 Face Detection/Recognition using OpenCV and AWS Rekognition

Before you begin - you'll need the OpenCV libraries installed. Packages
for Raspberry Pi Raspbian (stretch) are available here:

    

detect_opencv.py     - Basic example of using OpenCV with Haar Cascade
                       to do face/eye detection.

recognise_opencv.py  - A modified version of the detect_opencv with the
                       starting point for doing face recognition. Not
                       working yet!

recognise_aws.py     - Example of using AWS Rekognition to do more 
                       advanced face recognition in the 'cloud'. This
                       script needs an AWS account to work.

ball_tracker.py      - Example of simple threshold-based ball tracking
                       Update HSV threshold depending on colour of the
                       ball.

Things to try:

  * Histogram Backprojection - So your robot could say:

          "Show me the ball"

      You show the robot the ball, it captures a histogram and then
      uses it to track the ball using backprojection

      http://docs.opencv.org/3.1.0/dc/df6/tutorial_py_histogram_backprojection.html

  * Hough Circle Detection

      Might this be better? Not as depdendent on good lighting?

      Could this be used to improve the accuracy of the HSV-threshold method? or the
      Histogram Backprojection method? 

      http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html
      http://opencvexamples.blogspot.com/2013/10/hough-circle-detection.html
      http://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
      
