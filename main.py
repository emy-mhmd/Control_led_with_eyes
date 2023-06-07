import cv2 as cv
import numpy as np
import module as m
import time
import serial
# import usb.core





ser = serial.Serial(port='COM3', baudrate=9600)
time.sleep(2)

# creating camera object
camera = cv.VideoCapture(0)






while True:
   
    ret, frame = camera.read()
    if ret == False:
        break

    # converting frame into Gry image.
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    height, width = grayFrame.shape
  
    # calling the face detector funciton
    image, face = m.faceDetector(frame, grayFrame)
    if face is not None:

        # calling landmarks detector funciton.
        image, Pointarray = m.facelandmakdetctor(frame, grayFrame, face, True)
      

      
        Righteye = Pointarray[36:42]
        Lefteye = Pointarray[42:48]
       
        position, coloright = m.eyetracking(frame, grayFrame, Righteye)
        positionleft, colorleft = m.eyetracking(
            frame, grayFrame, Lefteye)
        

        if position == "Right":
             ser.write(b'1')  # Send signal for right lead
        elif position == "Left":
             ser.write(b'2')  # Send signal for left lead
        elif position == "Center":
             ser.write(b'3')

        # draw background as line where we put text.
        cv.line(image, (30, 90), (100, 90), coloright[0], 30)
        cv.line(image, (25, 50), (135, 50), m.WHITE, 30)
        cv.line(image, (int(width-150), 50), (int(width-45), 50), m.WHITE, 30)
        cv.line(image, (int(width-140), 90),
                (int(width-60), 90), colorleft[0], 30)

        # writing text on above line
        cv.putText(image, f'{position}', (35, 95), m.fonts, 0.6, coloright[1], 2)
        cv.putText(image, f'{positionleft}', (int(width-140), 95),
                   m.fonts, 0.6, colorleft[1], 2)
        cv.putText(image, f'Right Eye', (35, 55), m.fonts, 0.6, coloright[1], 2)
        cv.putText(image, f'Left Eye', (int(width-145), 55),
                   m.fonts, 0.6, colorleft[1], 2)

        # showing the frame on the screen
        cv.imshow('Frame', image)
    else:
        cv.imshow('Frame', frame)


    key = cv.waitKey(1)

    # if q is pressed on keyboard: quit
    if key == ord('q'):
        break
# closing the camera
camera.release()

# closing  all the windows
cv.destroyAllWindows()               