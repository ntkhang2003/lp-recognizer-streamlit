import cv2
from ultralytics import YOLO
from model.WPOD.lib import load_model, detect_lp, im2single

# Load model LP detection
wpod_net_path = "model/WPOD/wpod-net_update1.json"
wpod_net = load_model(wpod_net_path)

# Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
Dmax = 608
Dmin = 288
def detection(model_name, image):
    if not model_name:
        return None
    elif model_name == 'YOLOv8':
        model = YOLO('model/YOLOv8/best.pt')
        img = image
        res = model(img)
        res_plotted = res[0].plot()
        t = res[0].boxes.xyxy
        t1 = t.cpu().numpy()
        x1 = int(t1[0][0])
        y1 = int(t1[0][1])
        x2 = int(t1[0][2])
        y2 = int(t1[0][3])
        cropped_img = res_plotted[y1:y2, x1:x2]
        cropped_img = cv2.resize(cropped_img, (470, 110))
        return cropped_img
    elif model_name == 'WPOD-NET':
        img = image
        ratio = float(max(img.shape[:2])) / min(img.shape[:2])
        side = int(ratio * Dmin)
        bound_dim = min(side, Dmax)

        _ , LpImg, lp_type = detect_lp(wpod_net, im2single(img), bound_dim, lp_threshold=0.5)
        LpImg[0] = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))
        return LpImg[0]