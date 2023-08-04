import easyocr
import cv2
import numpy as np

model_svm = cv2.ml.SVM_load('model/SVM/svm.xml')
model_knn = cv2.ml.KNearest.load("model/kNN/knn_1.xml")

# Dinh nghia cac ky tu tren bien so
char_list =  '0123456789ABCDEFGHKLMNPRSTUVXYZ'

# Cau hinh tham so cho model SVM
digit_w = 30 # Kich thuoc ki tu
digit_h = 60 # Kich thuoc ki tu

# Ham fine tune bien so, loai bo cac ki tu khong hop ly
def fine_tune(lp):
    newString = ""
    for i in range(len(lp)):
        if lp[i] in char_list:
            newString += lp[i]
    return newString

def sort_contours(cnts):

    reverse = False
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return cnts

def recognition(model_name, img):
    if not model_name:
        return None
    elif model_name == 'OCR':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 3)
        binary = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 2)
        reader = easyocr.Reader(['ch_sim',  'en'])
        prediction = reader.readtext(binary, detail=0)
        return fine_tune(prediction[0])
    else:
        roi = img
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 3)
        binary = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 2)
        kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        thre_mor = cv2.dilate(binary, kernel3, iterations = 1)
        cont, _  = cv2.findContours(thre_mor, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        plate_info = ''
        for c in sort_contours(cont):
            (x, y, w, h) = cv2.boundingRect(c)
            ratio = h/w
            if 1<=ratio<=3.5:
                if h/roi.shape[0]>=0.55:
                    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    curr_num = thre_mor[y:y+h,x:x+w]
                    curr_num = cv2.resize(curr_num, dsize=(digit_w, digit_h))
                    _, curr_num = cv2.threshold(curr_num, 30, 255, cv2.THRESH_BINARY)
                    curr_num = np.array(curr_num,dtype=np.float32)
                    curr_num = curr_num.reshape(-1, digit_w * digit_h)

                    if model_name == 'SVM':
                        result = model_svm.predict(curr_num)[1]
                        result = int(result[0, 0])

                    elif model_name == 'kNN':
                        result = model_knn.findNearest(curr_num, k=1)[1]
                        result = int(result[0, 0])

                    if result<=9:
                        result = str(result)
                    else:
                        result = chr(result)

                    plate_info +=result
        return fine_tune(plate_info)