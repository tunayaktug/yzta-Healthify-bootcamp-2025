from PIL import Image

class HairPredictor:
    def __init__(self, model_path="models/hair_model.onnx"):
        self.model_path = model_path
        # Model henüz mevcut değil, simülasyon kullanıyoruz
    
    def predict(self, image: Image):
        """Saç tahmini yap (şimdilik simülasyon)"""
        return "Yoğun dökülme ve seyrelme tespit edildi." 