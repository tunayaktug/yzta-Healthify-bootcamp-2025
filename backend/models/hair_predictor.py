from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

class HairPredictor:
    def __init__(self):
        # Burada h5 dosyasını yüklüyoruz
        self.model = load_model("models/VGG16-Final.h5")
        self.class_names = [
            'Alopecia Areata',
            'Contact Dermatitis',
            'Folliculitis',
            'Head Lice',
            'Lichen Planus',
            'Male Pattern Baldness',
            'Psoriasis',
            'Seborrheic Dermatitis',
            'Telogen Effluvium',
            'Tinea Capitis'
        ]

    def predict(self, img):
        img = img.resize((224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        prediction = self.model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)[0]
        return self.class_names[predicted_class]
