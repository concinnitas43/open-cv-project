import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
import os
import numpy as np
from torchvision import transforms
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
    model = CNNModel()
    # model.load_state_dict(torch.load('cnn-model.pth'))
    classes = [ f"snack{i}" for i in range(0, NUM_CLASSES) ]
    print(classes)
    image_paths = []
    labels = []

    for label, class_name in enumerate(classes):
        class_dir = os.path.join('snack_data', class_name)
        for img_name in os.listdir(class_dir):
            # only if the file is an image
            if not img_name.endswith('.jpg'):
                continue
            img_path = os.path.join(class_dir, img_name)
            image_paths.append(img_path)
            labels.append(label)

    image_paths = np.array(image_paths)
    labels = np.array(labels)

    # Generate a permutation of indices
    indices = np.random.permutation(len(image_paths))

    # Shuffle arrays with the permutation indices
    image_paths = image_paths[indices]
    labels = labels[indices]

    # Convert back to lists if needed
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

            images = torch.stack(images)
            batch_labels = torch.tensor(batch_labels, dtype=torch.long)

            outputs = model(images)
            loss = criterion(outputs, batch_labels)

            # 실제 훈련
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (step + 1) % 10 == 0:
                print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{step + 1}/{total_steps}], Loss: {loss.item()}')

            ## 정확도 계산을 위해서 
            _, predicted = torch.max(outputs, 1)
            correct_predictions += (predicted == batch_labels).sum().item()
            total_predictions += batch_labels.size(0)

            running_loss += loss.item()

            if (step + 1) % 10 == 0: # 정확도 출력
                accuracy = correct_predictions / total_predictions
                print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{step + 1}/{total_steps}], Loss: {running_loss / (step + 1)}, Accuracy: {accuracy:.4f}')


    # model.eval()
    # with torch.no_grad():
    #     for image_path in image_paths:
    #         image = cv2.imread(image_path)
    #         image = cv2.resize(image, (WIDTH, HEIGHT))
    #         image = torch.tensor(image, dtype=torch.float).permute(2, 0, 1) / 255.0  # Normalize to [0, 1]
    #         image = image.unsqueeze(0)  # Add batch dimension
    #         output = model(image)
    #         _, predicted = torch.max(output, 1)
            # print(classes[predicted.item()])


    torch.save(model.state_dict(), 'cnn-model2.pth')