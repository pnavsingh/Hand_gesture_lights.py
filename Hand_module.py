
import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False,maxHands = 2,model_complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.model_complexity,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
    
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #only process color of hands
        self.results = self.hands.process(imgRGB) #processes the color of the hand
    #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img
    def findPosition(self,img, handNo=0, draw = True): #handno for 1 hand rn can refer 40 min in vid to make two
        lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand= self.results.multi_hand_landmarks[handNo]
        
            for id, lm in enumerate(myhand.landmark): #gets landmark and id 
                #print(id,lm)
                h, w, c = img.shape #width height 
                cx, cy = int(lm.x*w), int(lm.y*h) #width heigh in pixel form
                #print(id, cx,cy)
                lmlist.append([id,cx,cy])
                #if id == 4: #gets the specific placement
                if draw:
                    cv2.circle(img, (cx,cy), 10,(255,0,255),cv2.FILLED)
        return lmlist
   

def main():
    ptime=0
    ctime=0
    cap = cv2.VideoCapture(0)
    detector = handDetector()



    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist =detector.findPosition(img)
        if len(lmlist) !=0:
            print(lmlist[4])
        #detector.findHands(img)
        ctime= time.time()
        fps = 1/(ctime-ptime) #calculates fps

        ptime=ctime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),2) #displays fps
    
    
        cv2.imshow("Image", img) #Shows the camera
        cv2.waitKey(1) #not sure what this does 
if __name__ == "__main__":
        main()
        
