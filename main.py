import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import serial
import math

#Assigning variables to real world values for a precise estimation
webcam_focal_length = 1849 #This is specific to my webcam so change it with further instructions in the README
interpupilary_distance = 6.5 #This is specific to my eyes so change it with further instructions in the README (in cm)

#Measured lengths of the robot arm 
UF = 8 #Upper arm servo pivot to forearm servo pivot
FG = 14.2 #Forearm servo to gripper tip 

base_options = python.BaseOptions(model_asset_path=r'D:\Github\Automatic-snack-feeder\face_landmarker.task') # 'r' means treat  the path as a raw string to '\n' is ignored if it is in the path. 

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=1,min_face_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

face_landmarker = vision.FaceLandmarker.create_from_options(options)

#Establish serial connection
ser = serial.Serial('COM3', 115200)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Unable to open camera")
try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Unable to recieve the frame")
            break

        #Converting frame for mediapipe        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image_object = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        #Running detection
        results = face_landmarker.detect(mp_image_object)

        #Checking for a face
        if results.face_landmarks:
            #Getting the mouth landmark(13)
            mouth_x = results.face_landmarks[0][13].x
            mouth_y = results.face_landmarks[0][13].y

            #Calculating user distance based on the measurements of the eye locations
            right_eye_x = results.face_landmarks[0][263].x
            left_eye_x = results.face_landmarks[0][33].x
            pixel_eye_distance = (right_eye_x - left_eye_x) * 1280
            distance = (interpupilary_distance * webcam_focal_length) / pixel_eye_distance

            #Warning if the user is too far away in order to prevent a math error
            if distance > (UF + FG):
                print("Please get closer!")
                continue

            #Calcuating angles using the cosine law (see README)
            elbow_angle = math.degrees(math.acos((UF**2 + FG**2 - distance**2) / (2 * UF  * FG)))
            shoulder_angle = math.degrees(math.acos((UF**2 + distance**2 - FG**2) / (2 * UF * distance)) )



            #Convert x and y values to pan and tilt 
            pan = int(np.interp(mouth_x, (0,1), (180, 0))) #Inverting x 
            tilt = int(np.interp(mouth_y, (0,1), (180, 0))) #Inverting y

            print(pan,tilt)

            #Format the pan and tilt values for serial communication
            message = f"{str(pan)},{str(tilt)}\n".encode()


            #Send the values to the ESP32
            ser.write(message)

        cv2.imshow('Video Feed', frame)

        #Ends the camera feed if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            print("Exiting...")
            break 

finally:
    ser.close()
    cap.release()
    cv2.destroyAllWindows()