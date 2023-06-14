from flask import Flask,render_template,request
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image
app = Flask(__name__)

app.config['INITIAL_FILE_UPLOADS'] = 'static/images/uploads'
app.config['EXISTNG_FILE'] = 'static/images/original'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        file_upload = request.files['file_upload']
        filename = file_upload.filename
        uploaded_image = Image.open(file_upload).resize((250,160))
        uploaded_image = uploaded_image.convert('RGB')
        uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))
        print(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))
        original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'))
        uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))
        original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
        (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
        diff = (diff * 255).astype("uint8")
        if round(score*100,2)>50:
            res="Real"
        else:
            res="Fake"
        return render_template('index.html',pred=str(round(score*100,2)) + '%' + ' correct',result=res)


if __name__=="__main__":
    app.run(debug=True)