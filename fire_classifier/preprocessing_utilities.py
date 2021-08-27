import cv2
import numpy as np


def read_img_from_path(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    return img


def read_from_file(file_object):
    arr = np.fromstring(file_object.read(), np.uint8)
    img_np = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    return img_np
