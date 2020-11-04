from flask import Flask, redirect, url_for, render_template, request, jsonify
from werkzeug.utils import secure_filename

from fastai.learner import load_learner
from fastai.vision.all import PILImage, Path

import os

app = Flask(__name__)

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]
app.config["IMAGE_UPLOADS"] = 'static/img'

img_path = Path(app.config["IMAGE_UPLOADS"])

# Load the trained classifier
learn = load_learner('/models/base.pkl')
# Get the classes, that have been used to train
classes = learn.dls.vocab

def predict_single(fn):
    # Get the prediction for a particular image, from its path
    prediction = learn.predict(fn)
    # Get label and confidence for that label
    class_no = prediction[1].item() # from tensor
    label = classes[class_no]
    conf = prediction[2][class_no].item()
    return {
        'label': label,
        'confidence': conf
    }

def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            
            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(image.filename)

            filepath = (img_path/filename)
            print(f'Save image to: {filepath.absolute()}')
            image.save(filepath)

            prediction = predict_single(filepath)
            print(prediction)

            return render_template("/predict.html", filepath=filepath, prediction=prediction)

    return render_template("/upload.html")

@app.route('/predict', methods=['POST', 'GET'])
def predict():#image, prediction):
    
    return render_template('predict.html')#, filepath=filepath, prediction=prediction)


if __name__ == "__main__":
    app.run(debug = True)