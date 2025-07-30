from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image as PILImage

class SkinPredictor:
    def __init__(self):
        self.model = load_model("models/skin_disease_model.h5")
        self.class_names = [
            "Actinic Keratosis",
            "Basal Cell Carcinoma",
            "Dermatofibroma",
            "Melanoma",
            "Nevus",
            "Pigmented Benign Keratosis",
            "Seborrheic Keratosis",
            "Squamous Cell Carcinoma",
            "Vascular Lesion"
        ]

    def predict(self, img):
        if isinstance(img, str):
            img = image.load_img(img, target_size=(75, 100))
        elif isinstance(img, PILImage.Image):
            img = img.resize((100, 75))
        else:
            raise ValueError("Geçersiz görüntü formatı")

        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        prediction = self.model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)[0]
        return self.class_names[predicted_class]
