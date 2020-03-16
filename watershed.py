import numpy as np
import cv2
from preprocessing import get_fg_and_bg


def watershed(img, gray) -> (np.ndarray, np.ndarray):
    img_copy, gray_copy = img.copy(), gray.copy()
    sure_fg, sure_bg = get_fg_and_bg(gray_copy, scale=0.1)
    unknown = cv2.subtract(sure_bg, sure_fg)
    n_labels, markers, stats, centroids = cv2.connectedComponentsWithStats(
        sure_fg)

    markers[unknown == 255] = 0
    colors = np.random.randint(0, 255, size=(n_labels, 3), dtype=np.uint8)
    colors[0] = [0, 0, 0]
    for i, centroid in enumerate(centroids[1:], start=1):
        area = stats[i, 4]
        if area < 25:
            markers[markers == i] = 0

    markers = cv2.watershed(img_copy, markers)
    img_copy[markers == -1] = [0, 0, 255]

    return img_copy, markers
