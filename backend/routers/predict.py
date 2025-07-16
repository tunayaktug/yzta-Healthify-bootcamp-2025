from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import UnidentifiedImageError
# from models.nail_predictor import predict_nail_image  # Tırnak modeli kaldırıldı

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

# Tırnak endpointi kaldırıldı
