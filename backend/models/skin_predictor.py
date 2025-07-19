from PIL import Image

class SkinPredictor:
    def __init__(self, model_path="models/skin_model.onnx"):
        self.model_path = model_path
        # Model henüz mevcut değil, simülasyon kullanıyoruz
    
    def predict(self, image: Image):
        """Deri tahmini yap (şimdilik simülasyon)"""
        return "Ciltte alerjik reaksiyon belirtisi görüldü." 