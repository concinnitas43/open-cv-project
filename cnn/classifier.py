from cnn.cnn_model import *

model = CNNModel()
model.load_state_dict(torch.load('cnn/cnn-model1.pth'))

def classify_image(image):
    # evaluate the class on image
    model.eval()

    with torch.no_grad():
        image = cv2.resize(image, (WIDTH, HEIGHT))
        image = torch.tensor(image, dtype=torch.float).permute(2, 0, 1) / 255.0

        image = image.unsqueeze(0)  # Add batch dimension
        output = model(image)
        _, predicted = torch.max(output, 1)
        return predicted.item()
