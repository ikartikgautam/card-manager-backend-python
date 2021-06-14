from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
from PIL import Image
from pytesseract import pytesseract
import re
app = Flask(__name__)

def convert_task(n):
    path_to_tesserect = r"D:\\Tesserect\\tesseract"
    image_path = "D:\\TextFromImage\\" + n
    img = Image.open(image_path)
    pytesseract.tesseract_cmd = path_to_tesserect
    text = pytesseract.image_to_string(img)
    #removing lines
    text2 = text.splitlines()

    final = []

    #removing spaces
    for ele in text2:
        if ele.strip():
            final.append(ele)
        print(final)
    email = []
    #getting out email
    for s in final:
        if(re.search(r'[\w\.-]+@[\w\.-]+',s)):
            email.append(s)
    print(email)

#getting out phone number
    phoneNumber = []
    for s in final:
        if(s[0] == '+'):
            phoneNumber.append(s)
    print(phoneNumber)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload', methods = ['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        convert_task(secure_filename(f.filename))
        return 'file uploaded successfully' 
    elif request.method == 'GET':
        return render_template("upload.html")
    return "Some error occured"


if __name__ == "__main__":
    app.run(debug=True)

