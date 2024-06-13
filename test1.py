from cnn.cnn_model import *

# 학습을 GPU가 있는 컴에서 해서 저장한 모델을 CPU에서 불러올 때 사용, 나도 사실 원리 모름
def load_model_on_cpu(model_path):
    return torch.load(model_path, map_location=torch.device('cpu'))

model = CNNModel()  # 초기화 
model.load_state_dict(load_model_on_cpu('cnn/cnn-model.pth'))  # 읽어오기

def classify_image(image):
    model.eval()  # 모델을 평가 모드로 전환 (Dropout 등 비활성화)

    with torch.no_grad():
        image = cv2.resize(image, (WIDTH, HEIGHT))  # 이미지를 모델 입력 크기로 리사이즈 (600x600)
        image = torch.tensor(image, dtype=torch.float).permute(2, 0, 1) / 255.0  # 이미지를 텐서로 변환하고 [0, 1] 범위로 정규화, (채널, 높이, 너비) 형식으로 변경

        image = image.unsqueeze(0)  # 배치 차원 추가
        output = model(image) # 대입!
        _, predicted = torch.max(output, 1) # 최대인거 가져오기
        return predicted.item()


import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
import os
import numpy as np
from torchvision import transforms

## GPU 서버에서 하기 위해서 cnn_model.py 수정 => GPU 관련된 부분만 조금 다름 

WIDTH, HEIGHT = 600, 600
NUM_CLASSES = 6
class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.pool = nn.MaxPool2d(2, 2)
        self.conv1 = nn.Conv2d(3, 32, 3)  # Increased filters
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, 3)  # Increased filters
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, 3)  # Increased filters
        self.bn3 = nn.BatchNorm2d(128)
        self.conv4 = nn.Conv2d(128, 256, 3)  # Increased filters
        self.bn4 = nn.BatchNorm2d(256)
        self.conv5 = nn.Conv2d(256, 512, 3)  # New convolutional layer
        self.bn5 = nn.BatchNorm2d(512)

        self.global_pool = nn.AdaptiveAvgPool2d(1)  # Global average pooling layer

        self.fc1 = nn.Linear(512, 256)  # Increased size of fully connected layers
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 32)
        self.fc5 = nn.Linear(32, NUM_CLASSES)

    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        x = self.pool(F.relu(self.bn4(self.conv4(x))))
        x = self.pool(F.relu(self.bn5(self.conv5(x))))  # Additional convolutional layer

        x = self.global_pool(x)  # Global average pooling
        x = x.view(x.size(0), -1)
        
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return x


if __name__ == "__main__":
    # 디바이스 설정 
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CNNModel().to(device)

    classes = [f"snack{i}" for i in range(0, NUM_CLASSES)]
    print(classes)
    image_paths = []
    labels = []

    for label, class_name in enumerate(classes):
        class_dir = os.path.join('snack_data', class_name)
        for img_name in os.listdir(class_dir):
            if not img_name.endswith('.jpg'):
                continue
            img_path = os.path.join(class_dir, img_name)
            image_paths.append(img_path)
            labels.append(label)

    image_paths = np.array(image_paths)
    labels = np.array(labels)

    indices = np.random.permutation(len(image_paths))

    image_paths = image_paths[indices]
    labels = labels[indices]

    image_paths = list(image_paths)
    labels = list(labels)

    print(image_paths[:5], labels[:5])

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    batch_size = 32
    num_epochs = 5
    total_steps = len(image_paths) // batch_size

    for epoch in range(num_epochs):
        running_loss = 0.0
        correct_predictions = 0
        total_predictions = 0
        for step in range(total_steps):
            batch_images = image_paths[step * batch_size:(step + 1) * batch_size]
            batch_labels = labels[step * batch_size:(step + 1) * batch_size]

            images = []
            for img_path in batch_images:
                image = cv2.imread(img_path)
                if image is None:
                    print('Wrong path:', img_path)
                    continue
                image = cv2.resize(image, (WIDTH, HEIGHT))
                image = torch.tensor(image, dtype=torch.float).permute(2, 0, 1) / 255.0  # Normalize to [0, 1]
                images.append(image)

            images = torch.stack(images).to(device)
            batch_labels = torch.tensor(batch_labels, dtype=torch.long).to(device)

            outputs = model(images)
            loss = criterion(outputs, batch_labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (step + 1) % 10 == 0:
                print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{step + 1}/{total_steps}], Loss: {loss.item()}')

            # Accuracy calculation
            _, predicted = torch.max(outputs, 1)
            correct_predictions += (predicted == batch_labels).sum().item()
            total_predictions += batch_labels.size(0)

            running_loss += loss.item()

            if (step + 1) % 10 == 0:  # Print accuracy
                accuracy = correct_predictions / total_predictions
                print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{step + 1}/{total_steps}], Loss: {running_loss / (step + 1)}, Accuracy: {accuracy:.4f}')

    torch.save(model.state_dict(), 'cnn-model2.pth')
