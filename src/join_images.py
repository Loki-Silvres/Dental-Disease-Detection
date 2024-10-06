import os
import os.path as osp
import cv2 as cv
import numpy as np
from tqdm import tqdm


def join_images(ds_paths, save_dir = None):

    image_groups = [sorted(os.listdir(ds_path)) for ds_path in ds_paths]
    folder_size = len(image_groups[0])
    folder_names = [ds_path.split("/")[-1] for ds_path in ds_paths]
    
    for i in tqdm(range(folder_size)):
        image_paths = [osp.join(ds_paths[j], image_groups[j][i]) for j in range(len(ds_paths))]
        images = [cv.resize(cv.imread(image_path), (640, 640)) for image_path in image_paths]
        images = [cv.putText(image, folder_names[j], (260, 30), cv.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 5) for j, image in enumerate(images)]
        merged = np.concatenate(images, axis=1)
        

        if save_dir is not None:
            cv.imwrite(osp.join(save_dir, image_groups[0][i]), merged)


if __name__ == "__main__":
    dir = 'test'
    ds_paths = [f"/home/loki/DentalObjectDetection/data/YOLO/{dir}/images", f"/home/loki/DentalObjectDetection/data/YOLO/{dir}/visualized", f'/home/loki/DentalObjectDetection/runs/segment/predict6']
    save_dir = f"/home/loki/DentalObjectDetection/data/YOLO/{dir}/merged"
    join_images(ds_paths, save_dir=save_dir) 