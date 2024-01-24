import threading
import cv2
import mediapipe as mp
import numpy as np
from gym.models import Exercises
from django.contrib.auth.models import User
import datetime
import time
import math

class BarbellCamera(object):
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
                        # Right leg
                        rightLegAngle = self.findAngle(image, 24, 26, 28)
                        rightHandAngle = int(np.interp(rightLegAngle, (80, 173), (100, 0)))

                        # Left leg
                        leftLegAngle = self.findAngle(image, 23, 25, 27)
                        leftHandAngle = int(np.interp(leftLegAngle, (-30, 180), (100, 0)))
                        per = np.interp(leftLegAngle, (33, 57), (100, 0))

                        left, right = leftHandAngle, rightHandAngle

                        print(left, right)
                        #color = (255, 0, 255)
                        if left >= 33:
                            self.exType = 'Barbell Squat'
                            if self.dir == 0:
                                self.count += 0.5
                                self.dir = 1

                        if left <= 33:
                            self.exType = 'Barbell Squat'
                            if self.dir == 1:
                                self.count += 0.5
                                self.dir = 0
                                self.saveToDB()

                        cv2.rectangle(image, (0, 0), (120, 120), (0, 0, 255), -1)
                        cv2.putText(image, str(int(self.count)), (20, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (255, 255, 255), 7)

                        leftval  = np.interp(right,[0,100],[400,200])
                        
                        cv2.rectangle(image, (952, 200), (995, 400), (0, 255, 0), 5)
                        cv2.rectangle(image, (952, int(leftval)), (995, 400), (0, 255, 0), -1)

                except:
                    pass
                

                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

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
        