import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils.detection import detection
from utils.recognition import recognition

def main():
    st.title("License Plate Recognition")
    uploaded_image = st.file_uploader("Choose an image file", type=["jpg", "png", "jpeg"])
    detection_opt = st.selectbox("Detection model", ["WPOD-NET", "YOLOv8"])
    recognition_opt = st.selectbox("Recognition model:", ["OCR", "SVM", "kNN"])

    if uploaded_image is not None:
        if st.button("Read Plate"):
            img_bytes = uploaded_image.read()
            nparr = np.frombuffer(img_bytes, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            cropped_img = detection(detection_opt, img_np)
            lp_text = recognition(recognition_opt, cropped_img)
            st.write(f"<div style='font-size: 50px; text-align: center;'>{lp_text}</div>", unsafe_allow_html=True)
            st.image(uploaded_image, caption="Uploaded image", use_column_width=True)
if __name__ == "__main__":
    main()
