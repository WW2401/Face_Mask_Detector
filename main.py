import torch
import torch.nn as nn
import torchvision
from torchvision import models
import numpy as np
import mmcv, cv2
from utils.utils import corp_img, predict_draw

# model loading
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model_ft = models.resnet18(pretrained=True)
num_ftrs = model_ft.fc.in_features
model_ft.fc = nn.Linear(num_ftrs, 2)
print('loading model')
model_ft.load_state_dict(torch.load('./model/mask_classifier'))
model_ft = model_ft.to(device)

# running camera
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read() #Capture each frame
    img = predict_draw(model_ft, frame)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow("Face Mask Detetor", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyWindow("Face Mask Detetor")
