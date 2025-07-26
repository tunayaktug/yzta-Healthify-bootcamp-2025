import onnxruntime as ort
import numpy as np
from PIL import Image
import os

class FracturePredictor:
    def __init__(self, model_path="models/yolov7.onnx"):
        self.model_path = model_path
        self.session = None
        self.fracture_types = [
            "Kırık", "Çatlak", "Kompound Kırık", "Spiral Kırık", 
            "Transvers Kırık", "Oblik Kırık", "Kırık Yok"
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
        
        # YOLOv7 için görüntü boyutunu ayarla (model gereksinimlerine göre)
        # Bu kısım model spesifikasyonuna göre değiştirilmeli
        target_size = (640, 640)  # YOLOv7 için tipik boyut
        image = image.resize(target_size)
        
        # Numpy array'e çevir
        img_array = np.array(image).astype(np.float32) / 255.0
        img_array = np.transpose(img_array, (2, 0, 1))
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image: Image):
        """Kırık tahmini yap"""
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
            raise Exception(f"Kırık tahmin hatası: {str(e)}")
    
    def process_prediction(self, prediction):
        """Tahmin sonuçlarını işle"""
        # YOLOv7 çıktılarını işle
        try:
            # YOLOv7 çıktısı genellikle [batch, num_detections, 6] formatındadır
            # 6 değer: [x, y, w, h, confidence, class_id]
            if len(prediction.shape) >= 2:
                # En yüksek güvenilirlik skoruna sahip tespiti bul
                max_confidence_idx = np.argmax(prediction[:, 4]) if prediction.shape[1] > 4 else 0
                confidence = float(prediction[max_confidence_idx, 4]) if prediction.shape[1] > 4 else 0.0
                
                # Sınıf ID'sini al (eğer varsa)
                class_id = int(prediction[max_confidence_idx, 5]) if prediction.shape[1] > 5 else 0
                
                if confidence > 0.5:
                    # Sınıf ID'sine göre kırık türünü belirle
                    fracture_type = self.fracture_types[class_id] if class_id < len(self.fracture_types) else "Kırık"
                    return f"{fracture_type} tespit edildi (Güvenilirlik: {confidence:.2f})"
                else:
                    return "Kırık tespit edilmedi"
            else:
                return "Kırık analizi tamamlandı"
                
        except Exception as e:
            return f"Kırık analizi tamamlandı (İşleme hatası: {str(e)})" 