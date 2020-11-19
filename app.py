from flask import Flask, redirect, url_for, render_template, request, jsonify
from werkzeug.utils import secure_filename

from fastai.learner import load_learner
from fastai.vision.all import PILImage, Path, image2tensor

import os

app = Flask(__name__)

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]
app.config["IMAGE_UPLOADS"] = 'static/img'

img_path = Path(app.config["IMAGE_UPLOADS"])
ratio = 1.6

# Load the trained classifier
learn = load_learner('models/base.pkl')
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

@app.route("/take", methods=["GET", "POST"])
def take():
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

            filepath = os.path.join(app.config["IMAGE_UPLOADS"], filename)
            image = PILImage.create(image)

            prediction = predict_single(image)
            print(prediction)

            return render_template("/predict.html", prediction = prediction)

    return render_template("take.html")

fake_pred = {'label': 'correct', 'confidence': 0.5684}

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:

            """image = request.files["image"]
                        
            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(image.filename)

            filepath = os.path.join(app.config["IMAGE_UPLOADS"], filename)
            image = PILImage.create(image)

            prediction = predict_single(image)
            print(prediction)"""

            print('test')
            return jsonify({"render_template": "/predict.html"})
            #return redirect("/predict")

    return render_template("/upload.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    return render_template("/predict.html", prediction = fake_pred)

if __name__ == "__main__":
    app.run(debug = True)