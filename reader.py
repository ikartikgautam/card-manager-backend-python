from PIL import Image
from pytesseract import pytesseract
import pandas as pd
import re
import cv2
import matplotlib.pyplot as plt
import numpy as np
from pytesseract import Output
import json
import imutils

# ------------- Global Functions ------------
path_to_tesserect = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'  # Tesserect Path


def extractText(fileName, type):

    cities = json.load(open('cities.json'))

    image_path = f'./files/{fileName}'
    org_image_path = f'./files/orignal/{fileName}'

    im = cv2.imread(org_image_path)
    if(type is 'Greyscale'):  # Run with greyscale image
        image = imutils.resize(im, width=1200)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # thresh = cv2.threshold(
        #     gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
        cv2.imwrite(image_path, gray)
    elif(type is 'Mixed_Not'):  # Run with greyscale and blacked image
        # im = cv2.imread(image_path)
        # image = imutils.resize(im, width=1200)
        image = cv2.resize(im, None, fx=3, fy=3)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        thresh = cv2.GaussianBlur(thresh, (7, 7), 0)
        bit_not = cv2.bitwise_not(thresh)
        cv2.imwrite(image_path, bit_not)
    elif(type is 'Mixed'):  # Run with greyscale and blacked image
        # im = cv2.imread(image_path)
        # image = imutils.resize(im, width=1200)
        image = cv2.resize(im, None, fx=3, fy=3)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        thresh = cv2.GaussianBlur(thresh, (7, 7), 0)
        cv2.imwrite(image_path, thresh)
    else:  # Run on original image
        cv2.imwrite(image_path, im)
        pass

    img = Image.open(image_path)
    pytesseract.tesseract_cmd = path_to_tesserect

    text = pytesseract.image_to_string(img)
    txt = pytesseract.image_to_data(img, output_type=Output.DICT)

    max_len = len(txt['text'])
    obj = []
    # Run a loop to create object with text and their respective word heights
    for i in range(0, max_len):
        for j in range(i+1, max_len):
            if txt['word_num'][j] <= txt['word_num'][i]:
                arr = txt['word_num'][i:j]
                word_arr = txt['text'][i:j]
                height_arr = txt['height'][i:j]
                if arr[0] == 1:
                    if ''.join(word_arr).strip():
                        obj.append({'word': word_arr, 'avg_ht': sum(
                            height_arr)/len(height_arr)})
                break

    max = {'content': [], 'height': -1}
    addr = []
    mobile = []
    email = []
    website = []

    # Determine highest
    for e in obj:
        line = ''
        for ele in e['word']:
            line += ele
            ele = ''.join(e for e in ele if e.isalnum())
            if ele.lower() in cities:
                addr = e['word']
        if e['avg_ht'] > max['height']:
            tempObj = {'content': e['word'], 'height': e['avg_ht']}
            max = tempObj
        mobile += getPhoneFromLine(line)
    for i in range(0, len(max['content'])):
        max['content'][i] = ''.join(
            e for e in max['content'][i] if e.isalnum())

    splitText = text.splitlines()

    for line in splitText:
        words = line.split(' ')
        words = list(map(lambda x: x.lower(), words))
        for word in words:
            pass
            if word not in ['', ' ']:
                mobile += [checkMobileNumber(word)
                           ] if checkMobileNumber(word) is not None else []
                email += [checkEmail(word)
                          ] if checkEmail(word) is not None else []
                website += [checkWebsite(word)
                            ] if checkWebsite(word) is not None else []
    # extractCompany(image_path)

    obj = {'mobile': mobile, 'website': website,
           'email': email, 'raw': splitText, 'company_name': ' '.join(max['content']), 'address': ' '.join(addr)}
    return obj


def getPhoneFromLine(line):
    tempArr = []
    nums = re.sub("[^0-9,]", "", line).split(',')
    for e in nums:
        tempArr += [checkMobileNumber(e)
                    ] if checkMobileNumber(e) is not None else []
    return tempArr


def extractCompany(filePath):
    # im = cv2.imread(filePath)
    # kernel = np.ones((10, 10), np.float32)/25
    # dst = cv2.filter2D(im, -1, kernel)
    # # plt.imshow(dst)
    # plt.imsave('files/test.png', dst)

    # img = Image.open('files/test.png')
    # pytesseract.tesseract_cmd = path_to_tesserect

    text = pytesseract.image_to_string(filePath)
    print(text)


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
    if re.search('\d{10}', word) or re.search('\+91-*\d{10}', word) or re.search('\+*91-*\d+-\d+', word):
        return word

# Fetch Website from word


def checkWebsite(word):
    if(re.search('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', word)):
        return word
