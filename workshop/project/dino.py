import torch
import numpy as np
import cv2

# load model
vits8 = torch.hub.load('facebookresearch/dino:main', 'dino_vits8')
vits8.eval()

#device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = 'cpu'
print('device:',device)
vits8.to(device)

def dino(image, head=2):
    image_size = (224, 224)
    blob = cv2.dnn.blobFromImage(image, 1.0/255, image_size, swapRB=True, crop=True)
    blob[0][0] = (blob[0][0] - 0.485)/0.229
    blob[0][1] = (blob[0][1] - 0.456)/0.224
    blob[0][2] = (blob[0][2] - 0.406)/0.225
    with torch.no_grad():
        input_tensor = torch.tensor(blob).to(device)
        attention = vits8.get_last_selfattention(input_tensor)[0]
        attention = attention[:,0,1:].view(-1,image_size[1]//8,image_size[0]//8)

    attention = attention.cpu().numpy()
    mask = attention[head]
    mask /= mask.max()
    mask = (mask*255).astype(np.uint8)
    mask = cv2.resize(mask,(image.shape[1],image.shape[0]))
    mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(mask)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
    ys, xs = np.where(mask > 0)
    point = (0.5,0.5) if len(xs) == 0 else (xs.mean() / mask.shape[1], ys.mean() / mask.shape[0])
    return mask, point

def dino_visualization(frame, mask, point):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    result = cv2.merge([gray,gray,gray|mask])
    pt = (int(point[0]*frame.shape[1]),int(point[1]*frame.shape[0]))
    cv2.circle(result,pt,3,(0,0,255),cv2.FILLED)
    return result
    
if __name__ == "__main__": 
    frame = cv2.imread("sample.jpg")
    cv2.imshow('input',frame)
    cv2.waitKey(1)
    mask, point = dino(frame)
    result = dino_visualization(frame, mask, point)
    cv2.imshow('DINO',result)
    cv2.waitKey(0)
