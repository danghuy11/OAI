import cv2 as cv
import numpy as np 
import time
import os
from agentspace import space, Agent
from dino import dino, dino_visualization

def quit():
    os._exit(0)

# Initializing video capture agent
class CameraAgent(Agent):
    def init(self):
        camera = cv.VideoCapture(0) # ,cv.CAP_DSHOW
        while True:
            _, frame = camera.read()
            space["bgr"] = frame
            if self.stopped:
                break
        
camera_agent = CameraAgent()
while space["bgr"] is None: 
    time.sleep(0.25) # wait for camera

# Kalman filtering initialization
last_ticks = cv.getTickCount()    
KF = cv.KalmanFilter(4, 2, 0) 
KF.transitionMatrix = cv.setIdentity(KF.transitionMatrix)
KF.measurementMatrix = cv.setIdentity(KF.measurementMatrix)

while True:
    frame = space["bgr"]
    if frame is None:
        break

    t0 = time.time()
    
    mask, point = dino(frame)
    
    # Kalman filtering
    ticks = cv.getTickCount()
    dt = (ticks - last_ticks) / cv.getTickFrequency()
    last_ticks = ticks    
    KF.transitionMatrix[0,2] = dt
    KF.transitionMatrix[1,3] = dt
    prediction = KF.predict()
    if point[0] >= 0.0 and point[1] >= 0.0:
        correction = KF.correct(np.array(point,np.float32))
        point = (correction[0][0],correction[1][0])
    else:
        point = (prediction[0][0],prediction[1][0])
    
    t1 = time.time()
    fps = 1.0/(t1-t0)
    
    result = dino_visualization(frame, mask, point)

    cv.imshow('dino',result)
    key = cv.waitKey(1) & 0xff
    if key == 27:
        break

cv.destroyAllWindows()
camera_agent.stop()
