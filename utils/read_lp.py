import easyocr
reader = easyocr.Reader(['ch_sim','en'])

char_list =  '0123456789ABCDEFGHKLMNPRSTUVXYZ'
def format(lp):
    newString = ""
    for i in range(len(lp)):
        if lp[i] in char_list:
            newString += lp[i]
    return newString
def read_license_plate(lp):
    detections = reader.readtext(lp)
    for detection in detections:
        bbox, text, score = detection
        if format(text):
            return format(text), score

    return None, None