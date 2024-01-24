import threading
import cv2
import mediapipe as mp
import numpy as np
from gym.models import Exercises
from django.contrib.auth.models import User
import datetime
import time
import math

class DumbbellCamera(object):
    def __init__(self, user):
        #define class veriables.
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.user = user
        self.counter = 0 
        self.lock = False
        self.stage = None
        self.lmList = []
        self.count = 0
        self.dir = 1
        self.pTime = 0
        self.results = None
        self.exType = ''

        (self.grabbed, self.frame) = self.video.read()
        # Threading is a sequence of instructions in a program that can be executed independently of the remaining process
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()
                
    #this will run for each video frame
    def get_frame(self):
        image = self.frame
        #image = cv2.resize(image, (1280, 720))

        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while True:
                # Reverse frame color order (Blue Green, Red) from BGR to RGB reverse from frame
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                # ser writeable to False to save some memory
                image.flags.writeable = False
            
                # Make detection and store it in an array called results
                results = pose.process(image)
            
                # Set writable back to True
                image.flags.writeable = True

                # render back to image using OpenCV
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                

                try:
                    image = self.findPose(image, results)
                    self.lmList = self.findPosition(image, results)

                    if len(self.lmList) != 0:
                        # Right Arm
                        rightArmAngle = self.findAngle(image, 12, 14, 16)

                        per = np.interp(rightArmAngle, (210, 310), (0, 100))

                        # Left Arm
                        leftArmAngle = self.findAngle(image, 11, 13, 15)


                        if rightArmAngle >= 250:
                            bar = np.interp(rightArmAngle, (220, 310), (650, 100))
                        elif leftArmAngle >= 0:
                            per = np.interp(leftArmAngle, (30, 150), (100, 0))
                            bar = np.interp(leftArmAngle, (30, 150), (100, 650))

                        # Check for the dumbbell curls
                        color = (255, 0, 255)
                        if per == 100:
                            if rightArmAngle >= 250:
                                self.exType = 'Dumbbell Reverse Curl'
                            elif leftArmAngle >= 0:
                                self.exType = 'Dumbbell Reverse Curl'

                            color = (0, 255, 0)
                            if self.dir == 0:
                                self.count += 0.5
                                self.dir = 1

                        if per == 0:
                            if rightArmAngle >= 250:
                                self.exType = 'Dumbbell Reverse Curl'
                            elif leftArmAngle >= 0:
                                self.exType = 'Dumbbell Reverse Curl'
                            color = (0, 255, 0)
                            if self.dir == 1:
                                self.count += 0.5
                                self.dir = 0
                                self.saveToDB()

                        # Draw Bar
                        cv2.rectangle(image, (1100, 100), (1175, 650), color, 3)
                        cv2.rectangle(image, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
                        cv2.putText(image, f'{int(per)} %', (500, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

                except:
                    pass
                
                # Render curl counter
                # Setup status box
                # cv2.rectangle(image, (0,0), (325,73), (0, 0, 255), -1)
                
                # Rep data
                # cv2.putText(image, 'Exercise Type', (15,12), 
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
                # cv2.putText(image, str(self.exType), 
                #             (10,60), 
                #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)

                cTime = time.time()
                fps = 1 / (cTime - self.pTime)
                self.pTime = cTime
                cv2.putText(image, str(int(fps)), (50, 0), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

                # Draw Curl Count
                cv2.rectangle(image, (0, 450), (150, 350), (0, 0, 255), cv2.FILLED)
                cv2.putText(image, str(int(self.count)), (25, 420), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 7)

                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                # Render detections
                """self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                        self.mp_drawing.DrawingSpec(color=(255,1,3), thickness=2, circle_radius=2), 
                                        self.mp_drawing.DrawingSpec(color=(3,3,254), thickness=2, circle_radius=2) 
                                        )  
                   """
                
                _, jpeg = cv2.imencode('.jpg', image)
                return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

    def findPose(self, img, results, draw=True):
        if results.pose_landmarks:
            if draw:
                self.mp_drawing.draw_landmarks(img, results.pose_landmarks,
                                           self.mp_pose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, results, draw=True):
        lmList = []
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList
    
    def findAngle(self, img, p1, p2, p3, draw=True):
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        #print(angle)

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (0, 0, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle
    
    def saveToDB(self):
        today = datetime.datetime.now().date()
        try:
            step_update = Exercises.objects.get(exercise_date = today, user_id = self.user, exercise_type = self.exType)
            step_update.exercise_value = step_update.exercise_value + 1
            step_update.save()
        except:
            user = User.objects.get(id=self.user)
            exercise = Exercises(exercise_date = today, exercise_type = self.exType, exercise_value = 1, user_id = user)
            exercise.save()
        