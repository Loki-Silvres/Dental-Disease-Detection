from ultralytics import YOLO
import cv2 as cv
import sys
sys.path.append("/home/loki/B3RB_ENIAC")

model = YOLO('/home/loki/DentalObjectDetection/runs/segment/train2/weights/best.pt')
results = model.train(data="/home/loki/DentalObjectDetection/data/YOLO/data.yaml", batch = 4, epochs=5, lr0=0.000001, freeze = 6, iou = 0.80, conf = 0.50, optimizer = "AdamW", dropout = 0.5, plots = True)

# results = model.val(data = '/home/loki/DentalObjectDetection/data/YOLO/data.yaml')
# yolo segment train data=/home/loki/DentalObjectDetection/data/YOLO/data.yaml model=/home/loki/DentalObjectDetection/runs/segment/train3/weights/last.pt epochs=50 batch=8 imgsz=640 freeze=6 lr0=0.00001 optimizer="AdamW" dropout=0.5 cos_lr = True resume = True
# yolo segment val data=/home/loki/DentalObjectDetection/data/YOLO/data.yaml model = /home/loki/DentalObjectDetection/runs/segment/train3/weights/best.pt
# yolo segment predict model = /home/loki/DentalObjectDetection/runs/segment/train3/weights/best.pt source = '/home/loki/DentalObjectDetection/data/YOLO/valid/images'  show_labels = False show_boxes=False save=True