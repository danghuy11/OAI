import numpy as np
import cv2
import time

camera = cv2.VideoCapture(0) 
#camera = cv2.VideoCapture(0,cv2.CAP_DSHOW) 
#camera = cv2.VideoCapture("http://93.48.88.159/mjpg/video.mjpg")

print('use key s to save the current image')
while True:
    hasFrame, frame = camera.read()
    if not hasFrame:
        break
    cv2.imshow('camera',frame)
    key = cv2.waitKey(10) & 0xff
    if key == 27:
        break
    elif key == ord('s'): # save the image
        name = str(round(time.time()))
        cv2.imwrite(name+'.png',frame)
        print(f'saved {name}.png')

camera.release()
cv2.destroyAllWindows()
