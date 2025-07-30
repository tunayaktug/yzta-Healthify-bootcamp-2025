from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import UnidentifiedImageError, Image
import io
import os
import sys

# Models klasörünü Python path'ine ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

from chest_predictor import ChestPredictor
from fracture_predictor import FracturePredictor
from skin_predictor import SkinPredictor
from eye_predictor import EyePredictor
from nail_predictor import NailPredictor
from hair_predictor import HairPredictor

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

# Model yolları
MODEL_PATHS = {
    "skin": "models/skin_model.onnx",
    "eye": "models/eye_model.onnx", 
    "nail": "models/nail_model.onnx",
    "hair": "models/hair_model.onnx",
    "chest": "models/chexnet_densenet121.onnx",
    "fracture": "models/yolov7.onnx"
}

# Predictor sınıfları
predictors = {}

@router.post("/{category}")
async def predict_image(category: str, file: UploadFile = File(...)):
    """
    Belirtilen kategori için görüntü tahmini yapar
    """
    try:
        # Dosya türünü kontrol et
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Sadece görüntü dosyaları kabul edilir")
        
        # Görüntüyü oku
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Kategori kontrolü
        if category not in MODEL_PATHS:
            raise HTTPException(status_code=400, detail="Geçersiz kategori")
        
        # Model dosyasının varlığını kontrol et
        model_path = MODEL_PATHS[category]
        if not os.path.exists(model_path):
            # Model yoksa simülasyon sonucu döndür
            return {
                "category": category,
                "prediction": f"{category} analizi simülasyonu tamamlandı",
                "confidence": 0.85,
                "recommendations": get_recommendations(category, "simulation")
            }
        
        # Kategoriye göre tahmin yap
        if category == "chest":
            result = await predict_chest_xray(image)
        elif category == "fracture":
            result = await predict_fracture_xray(image)
        elif category == "skin":
            result = await predict_skin(image)
        elif category == "eye":
            result = await predict_eye(image)
        elif category == "nail":
            result = await predict_nail(image)
        elif category == "hair":
            result = await predict_hair(image)
        else:
            # Diğer kategoriler için genel tahmin
            result = await predict_general(image, category)
        
        return {
            "category": category,
            "prediction": result,
            "confidence": 0.85,
            "recommendations": get_recommendations(category, result)
        }
        
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Geçersiz görüntü dosyası")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")

async def predict_chest_xray(image: Image):
    """
    Göğüs X-ray görüntüsü için tahmin
    """
    try:
        # ChestPredictor sınıfını kullan
        if "chest" not in predictors:
            predictors["chest"] = ChestPredictor()
        
        result = predictors["chest"].predict(image)
        return result
        
    except Exception as e:
        raise Exception(f"Göğüs X-ray tahmin hatası: {str(e)}")

async def predict_fracture_xray(image: Image):
    """
    Kırık X-ray görüntüsü için tahmin
    """
    try:
        # FracturePredictor sınıfını kullan
        if "fracture" not in predictors:
            predictors["fracture"] = FracturePredictor()
        
        result = predictors["fracture"].predict(image)
        return result
        
    except Exception as e:
        raise Exception(f"Kırık X-ray tahmin hatası: {str(e)}")

async def predict_skin(image: Image):
    """
    Deri görüntüsü için tahmin
    """
    try:
        if "skin" not in predictors:
            predictors["skin"] = SkinPredictor()
        
        result = predictors["skin"].predict(image)
        return result
        
    except Exception as e:
        raise Exception(f"Deri tahmin hatası: {str(e)}")

async def predict_eye(image: Image):
    """
    Göz görüntüsü için tahmin
    """
    try:
        if "eye" not in predictors:
            predictors["eye"] = EyePredictor()
        
        result = predictors["eye"].predict(image)
        return result
        
    except Exception as e:
        raise Exception(f"Göz tahmin hatası: {str(e)}")

async def predict_nail(image: Image):
    """
    Tırnak görüntüsü için tahmin
    """
    try:
        if "nail" not in predictors:
            predictors["nail"] = NailPredictor()
        
        result = predictors["nail"].predict(image)
        return result
        
    except Exception as e:
        raise Exception(f"Tırnak tahmin hatası: {str(e)}")

async def predict_hair(image: Image):
    """
    Saç görüntüsü için tahmin
    """
    try:
        if "hair" not in predictors:
            predictors["hair"] = HairPredictor()
        
        result = predictors["hair"].predict(image)
        return result
        
    except Exception as e:
        raise Exception(f"Saç tahmin hatası: {str(e)}")

async def predict_general(image: Image, category: str):
    """
    Genel kategoriler için tahmin
    """
    return f"{category} analizi tamamlandı"

def get_recommendations(category: str, result: str):
    """
    Kategoriye göre öneriler döndür
    """
    recommendations = {
        "chest": [
            "Sonuçları doktorunuzla paylaşın",
            "Düzenli kontroller yaptırın",
            "Sigara kullanıyorsanız bırakın"
        ],
        "fracture": [
            "Acil servise başvurun",
            "Hareket etmeyin",
            "Soğuk kompres uygulayın"
        ],
        "skin": [
            "Güneş koruyucu kullanın",
            "Düzenli cilt kontrolü yapın",
            "Doktor kontrolüne gidin"
        ],
        "eye": [
            "Göz doktoruna başvurun",
            "Ekran süresini sınırlayın",
            "Düzenli göz kontrolü yapın"
        ],
        "nail": [
            "Tırnak bakımına dikkat edin",
            "Doktor kontrolüne gidin",
            "Beslenmenizi gözden geçirin"
        ],
        "hair": [
            "Saç bakımına dikkat edin",
            "Dermatoloğa başvurun",
            "Beslenmenizi gözden geçirin"
        ]
    }
    
    return recommendations.get(category, ["Doktor kontrolüne başvurun"])


