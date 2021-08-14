import torch
from PIL import Image
import os
import torchvision.models as models
import sys
from torch.backends import cudnn
import torchvision.transforms as transforms

from model import *
import torch.nn as nn
import numpy as np

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def load_model():
    if os.path.isfile('../model_state_dict/PCA-Net.pth'):
        model_loaded = resnet50(pretrained=True, use_bp=True)
        in_features = model_loaded.classifier.in_features
        model_loaded.classifier = torch.nn.Linear(in_features=in_features, out_features=200)
        model_loaded = model_loaded.cuda()
        model_loaded = nn.DataParallel(model_loaded)
        checkpoint = torch.load('../model_state_dict/PCA-Net.pth.tar')
        model_loaded.load_state_dict(checkpoint['state_dict'], False)
    else:
        return 'model failed to load'
    model_loaded.eval()
    # print("Model loaded")
    return model_loaded


def model_predict(model, image):
    # process file?
    image = Image.open(image)
    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.CenterCrop((448, 448)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    image = transform(image)
    image = np.expand_dims(image, 0)
    image = torch.from_numpy(image)
    image = image.cuda()
    # pass to model
    _, _, _, result = model(image)
    # print(result)
    # return prediction
    return result

