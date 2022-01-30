from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
from PIL import Image
from pytesseract import pytesseract
import re
import reader as rd

app = Flask(__name__)

# -------------------------

@app.route('/testGet', methods=['GET'])
def getGet():
    return 'Get request is working count='+request.args['count']

@app.route('/testPost', methods=['POST'])
def getPost():
    return 'Post request is working count='+request.form['count']

@app.route('/uploadImage', methods=['POST'])
def uploadImage():
    file = request.files['file']
    fileName = secure_filename(file.filename)
    file.save(f'./files/{fileName}')
    rd.extractText(fileName)
    return fileName

# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
