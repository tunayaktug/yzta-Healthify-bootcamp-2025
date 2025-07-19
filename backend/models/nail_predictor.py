from PIL import Image

class NailPredictor:
    def __init__(self, model_path="models/nail_model.onnx"):
        self.model_path = model_path
        # Model henüz mevcut değil, simülasyon kullanıyoruz
    
    def predict(self, image: Image):
        """Tırnak tahmini yap (şimdilik simülasyon)"""
        return "Tırnak renginde bozulma ve çatlak tespit edildi."
