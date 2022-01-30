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
    print(splitText)
    for line in splitText:
        words = line.split(' ')
        words = list(map(lambda x: x.lower(), words))
        # print(words)
        # checkName(words)
        # checkEmail(words)
        # print(line)
        for word in words:
            if word not in ['', ' ']:
                # mobile += [checkMobileNumber(word)
                #            ] if checkMobileNumber(word) is not None else []
                print(checkEmail(word))
    print(mobile)
    pass


def checkName(words):
    female_names = pd.read_csv(
        './datasets/Indian-Female-Names.csv')['name'].to_list()
    male_names = pd.read_csv(
        './datasets/Indian-Male-Names.csv')['name'].to_list()
    for ele in words:
        if ele in male_names or ele in female_names:
            print('Found Name - ', ele)


def checkEmail(word):
    print(word)
    re.search()
    pass
    # print('-->')
    # for ele in words:
    #     re.search(
    #         '/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/', ele)


def checkMobileNumber(word):
    if(re.search('\d{10}', word)):
        return word
