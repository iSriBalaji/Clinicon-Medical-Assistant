import cv2
import os
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
aadhar_path = os.path.join(os.path.dirname(__file__),"aadhar.png")
img = cv2.imread(aadhar_path)

custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(img, config=custom_config)
print(text)
