import random
import cv2 
import cvzone 
from cvzone.HandTrackingModule import HandDetector 
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
playerWickets = 10  # Player has 10 turns (wickets)
scores = [0, 0]  # [AI, Player]

def display_final_score():
    print(f"Game Over! Final Score: {scores[1]}")
    cv2.putText(imgBG, f"Final Score: {scores[1]}", (800, 500), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 5)
    cv2.imshow("BG", imgBG)
    cv2.waitKey(3000)  # Show final score for 3 seconds
    cap.release()
    cv2.destroyAllWindows()
    exit()

while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 0  # ZERO
                    elif fingers == [0, 1, 0, 0, 0]:
                        playerMove = 1  # ONE
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 2  # TWO
                    elif fingers == [0, 1, 1, 1, 0]:
                        playerMove = 3  # THREE
                    elif fingers == [0, 1, 1, 1, 1]:
                        playerMove = 4  # FOUR
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 5  # FIVE
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 5  # FIVE
                    randomNumber = random.randint(0, 5)  # Random AI move from 0 to 5
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Hand Cricket Logic
                    if playerMove == randomNumber:
                        playerWickets -= 1  # Lose a wicket
                        resultText = "OUT!"
                    else:
                        scores[1] += playerMove  # Add score to player

                    if playerWickets == 0:
                        display_final_score()
    
    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    # Scoreboard UI
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, f"Wickets: {playerWickets}/10", (800, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 5)

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
