import onnxruntime as ort
import numpy as np
from PIL import Image
import os

class ChestPredictor:
    def __init__(self, model_path="models/chexnet_densenet121.onnx"):
        self.model_path = model_path
        self.session = None
        self.conditions = [
            "Atelectasis", "Cardiomegaly", "Consolidation", "Edema",
            "Effusion", "Emphysema", "Fibrosis", "Hernia", "Infiltration",
            "Mass", "Nodule", "Pleural_Thickening", "Pneumonia", "Pneumothorax"
        ]
        self.load_model()
    
    def load_model(self):
        """ONNX modelini yükle"""
        if os.path.exists(self.model_path):
            self.session = ort.InferenceSession(self.model_path)
        else:
            raise FileNotFoundError(f"Model dosyası bulunamadı: {self.model_path}")
    
    def preprocess_image(self, image: Image):
        """Görüntüyü model için hazırla"""
        image = image.convert('RGB')
        image = image.resize((224, 224))
        
        # Numpy array'e çevir
        img_array = np.array(image).astype(np.float32) / 255.0
        img_array = np.transpose(img_array, (2, 0, 1))
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image: Image):
        """Göğüs X-ray tahmini yap"""
        try:
            # Görüntüyü hazırla
            img_array = self.preprocess_image(image)
            
            # Tahmin yap
            input_name = self.session.get_inputs()[0].name
            output_name = self.session.get_outputs()[0].name
            prediction = self.session.run([output_name], {input_name: img_array})
            
            # Sonuçları işle
            return self.process_prediction(prediction[0])
            
        except Exception as e:
            raise Exception(f"Göğüs X-ray tahmin hatası: {str(e)}")
    
    def process_prediction(self, prediction):
        """Tahmin sonuçlarını işle"""
        results = {}
        for i, condition in enumerate(self.conditions):
            if i < len(prediction[0]):
                results[condition] = float(prediction[0][i])
        
        # En yüksek skorlu durumu döndür
        if results:
            max_condition = max(results, key=results.get)
            return f"Tespit edilen durum: {max_condition}"
        
        return "Normal göğüs X-ray" 