import numpy as np
import cv2
import torch
from transformers import CLIPProcessor, CLIPModel

# Load model + processor
from transformers import logging
logging.set_verbosity_error()
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=False)
model.eval()

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('device:',device)
model.to(device)

def normalize(embeddings):
    return embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def image_clip(image,cropping = True):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    inputs = processor(images=image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
        if isinstance(image_features, dict) and 'pooler_output' in image_features: # fix for higher versions
            image_features = image_features['pooler_output']
        #image_features = image_features / image_features.norm(dim=-1, keepdim=True)
    return image_features.cpu().numpy()
       
def text_clip(texts):
    inputs = processor(text=texts, return_tensors="pt", padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        text_features = model.get_text_features(**inputs)
        if isinstance(text_features, dict) and 'pooler_output' in text_features: # fix for higher versions
            text_features = text_features['pooler_output']
        #text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    return text_features.cpu().numpy()
    
def cosine_similarity(embedding, embeddings, factor=100):
    logits = (normalize(embedding) @ normalize(embeddings).T)[0]
    probabilities = softmax(logits*factor)
    return probabilities

def clip(image, texts_embeddings, cropping = True):
    image_embedding = image_clip(image, cropping)
    probabilities = cosine_similarity(image_embedding, text_embeddings)
    return probabilities

if __name__ == "__main__":

    texts = [
        "a mandarine", 
        "two mandarines", 
        "a man showing a mandarine", 
        "a girl showing a mandarine", 
        "a ball", 
        "two balls", 
        "a man showing a ball", 
        "a girl showing a ball", 
        "an iron",
        "a man showing an iron",
    ]
    text_embeddings = text_clip(texts)
    
    for image_name in ['mandarine.jpg','ball.jpg']:
    
        image = cv2.imread(image_name)
    
        probabilities = clip(image,texts)
        for text, probability in zip(texts, probabilities):
            print(f"{text}: {probability:.3f}")

        print()

"""
a mandarine: 0.055
two mandarines: 0.029
a man showing a mandarine: 0.898
a girl showing a mandarine: 0.010
a ball: 0.001
two balls: 0.002
a man showing a ball: 0.004
a girl showing a ball: 0.000
an iron: 0.000
a man showing an iron: 0.000
"""

"""
a mandarine: 0.001
two mandarines: 0.000
a man showing a mandarine: 0.025
a girl showing a mandarine: 0.000
a ball: 0.091
two balls: 0.023
a man showing a ball: 0.828
a girl showing a ball: 0.020
an iron: 0.001
a man showing an iron: 0.011
"""


