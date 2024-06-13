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
