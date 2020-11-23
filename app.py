from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename

from fastai.learner import load_learner
from fastai.vision.all import PILImage, Path

app = Flask(__name__)
CORS(app, support_credentials=True)

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]
app.config["IMAGE_UPLOADS"] = 'static/img'

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
    return render_template("take.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template("/upload.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
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

            filepath = Path(app.config["IMAGE_UPLOADS"]) / filename
            image = PILImage.create(image)
            image.save(f'static/img/{filename}') ## to check if correct image is received

            prediction = predict_single(image)
            print(prediction)
        res = make_response(jsonify(prediction), 200)
        return res

    return "There was a mistake, please try again."

if __name__ == "__main__":
    app.run()