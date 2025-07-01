import torch
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights
from PIL import Image
import io

# Yeni weights sistemini kullan
weights = ResNet50_Weights.DEFAULT
model = models.resnet50(weights=weights)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(tensor)
        _, predicted = outputs.max(1)
    return int(predicted.item())
