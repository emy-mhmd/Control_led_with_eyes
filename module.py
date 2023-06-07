import cv2 as cv
import numpy as np
import math
import dlib

fonts =cv.FONT_HERSHEY_DUPLEX

# colors
CYAN = (255, 255, 0)
PURPLE = (128, 0, 128)
PINK = (147, 20, 255)
ORANGE = (0, 69, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

 #the detectface is the pretrained face detector object
detectface=dlib.get_frontal_face_detector()

#the predictor is the pre-trained facial landmark predictor object
predictor = dlib.shape_predictor("shape_predictor_81_face_landmarks.dat")



 # return the position of the eye with the color for the detection
def Position(ValuesList):

    maxIndex = ValuesList.index(max(ValuesList))
    posEye = ''
    color = [WHITE, BLACK]
    if maxIndex == 0:
        posEye = "Right"
        color = [BLUE, BLACK]
    elif maxIndex == 1:
        posEye = "Center"
        color = [CYAN, PINK]
    elif maxIndex == 2:
        posEye = "Left"
        color = [PURPLE, BLACK]
   
    return posEye, color

#takes the image and grayscale version and then detect the face using
#pretrained object
def faceDetector(image, gray, Draw=True):
    cordFace1 = (0, 0)
    cordFace2 = (0, 0)
    # getting faces from face detector
    faces = detectface(gray)

    face = None
    # looping through All the face detected.
    for face in faces:
        # getting coordinates of face.
        cordFace1 = (face.left(), face.top())
        cordFace2 = (face.right(), face.bottom())

        # draw rectangle if draw is True.
        if Draw == True:
            cv.rectangle(image, cordFace1, cordFace2, GREEN, 4)
     #image is the camera and the face is the face that is detected now
    return image, face

def facelandmakdetctor(image, gray, face, Draw=True):
    # calling the landmarks predictor
    #returns dlib.full_object_detection object that
    #  represents the detected landmarks.
    landmarks = predictor(gray, face)
    pointList = []

    for n in range(0,landmarks.num_parts):
        point = (landmarks.part(n).x, landmarks.part(n).y)
        # getting x and y coordinates of each mark and adding into list.
        pointList.append(point)
        # draw if draw is True.
        if Draw == True:
            # draw circle on each landmark
            cv.circle(image, point, 3, ORANGE, 1)
    #image is the camera and the face is the face that is detected now  
    return image, pointList



def eyetracking(image, gray, eyePoints):
   dimension=gray.shape
   mask=np.zeros(dimension,dtype=np.uint8)
   #convert the list of eyepoint to numpy array int
   pollypoints=np.array(eyePoints,dtype=np.int32)

   #starting to put the pollypoints in the mask array but with white pixels
   #so here i did the mask to the eye so the eye is white and anything else is 
   #black
   cv.fillPoly(mask,[pollypoints],255)
#anding the gray image and the mask and but it agian in the gray
#so now the gray image have the eye wight and other black
   eyeimage=cv.bitwise_and(gray,gray,mask=mask)
#want to get the max and min of x and y to crop the pic
   maxx=(max(eyePoints,key=lambda iteam:iteam[0]))[0]
   minx=(min(eyePoints,key=lambda iteam:iteam[0]))[0]
   maxy=(max(eyePoints,key=lambda iteam:iteam[1]))[1]
   miny=(min(eyePoints,key=lambda iteam:iteam[1]))[1]
 
 #removes non-eye regions of the image
   eyeimage[mask==0]=255


   cropedeye=eyeimage[miny:maxy,minx:maxx]
#getting the hight and width of the eye
   height,width=cropedeye.shape
#divided the eye int three horizontall region right,left,center
#so to determine the width of each one i divided the width by 3
   divpart=int(width/3)
#converting the gray eye to binary
   ret,thresholdeye=cv.threshold(cropedeye,100,250,cv.THRESH_BINARY)


   rightpart=thresholdeye[0:height,0:divpart]
   centerpart=thresholdeye[0:height,divpart:divpart+divpart]
   leftpart=thresholdeye[0:height,divpart+divpart:width]

#counts the black pixels
   rightblackpx=np.sum(rightpart==0)
   centerblackpx=np.sum(centerpart==0)
   leftblackpx=np.sum(leftpart==0)

   pos,color=Position([rightblackpx,centerblackpx,leftblackpx])
 
   return pos,color


