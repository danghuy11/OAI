import numpy as np
import cv2 as cv
import time
from agentspace import Agent, space
from dino import dino
from clip import image_clip

class PerceptionAgent(Agent):

    def __init__(self, nameImage, nameFeatures, namePoints):
        self.nameImage = nameImage
        self.nameFeatures = nameFeatures
        self.namePoints = namePoints
        super().__init__()

    def init(self):
        self.KF = cv.KalmanFilter(4, 2, 0)
        self.KF.transitionMatrix = cv.setIdentity(self.KF.transitionMatrix)
        self.KF.measurementMatrix = cv.setIdentity(self.KF.measurementMatrix)
        self.ticks = cv.getTickCount()
        space.attach_trigger(self.nameImage,self)
        self.t0 = int(time.time())
        self.fs = 0
        self.fps = 0
 
    def senseSelectAct(self):
        frame = space[self.nameImage]
        if frame is None:
            return
            
        _, point = dino(frame)
        
        features = image_clip(frame)
            
        ticks = cv.getTickCount()
        dt = (ticks - self.ticks) / cv.getTickFrequency()
        self.ticks = ticks
        self.KF.transitionMatrix[0,2] = dt
        self.KF.transitionMatrix[1,3] = dt
        prediction = self.KF.predict()
        if point[0] >= 0.0 and point[1] >= 0.0:
            correction = self.KF.correct(np.array(point,np.float32))
            point = (correction[0][0],correction[1][0])
        else:
            point = (prediction[0][0],prediction[1][0])
        
        self.fs += 1
        self.t1 = int(time.time())
        if self.t1 > self.t0:
            self.fps = self.fs / (self.t1-self.t0)
            self.fs = 0
            self.t0 = self.t1
            space(validity=2.5)['fps'] = self.fps
        
        space(validity=0.5)[self.nameFeatures] = features
        space(validity=0.5)[self.namePoints] = point

if __name__ == "__main__":

    from CameraAgent import CameraAgent
    camera_agent = CameraAgent('See3CAM_CU135', 0, 'bgr', fps=30, zoom=350)
    
    from dino import dino_visualization
    PerceptionAgent('bgr','clipFeatures','dinoPoints')

    class ViewerAgent(Agent):
    
        def init(self):
            space.attach_trigger('bgr',self)
            
        def senseSelectAct(self):
            frame = space["bgr"]
            if frame is None:
                self.stopped = True
                return

            point = space["dinoPoints"]
            result = dino_visualization(frame,np.zeros(frame.shape[:2],np.uint8),point)
            fps = space["fps"]
            if fps is not None:
                cv.putText(result, f"{fps:1.0f}", (8,25), 0, 1.0, (0, 255, 0), 2)

            cv.imshow('dino & clip',result)
            key = cv.waitKey(1) & 0xff
            if key == 27:
                self.stopped = True
                return
    
    viewer_agent = ViewerAgent()
    time.sleep(20)
    viewer_agent.stop()
    cv.destroyAllWindows()
    camera_agent.stop()
