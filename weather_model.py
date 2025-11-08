import os
import numpy as np
from tensorflow.keras.models import load_model

def predict_weather_from_image(img_path):
    import cv2  # lazy import to avoid Streamlit Cloud crash
    MODEL_PATH = "vgg19.h5"
    model = load_model(MODEL_PATH)
    classes = ["cloudy","foggy","rainy","shine","sunrise"]

    img = cv2.imread(img_path)
    img = cv2.resize(img, (150,150))
    img = np.expand_dims(img, axis=0)/255.0
    pred = model.predict(img)
    class_idx = np.argmax(pred)
    return classes[class_idx], float(pred[0][class_idx])
