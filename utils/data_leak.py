import time
import os
import os.path as osp
import cv2 as cv
import numpy as np
from tqdm import tqdm

RESIZE_DIM = (320, 320)
def get_image_path_list(dir: str) -> list:
    return [osp.join(dir, f) for f in os.listdir(dir)]

def read_img(path: str) -> np.ndarray:  
    img = cv.imread(path)
    return img

def preprocess_img(img: np.ndarray) -> np.ndarray:
    img = cv.resize(img, RESIZE_DIM)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = img / 255
    return img

def calculate_loss(img1: np.ndarray, img2: np.ndarray, print_loss: bool = False) -> float:
    loss = np.linalg.norm(img1 - img2)

    if print_loss:
        print(f"Loss: {loss}")
    return loss

def display_img(img: np.ndarray, millis: float = 0) -> None:
    cv.imshow("image", img)
    cv.waitKey(millis)

def benchmark_func(func : callable, *args, **kwargs) -> float:
    start = time.time()
    N_iters = 1000
    for i in range(N_iters):
        func(*args, **kwargs)
    end = time.time()
    return (end - start)/N_iters

if __name__ == "__main__":
    train_imgs_dir = '/home/loki/DentalObjectDetection/data/v6/train/images'
    valid_imgs_dir = '/home/loki/DentalObjectDetection/data/v6/valid/images'

    path1 = '/home/loki/DentalObjectDetection/data/v6/train/images/120dfa9b-JAFARNADERY_JAVID_2020-06-07092041_jpg.rf.4d29482009cf6bd0ea86555b3e90fd73.jpg'
    path2 = '/home/loki/DentalObjectDetection/data/v6/valid/images/120dfa9b-JAFARNADERY_JAVID_2020-06-07092041_jpg.rf.39bbf3023b9e25115c3189d23e82878e.jpg'

    path3 = '/home/loki/DentalObjectDetection/data/v6/train/images/98e2e8e2-Hushmand_Ali_2022-06-12142327_jpg.rf.c7e8a370680408a4e46fffe784393e4b.jpg'

    print("Reading takes: ", benchmark_func(read_img, path = path1), "seconds.")

    img1 = cv.imread(path1)
    img2 = cv.imread(path2)
    img3 = cv.imread(path3)

    print("Preprocessing takes: ", benchmark_func(preprocess_img, img = img1), "seconds.")

    img1 = preprocess_img(img1)
    img2 = preprocess_img(img2)
    img3 = preprocess_img(img3)

    print("Loss calculation takes: ", benchmark_func(calculate_loss, img1 = img1, img2 = img2), "seconds.")

    # start_time = time.time()
    # calculate_loss(img1, img2, print_loss=True)
    # calculate_loss(img1, img3, print_loss=True)
    # calculate_loss(img2, img3, print_loss=True)
    # print("Time taken: ", time.time() - start_time)
    # breakpoint()

    train_img_path_list = get_image_path_list(train_imgs_dir)
    valid_img_path_list = get_image_path_list(valid_imgs_dir)

    train_imgs = [preprocess_img(read_img(path)) for path in train_img_path_list]
    valid_imgs = [preprocess_img(read_img(path)) for path in valid_img_path_list]

    same_img_paths = []
    losses = []
    for train_idx, train_img in tqdm(enumerate(train_imgs), total=len(train_imgs)):
        # train_img = read_img(train_img_path)
        # preprocessed_train_img = preprocess_img(train_img)

        for valid_idx, valid_img in tqdm(enumerate(valid_imgs), total=len(valid_imgs)):
            # valid_img = read_img(valid_img_path)
            # preprocessed_valid_img = preprocess_img(valid_img)

            loss = calculate_loss(train_img, valid_img)
            if loss < 0.1:
                same_img_paths.append((train_img_path_list[train_idx], valid_img_path_list[valid_idx]))
            losses.append(loss)
            # print(f'Loss between {train_img_path} and {valid_img_path} : {loss}')
        train_imgs[train_idx] = None
    print(losses)
    breakpoint()
    # cv.imshow("image", img1- img2)
    # cv.waitKey(0)