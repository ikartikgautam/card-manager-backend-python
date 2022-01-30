from PIL import Image
from pytesseract import pytesseract
import pandas as pd
import re

# ------------- Global Functions ------------
path_to_tesserect = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'  # Tesserect Path


def extractText(fileName):
    image_path = f'./files/{fileName}'
    img = Image.open(image_path)
    pytesseract.tesseract_cmd = path_to_tesserect

    text = pytesseract.image_to_string(img)
    splitText = text.splitlines()
    mobile = []
    email = []
    print(splitText)
    for line in splitText:
        words = line.split(' ')
        words = list(map(lambda x: x.lower(), words))
        for word in words:
            if word not in ['', ' ']:
                mobile += [checkMobileNumber(word)
                           ] if checkMobileNumber(word) is not None else []
                email += [checkEmail(word)
                          ] if checkEmail(word) is not None else []
    print('mobile - ', mobile)
    print('email - ', email)
    pass


def checkName(words):
    female_names = pd.read_csv(
        './datasets/Indian-Female-Names.csv')['name'].to_list()
    male_names = pd.read_csv(
        './datasets/Indian-Male-Names.csv')['name'].to_list()
    for ele in words:
        if ele in male_names or ele in female_names:
            print('Found Name - ', ele)

# Fetch Email from word


def checkEmail(word):
    if(re.search('[a-zA-Z0-9.]+@[a-zA-Z0-9.]+', word)):
        return word

# Fetch Mobile from word


def checkMobileNumber(word):
    if(re.search('\d{10}', word)):
        return word
