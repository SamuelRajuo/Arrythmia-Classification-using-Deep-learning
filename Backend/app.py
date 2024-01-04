import os
import numpy as np
from flask import Flask, request, render_template
from keras.models import load_model
from keras.preprocessing import image
from PIL import Image, ImageOps

app = Flask(__name__)
model = load_model("D:\ECG\ECG.h5")

@app.route("/")
def about():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/info")
def information():
    return render_template("info.html")

@app.route("/upload")
def test():
    return render_template("Predict.html")

@app.route("/predict", methods=["POST"])
def upload():
    if request.method == "POST":
        try:
            f = request.files['img']
            basepath = os.path.dirname(__file__)
            uploads_folder = os.path.join(basepath, "uploads")

            if not os.path.exists(uploads_folder):
                os.makedirs(uploads_folder)

            filepath = os.path.join(uploads_folder, f.filename)
            f.save(filepath)

            img = Image.open(filepath).convert("L")  # Convert to grayscale
            img = ImageOps.grayscale(img)
            img = img.resize((64, 64))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)

            # Ensure input has 3 channels (RGB) instead of 1 channel (grayscale)
            x = np.repeat(x, 3, axis=-1)

            pred_probabilities = model.predict(x)
            pred_class = np.argmax(pred_probabilities)
            
            index = ['Left Bundle Branch Block', 'Normal', 'Premature Atrial Contraction', 'Premature Ventricular Contractions', 'Right Bundle Branch Block', 'Ventricular Fibrillation']
            result = str(index[pred_class])

            return result

        except Exception as e:
            print("Error:", e)
            return "Error occurred during prediction."

    return "Please use a POST request to upload an image."

if __name__ == "__main__":
    app.run(debug=True)
