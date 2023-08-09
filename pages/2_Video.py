import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
from utils.write_csv import write_csv
from utils.read_lp import read_license_plate
from component.page_meta import page_meta

page_meta(page_title='Video', page_icon='🎞️')
model = YOLO('model/YOLOv8/best.pt')

uploaded_video = st.file_uploader('Choose an image file', type=['mp4', 'mov'])

if uploaded_video is not None:
    if st.button('Read Plate'):
        video_data = uploaded_video.read()

        temp_file = "temp_video.mp4"
        with open(temp_file, "wb") as f:
            f.write(video_data)

        cap = cv2.VideoCapture(temp_file)
        results = {}
        frame_nmr = -1
        ret = True
        while ret:
            frame_nmr += 1
            ret, frame = cap.read()
            if ret:
                results[frame_nmr] = {}
                license_plates = model(frame)[0]
                for license_plate in license_plates.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = license_plate
                    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]
                    gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    blur = cv2.medianBlur(gray, 3)
                    lp = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 2)
                    license_plate_text, license_plate_text_score = read_license_plate(lp)
                    if license_plate_text is not None:
                        results[frame_nmr]= {'license_plate': {'bbox': [x1, y1, x2, y2],
                                                            'text': license_plate_text,
                                                            'bbox_score': score,
                                                            'text_score': license_plate_text_score}}
        write_csv(results, './test.csv')
        if 'data.csv' in os.listdir():
            with open('data.csv', 'rb') as file:
                st.download_button("Tải xuống dữ liệu", data=file, mime='text/csv', file_name='data.csv')
