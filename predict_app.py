# * Remember to: set FLASK_APP=predict_app.py
# * Type flask run to run
# ? Type flask run --host=0.0.0.0 to set the IP to it and let others access it
# ! Only set host when you trust the outside access-er
import base64
import io
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import Flask, request, jsonify
app = Flask(__name__)


def get_model():
    global model
    model = load_model(r'models/fine-tune_dogs_vs_cats.h5')
    print("* Load successfully!")


def preprocess_image(image, target_size):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image


print('* Loading Keras model')
get_model()


@app.route('/')
def index():
    return 'Hello World'


@app.route('/predict', methods=['POST'])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(224, 224))

    prediction = model.predict(processed_image).tolist()

    response = {
        'prediction': {
            'dog': prediction[0][0],
            'cat': prediction[0][1]
        }
    }

    return jsonify(response)
