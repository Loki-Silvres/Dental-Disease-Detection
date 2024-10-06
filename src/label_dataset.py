import os
import os.path as osp
import sys
import cv2 as cv
import numpy as np
from tqdm import tqdm

ds_path = "/home/loki/DentalObjectDetection/data/YOLO/test"

labels = sorted(os.listdir(osp.join(ds_path, "labels")))
images = sorted(os.listdir(osp.join(ds_path, "images")))

for label in tqdm(labels):
    img = cv.imread(osp.join(ds_path, "images", images[labels.index(label)]))
    IMG_H, IMG_W = img.shape[:2]
    with open(osp.join(ds_path, "labels", label), 'r') as r:
        lines = r.readlines()
        for line in lines:
            line = line.split()
            cls = int(line[0])
            line = line[1:]
            line = [float(i) for i in line]
            n_pts = len(line)//2
            pts = []
            for i in range(n_pts):
                x, y = line[i*2], line[i*2+1]
                x, y = x*IMG_W, y*IMG_H
                line[i*2], line[i*2+1] = x, y
                pts.append((x, y))

            PALETTE = [
                (220, 20, 60), (119, 11, 32), (0, 0, 142), (0, 0, 230), (106, 0, 228), 
                (0, 60, 100), (0, 80, 100), (0, 0, 70), (0, 0, 192), (250, 170, 30), 
                (100, 170, 30), (220, 220, 0), (175, 116, 175), (250, 0, 30), 
                (30, 144, 255), (0, 191, 255), (135, 206, 250), (70, 130, 180), (123, 104, 238),
                (72, 61, 139), (138, 43, 226), (148, 0, 211), (186, 85, 211), (255, 20, 147), 
                (255, 105, 180), (255, 160, 122), (255, 69, 0), (255, 99, 71), (218, 112, 214), 
                (238, 130, 238), (255, 222, 173)
            ]
            color = PALETTE[cls]
            pts = np.array(pts, np.int32)

            for i in range(len(pts) - 1):
                img = cv.line(img, tuple(pts[i]), tuple(pts[i + 1]), color = color, thickness = 2)
            
            img = cv.line(img, tuple(pts[-1]), tuple(pts[0]), color = color, thickness = 2)
            # print(f"Done for {label}")
            # cv.imshow("image", img)
            # if cv.waitKey(0) & 0xFF == ord('q'):
            #     cv.destroyAllWindows()
            #     exit()
            # offset = 5
            # img = cv.putText(img, labels[cls], (int(x-w/2- offset), int(y-h/2 - offset)), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    save_path = osp.join(ds_path, "visualized", images[labels.index(label)])
    img = cv.resize(img, (640, 640))
    cv.imwrite(save_path, img)