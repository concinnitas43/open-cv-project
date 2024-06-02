# https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html 에서 참고를 많이 함, 일부 코드는 gpt 사용됨
import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
import os

WIDTH, HEIGHT = 400, 400

class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.fc1 = nn.Linear(64 * 47 * 47, 128)
        self.fc2 = nn.Linear(128, 6)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 47 * 47)
        x = F.relu(self.fc1(x))
        x = F.softmax(self.fc2(x), dim=1)
        return x


model = CNNModel()
model.load_state_dict(torch.load('cnn-model.pth'))

classes = ['class1', 'class2', 'class3', 'class4', 'class5', 'empty']
image_paths = []
labels = []

for label, class_name in enumerate(classes):
    class_dir = os.path.join('dataset', class_name)
    for img_name in os.listdir(class_dir):
        img_path = os.path.join(class_dir, img_name)
        image_paths.append(img_path)
        labels.append(label)


criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

batch_size = 32
num_epochs = 5
total_steps = len(image_paths) // batch_size

for epoch in range(num_epochs):
    for step in range(total_steps):
        batch_images = image_paths[step * batch_size:(step + 1) * batch_size]
        batch_labels = labels[step * batch_size:(step + 1) * batch_size]

        images = []
        for img_path in batch_images:
            image = cv2.imread(img_path)
            image = cv2.resize(image, (WIDTH, HEIGHT))
            image = torch.tensor(image, dtype=torch.float).permute(2, 0, 1)
            images.append(image)

        images = torch.stack(images)
        batch_labels = torch.tensor(batch_labels, dtype=torch.long)

        outputs = model(images)
        loss = criterion(outputs, batch_labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (step + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{step + 1}/{total_steps}], Loss: {loss.item()}')

model.eval()
with torch.no_grad():
    for image in images:
        image = torch.tensor(image, dtype=torch.float).permute(2, 0, 1).unsqueeze(0)
        output = model(image)
        _, predicted = torch.max(output, 1)
        print(classes[predicted.item()])

