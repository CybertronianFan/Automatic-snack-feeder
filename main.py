import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import serial


base_options = python.BaseOptions(model_asset_path=r'D:\Github\Automatic-snack-feeder\face_landmarker.task') # 'r' means treat  the path as a raw string to '\n' is ignored if it is in the path. 

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=1,
    min_face_detection_confidence=0.7,
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
            x = results.face_landmarks[0][13].x
            y = results.face_landmarks[0][13].y

            #Convert x and y values to pan and tilt 
            pan = int(np.interp(x, (0,1), (180, 0))) #Inverting x 
            tilt = int(np.interp(y, (0,1), (0, 180)))
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