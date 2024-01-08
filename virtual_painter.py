#read webcam
import cv2
import HandTrackingModule as htm
import numpy as np


detector = htm.handDetector()

draw_color =(0,0,255)

img_canvas = np.zeros((720,1280,3),np.uint8)

#read frames from webcam

cap = cv2.VideoCapture(0)

while True:

    success,frame = cap.read()
    frame = cv2.resize(frame,(1280,720))
    frame = cv2.flip(frame,1)  #horizontal ,-1 vertical flip image

    cv2.rectangle(frame,(10,10),(230,100),(0,0,255),cv2.FILLED)
    cv2.rectangle(frame,(240,10),(460,100),(0,255,0),cv2.FILLED)
    cv2.rectangle(frame,(470,10),(690,100),(255,0,0),cv2.FILLED)
    cv2.rectangle(frame,(700,10),(920,100),(255,255,0),cv2.FILLED)
    cv2.rectangle(frame,(930,10),(1270,100),(255,255,255),cv2.FILLED)
    cv2.putText(frame,'ERASER',(1040,70),fontScale=1,fontFace=cv2.FONT_HERSHEY_COMPLEX,color=(0,0,0),thickness=2)

    #Find hand landmarks
    frame = detector.findHands(frame,draw=True)  #to remove lines in hands draw=False
    lmlist = detector.findPosition(frame)  #landmark list

    #print(lmlist)


    if len(lmlist)!=0:
        x1,y1 =lmlist[8][1:]     #index finger cordinates
        x2,y2 = lmlist[12][1:]    #middle finger cordinates

        #print(x1,y1)

    
#check which finger is up      fingerup-1 ,not up -0

        fingers = detector.fingersUp()
        #print(fingers)


#selection mode --- 2 fingers is up
    
        if fingers[1] and fingers[2]:
          #print('Selection mode')
          xp,yp = 0,0  #origin


    #to change the selecting pointer color when arriving each color box

          if y1<100:
             
             if 10<x1<230:
                draw_color =(0,0,255)
                 #print('Red')

             elif 240<x1<460:
                draw_color =(0,255,0)
                #print('Green')

             elif 470<x1<690:
                draw_color =(255,0,0)
                #print('Blue')

             elif 700<x1<920:
                draw_color =(0,255,255)
                #print('Yellow')

             elif 930<x1<1270:
                draw_color=(255,255,255)
                #print('Eraser')


          cv2.rectangle(frame,(x1,y1),(x2,y2),draw_color,thickness=cv2.FILLED) #for selecting thing


#drawing mode - if index finger is up
        if (fingers[1] and not fingers[2]):
          #print('Drawing mode')
          cv2.putText(frame,'Drawing Mode',(1000,500),fontFace=cv2.FONT_HERSHEY_COMPLEX,color=(255,255,0),fontScale=1,thickness=3)
          cv2.circle(frame,(x1,y1),10,draw_color,thickness=-1)

          if xp == 0 and yp ==0:
             xp = x1
             yp = y1

          if draw_color ==(0,0,0):
               cv2.line(frame,(xp,yp),(x1,y1),color=draw_color,thickness=10)
               cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=10)

          else:
               cv2.line(frame,(xp,yp),(x1,y1),color=draw_color,thickness=10)
               cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=10)

          xp,yp = x1,y1
        

    

    #print frame


    #if not get vedio,remove model complex in py


    cv2.imshow('Virtual painter',frame)
    cv2.imshow('Canvas',img_canvas)

    if cv2.waitKey(1) & 0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()
