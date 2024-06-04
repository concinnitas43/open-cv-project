# https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html 에서 참고를 많이 함, 일부 코드는 gpt 사용됨
import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
import os
import numpy as np

WIDTH, HEIGHT = 400, 400
NUM_CLASSES = 3

class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.pool = nn.MaxPool2d(2, 2)
        self.conv1 = nn.Conv2d(3, 12, 3)
        self.conv2 = nn.Conv2d(12, 24, 3)
        self.conv3 = nn.Conv2d(24, 48, 3)
        self.fc1 = nn.Linear(48 * 48 * 48, 32)  # Corrected input size
        self.fc2 = nn.Linear(32, NUM_CLASSES)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 48 * 48 * 48)  # Corrected input size
        x = F.relu(self.fc1(x))
        x = F.softmax(self.fc2(x), dim=1)
        return x

model = CNNModel()
# model.load_state_dict(torch.load('cnn-model.pth'))

classes = [ f"snack{i}" for i in range(0, NUM_CLASSES) ]
image_paths = []
labels = []

for label, class_name in enumerate(classes):
    class_dir = os.path.join('snack_data', class_name)
    for img_name in os.listdir(class_dir):
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
            image = cv2.resize(image, (WIDTH, HEIGHT))
            image = torch.tensor(image, dtype=torch.float).permute(2, 0, 1) / 255.0  # Normalize to [0, 1]
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

        _, predicted = torch.max(outputs, 1)
        correct_predictions += (predicted == batch_labels).sum().item()
        total_predictions += batch_labels.size(0)

        running_loss += loss.item()

        if (step + 1) % 10 == 0:
            accuracy = correct_predictions / total_predictions
            print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{step + 1}/{total_steps}], Loss: {running_loss / (step + 1)}, Accuracy: {accuracy:.4f}')


# model.eval()
# with torch.no_grad():
#     for image in images:
#         image = torch.tensor(image, dtype=torch.float).permute(2, 0, 1).unsqueeze(0)
#         output = model(image)
#         _, predicted = torch.max(output, 1)
#         print(classes[predicted.item()])

model.eval()
with torch.no_grad():
    for image_path in image_paths:
        image = cv2.imread(image_path)
        image = cv2.resize(image, (WIDTH, HEIGHT))
        image = torch.tensor(image, dtype=torch.float).permute(2, 0, 1) / 255.0  # Normalize to [0, 1]
        image = image.unsqueeze(0)  # Add batch dimension
        output = model(image)
        _, predicted = torch.max(output, 1)
        print(classes[predicted.item()])


torch.save(model.state_dict(), 'cnn-model.pth')