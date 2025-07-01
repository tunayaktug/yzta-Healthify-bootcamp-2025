from fastapi import APIRouter, UploadFile, File
from models.predictor import predict_image
from fastapi import HTTPException

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

from PIL import UnidentifiedImageError

@router.post("/")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        result = predict_image(image_bytes)
        return {"result": result}
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))