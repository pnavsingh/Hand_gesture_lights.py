import cv2
import time
from cv2 import FILLED
import numpy as np
import handtrackingmodule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import asyncio
import msvcrt
from kasa import SmartBulb


lower = SmartBulb("IP address of bottom light") #kasa bottom ip 
upper = SmartBulb("Ip address of upper") #kasa top ip
#(0,0,100) default color scheme
#loop.run_until_complete(upper.update())
#loop.run_until_complete(lower.update())

loop = asyncio.get_event_loop() #import otherwise using run would cause event loop closed errors

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)








while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw = False)
    if len(lmlist) != 0:
        #print(lmlist[4],lmlist[8])
        x1, y1 = lmlist[4][1],lmlist[4][2]
        x2, y2 = lmlist[8][1],lmlist[8][2]
        x3,y3 = lmlist[12][1],lmlist[12][2]
        x4,y4 = lmlist[20][1],lmlist[20][2]


        cx,cy = (x1+x2)//2, (y1+y2)//2 #this finds the median
        cx1,cy1= (x1+x3)//2, (y1+y3)//2
        cx2,cy2 = (x1+x4)//2, (y1+y4)//2 

        cv2.circle(img, (x1,y1), 15 ,(255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15 ,(255,0,255), cv2.FILLED)
        cv2.circle(img, (x3,y3), 15 ,(255,0,255), cv2.FILLED)
        cv2.circle(img, (x4,y4), 15 ,(255,0,255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),1)
        cv2.line(img,(x1,y1),(x3,y3),(255,0,255),1)
        cv2.line(img,(x1,y1),(x4,y4),(255,0,255),1)
        #cv2.circle(img, (cx,cy), 15 ,(255,0,255), cv2.FILLED)
        lengthi = math.hypot(x2-x1,y2-y1)
        lengthm = math.hypot(x3-x1,y3-y1)#length of line
        lengthp = math.hypot(x4-x1,y4-y1)
        #  print(lengthp)
        #min 30 max #200 for index to thumb
        #min 30 max like 230 for middle to thumb 
        #min was 25 max wa 350 for pinky to thumb

        #vol range -63 to 0
       # vol = np.interp(length,[30,200],[minVol, maxVol])
        #volb = np.interp(length,[30,200],[400, 150])
        #volp = np.interp(length,[30,200],[0, 100])
        #print(int(length),vol)
        #volume.SetMasterVolumeLevel(vol,None)
        
        
        
        if lengthi<30:
            cv2.circle(img, (cx,cy), 15 ,(0,255,0), cv2.FILLED)
            loop.run_until_complete(upper.update())
            loop.run_until_complete(upper.turn_on())
        if lengthm<30:
            cv2.circle(img, (cx1,cy1), 15 ,(0,255,0), cv2.FILLED)
            loop.run_until_complete(lower.update())
            loop.run_until_complete(lower.turn_on())
        if lengthp<30:
            cv2.circle(img, (cx2,cy2), 15 ,(0,255,0), cv2.FILLED)
            loop.run_until_complete(upper.update())
            loop.run_until_complete(lower.update())
            loop.run_until_complete(upper.turn_off())
            loop.run_until_complete(lower.turn_off())



    #cv2.rectangle(img,(50,150),(85,400),(0,255,0), 3)
    #cv2.rectangle(img,(50,int(volb)),(85,400),(0,255,0), cv2.FILLED)
    #cv2.putText(img, f' {int(volp)}%',(40,450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,250,0), 3)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1) #1 second delay
