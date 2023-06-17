import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as T
from torchvision import models
from torchvision.io import read_image
import matplotlib.pyplot as plt
from PIL import Image

# 眼角膜 resnet18 pytorch

# CNV:脉络膜新生血管
# DME:糖尿病性黄斑水肿
# DRUSEN:玻璃疣
# NORMAL:正常
# label_map = {'CNV':0, 'DME':1, 'DRUSEN':2, 'NORMAL':3,}
label_reverse = { 0:'脉络膜新生血管(CNV)', 1:'糖尿病性黄斑水肿(DME)', 2:'玻璃膜疣(DRUSEN)', 3:'一切正常',}

img_path = '/home/lighthouse/resnet-OCT/static/image/CNV-1016042-1.jpeg'
model_path = '/home/lighthouse/resnet-OCT/OCT-Resnet_model.pth'


transform = T.Compose([
    T.Grayscale(num_output_channels = 1), # 彩色图像转灰度图像num_output_channels默认1
    T.ToTensor()
])

def transform_img(img_path):
        # image = read_image(img_path)
        image = Image.open(img_path)
        image = transform(image)
        print(image.size())
        if image.size()[0] == 1:
                image = image.repeat(3, 1, 1)
        image = image / 255.0
        image = T.Resize((224, 224))(image)
        image = image.unsqueeze(0)
        return image

def load_model(path):
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model = models.resnet18(weights=torchvision.models.ResNet18_Weights.IMAGENET1K_V1)
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, 10)
        model.to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        model.load_state_dict(torch.load(path, map_location='cpu'))
        return model



def pre_OCT(model_path, img_path):
        with torch.set_grad_enabled(False):
                model=load_model(model_path)
                outputs = model(transform_img(img_path))
                _, preds = torch.max(outputs, 1)
                prediction = preds.tolist()[0]
                # print(prediction)
                print(label_reverse[prediction])
                return label_reverse[prediction]

if __name__=='__main__':
        pre_OCT(model_path, img_path)

