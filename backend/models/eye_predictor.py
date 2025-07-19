from PIL import Image

class EyePredictor:
    def __init__(self, model_path="models/eye_model.onnx"):
        self.model_path = model_path
        # Model henüz mevcut değil, simülasyon kullanıyoruz
    
    def predict(self, image: Image):
        """Göz tahmini yap (şimdilik simülasyon)"""
        return "Göz çevresinde kuruluk ve kızarıklık tespit edildi." 