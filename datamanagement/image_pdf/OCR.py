import cv2
import numpy as np
import pytesseract
from fpdf import FPDF
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir('C:\\Users\\anagh\\PycharmProjects\\Case_Study\\Blurr_resume')
             if isfile(join('C:\\Users\\anagh\\PycharmProjects\\Case_Study\\Blurr_resume', f))]
for file in onlyfiles:
    image_file = join('C:\\Users\\anagh\\PycharmProjects\\Case_Study\\Blurr_resume',file)
    img = cv2.imread(image_file)
    print(file)

    def ocr_core(img): #convert to text
        text = pytesseract.image_to_string(img)
        return text
    def image_resize(image): #resize image
        return cv2.resize(image, None, fx=3, fy=3)
    def get_greyscale(image):#calculate greyscale
        return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    def thresholding(image): #Calculate threshold
        th = cv2.adaptiveThreshold(image, 300, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 11)
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        or_image = cv2.bitwise_or(image, closing)
        return or_image

    img = image_resize(img)
    img = get_greyscale(img)
    img = thresholding(img)
    print(ocr_core(img))
    file1 = open("1.txt", "w")
    file1.write(ocr_core(img))
    file1.close()
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('ArialUnicode', fname='Arial-Unicode-Regular.ttf', uni=True)#download & keep the file in the same location
    pdf.set_font('ArialUnicode', '', 11)
    f = open("1.txt", "r")
    for x in f:
        pdf.cell(200, 10, txt = x, ln=1, align='L')
    pdf.output(f'C:\\Users\\anagh\\PycharmProjects\\Case_Study\\newPDF\\'+file+'.pdf')#save as pdf
    f.close()
