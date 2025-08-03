from tensorflow.keras.models import load_model
import numpy as np

class EyePredictor:
    def __init__(self, model_path="models/vgg16_1.h5"):
        self.model = load_model(model_path)

    def predict(self, image):
        img = image.resize((224, 224))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)
        predictions = self.model.predict(img)
        classes = [
            "Normal",
            "Diabetes",
            "Glaucoma",
            "Cataract",
            "Age related Macular Degeneration",
            "Hypertension",
            "Pathological Myopia",
            "Other diseases/abnormalities"
        ]
        pred_index = np.argmax(predictions)
        return classes[pred_index]
