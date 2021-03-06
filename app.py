from flask import Flask, render_template, url_for, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from PIL import Image
from pytesseract import pytesseract
import reader as rd
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# -------------------------


@app.route('/testGet', methods=['GET'])
def getGet():
    return 'Get request is working count='+request.args['count']


@app.route('/testPost', methods=['POST'])
def getPost():
    return 'Post request is working count='+request.form['count']


@cross_origin()
@app.route('/uploadImage', methods=['POST'])
def uploadImage():
    file = request.files['file']
    fileName = secure_filename(file.filename)
    file.save(f'./files/orignal/{fileName}')
    obj1 = rd.extractText(fileName, 'None')
    obj2 = rd.extractText(fileName, 'Mixed_Not')
    obj3 = rd.extractText(fileName, 'Mixed')
    obj4 = rd.extractText(fileName, 'Greyscale')
    os.remove(f'./files/{fileName}')
    os.remove(f'./files/orignal/{fileName}')
    return {'success': True, 'meta': [obj1, obj2, obj3, obj4], 'msg': 'Card Scanned Successfully'}
    # return {'success': True, 'meta': [obj3], 'msg': 'Card Scanned Successfully'}
# -------------------------


if __name__ == "__main__":
    app.run(debug=True)
