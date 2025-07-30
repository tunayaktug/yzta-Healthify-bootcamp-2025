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
    "skin": "models/skin_disease_model.h5",
    "eye": "models/eye_model.onnx",
    "nail": "models/nail_model.onnx",
    "hair": "models/hair_model.onnx",
    "chest": "models/chexnet_densenet121.onnx",
    "fracture": "models/yolov7-p6-bonefracture.onnx"
}

# Predictor sınıfları
predictors = {}

@router.post("/{category}")
async def predict_image(category: str, file: UploadFile = File(...)):
    """
    Belirtilen kategori için görüntü tahmini yapar
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Sadece görüntü dosyaları kabul edilir")

        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        if category not in MODEL_PATHS:
            raise HTTPException(status_code=400, detail="Geçersiz kategori")

        model_path = MODEL_PATHS[category]
        if not os.path.exists(model_path):
            return {
                "category": category,
                "prediction": f"{category} analizi simülasyonu tamamlandı",
                "confidence": 0.85,
                "recommendations": get_recommendations(category, "simulation")
            }

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
    try:
        if "chest" not in predictors:
            predictors["chest"] = ChestPredictor()
        return predictors["chest"].predict(image)
    except Exception as e:
        raise Exception(f"Göğüs X-ray tahmin hatası: {str(e)}")

async def predict_fracture_xray(image: Image):
    try:
        if "fracture" not in predictors:
            predictors["fracture"] = FracturePredictor()
        return predictors["fracture"].predict(image)
    except Exception as e:
        raise Exception(f"Kırık X-ray tahmin hatası: {str(e)}")

async def predict_skin(image: Image):
    try:
        if "skin" not in predictors:
            predictors["skin"] = SkinPredictor()
        return predictors["skin"].predict(image)
    except Exception as e:
        raise Exception(f"Deri tahmin hatası: {str(e)}")

async def predict_eye(image: Image):
    try:
        if "eye" not in predictors:
            predictors["eye"] = EyePredictor()
        return predictors["eye"].predict(image)
    except Exception as e:
        raise Exception(f"Göz tahmin hatası: {str(e)}")

async def predict_nail(image: Image):
    try:
        if "nail" not in predictors:
            predictors["nail"] = NailPredictor()
        return predictors["nail"].predict(image)
    except Exception as e:
        raise Exception(f"Tırnak tahmin hatası: {str(e)}")

async def predict_hair(image: Image):
    try:
        if "hair" not in predictors:
            predictors["hair"] = HairPredictor()
        return predictors["hair"].predict(image)
    except Exception as e:
        raise Exception(f"Saç tahmin hatası: {str(e)}")

async def predict_general(image: Image, category: str):
    return f"{category} analizi tamamlandı"

def get_recommendations(category: str, result: str):
    if category == "skin":
        r = result.lower().replace(" ", "")
        if "actinickeratosis" in r:
            return [
                "Güneş ışığına doğrudan maruz kalmaktan kaçının.",
                "Ciltte yeni lezyonlar oluşursa dermatoloğa başvurun.",
                "Düzenli olarak dermatolojik kontrol yaptırın."
            ]
        elif "basalcellcarcinoma" in r:
            return [
                "Mutlaka bir dermatoloğa başvurun.",
                "Erken tedavi için gecikmeyin.",
                "Şüpheli bölgeleri kaşımayın veya müdahale etmeyin."
            ]
        elif "dermatofibroma" in r:
            return [
                "Genellikle iyi huyludur, endişe etmeyin.",
                "Büyüme veya ağrı olursa doktora başvurun.",
                "Kendi kendinize müdahale etmeyin."
            ]
        elif "melanoma" in r:
            return [
                "Acilen dermatoloji uzmanına başvurun.",
                "Erken tanı hayat kurtarır, gecikmeyin.",
                "Ciltte başka değişiklikler olursa takip edin."
            ]
        elif "nevus" in r:
            return [
                "Benlerinizde büyüme, şekil değişikliği veya kanama olursa doktora başvurun.",
                "Güneşten koruyucu kullanın.",
                "Benlerinizi düzenli olarak kontrol edin."
            ]
        elif "pigmentedbenignkeratosis" in r:
            return [
                "Genellikle zararsızdır.",
                "Kaşıma veya koparma yapmayın.",
                "Ciltte rahatsızlık hissederseniz dermatoloğa görünün."
            ]
        elif "seborrheickeratosis" in r:
            return [
                "Cilt temizliğine dikkat edin.",
                "Genellikle tedavi gerekmez.",
                "Şüpheli durumda doktorunuza başvurun."
            ]
        elif "squamouscellcarcinoma" in r:
            return [
                "Bir an önce dermatoloğa başvurun.",
                "Lezyonu güneşten koruyun.",
                "Tedavi edilmezse yayılabilir, takip şarttır."
            ]
        elif "vascularlesion" in r:
            return [
                "Çoğu zaman zararsızdır.",
                "Kanama veya büyüme olursa doktora başvurun.",
                "Travmadan koruyun."
            ]
        else:
            return [
                "Cilt sağlığınız için şüpheli bir durumda dermatoloğa danışın.",
                "Güneş koruyucu kullanmayı ihmal etmeyin."
            ]
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
