import cv2
from cvzone.HandTrackingModule import HandDetector

from time import sleep
from pynput.keyboard import Controller


cap = cv2.VideoCapture(0)
cap.set(3 , 1000)
cap.set(4  , 800)

key_list = [["Q" , "W" , "E" ,"R"],["A" , "S" , "D" ,"F"] , ["Z" , "X" , "C" ,"V"]]
final_text = ""
keyboard = Controller()


detector = HandDetector(detectionCon=0.5)

class Button():
    def __init__(self , pos , text , size= [90 , 50 ]  , color = (0, 255, 255)):
        self.pos = pos
        self.text = text
        self.size = size
        self.color = color



def drawAll(frame , btnlist):

    for btn in btnlist:
        x, y = btn.pos
        w, h = btn.size
        color = btn.color
        cv2.rectangle(frame, (x, y), (x + w, y + h),  color , cv2.FILLED)
        cv2.putText(frame, btn.text, (x + 10, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)


btn_list = []

for i in range(len(key_list)):
    for (j, key) in enumerate(key_list[i]):
        btn_list.append(Button([100 * j + 10, 70 * i + 50], key))



while True :
    ret , frame = cap.read()

    frame = cv2.flip(frame, 1)

    #lmList , bbox_info = detector.findPosition(frame)

    hand , frame = detector.findHands(frame)
    #print(hand)

    #lmList = hand[0]['lmList']
    #print(lmList)

    drawAll(frame, btn_list)

    if hand:

        lmList = hand[0]['lmList']

        print(lmList[8])
        print(lmList[8][:2])

        for btn in btn_list:
            x, y = btn.pos
            w , h = btn.size

            if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:


                cv2.rectangle(frame, (x, y), (x + w, y + h), (0 , 175, 175), cv2.FILLED)
                cv2.putText(frame, btn.text, (x + 10, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)

                # click if the distance bw two fingers is small

                l , _ , _= detector.findDistance( lmList[8][:2] , lmList[12][:2] ,  frame)
                print(l)

                if l<30:

                    keyboard.press(btn.text)
                    cv2.putText(frame, btn.text, (x + 10, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)

                    final_text += btn.text
                    sleep(0.15)

    cv2.rectangle(frame, (10 , 250 ), (600 , 330), (0, 255, 0), cv2.FILLED)
    cv2.putText(frame, final_text , ( 130, 300 ), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
    cv2.imshow("Frame" , frame)

    if cv2.waitKey(1) == ord('q'):
        break