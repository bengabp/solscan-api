import pytesseract
import cv2 as cv
from PIL import Image
import pandas as pd
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_table():
    img = Image.open(r"C:\Users\bengabp\Documents\IT\UKTeam\SolanaScan\datasets\data_page.png")
    results = pytesseract.image_to_data(img, lang="eng")
    print(results)


extract_table()
