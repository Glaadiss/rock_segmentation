import numpy as np
import cv2
from skimage import filters
from skimage.segmentation import clear_border
from skimage import img_as_ubyte

kernel2 = np.ones((2, 2), np.uint8)
kernel3 = np.ones((3, 3), np.uint8)
kernel5 = np.ones((5, 5), np.uint8)

kernel42 = np.ones((56, 56), np.uint8)
kernel15 = np.ones((21, 21), np.uint8)


def erode_background(gray):
    thresh = threshold(gray)
    edges = cv2.Canny(thresh, 110, 330)
    edges = cv2.dilate(edges, kernel15)
    return cv2.erode(edges, kernel42, iterations=2)


def crop_image(img_color):
    copy = img_color.copy()
    gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    eroded_area = erode_background(gray)
    mask = eroded_area > 0
    coords = np.argwhere(mask)
    x0, y0 = coords.min(axis=0)
    x0 = x0 - 50 if x0 > 150 else x0
    x1, y1 = coords.max(axis=0) + 1  # slices are exclusive at the top
    return copy[x0:x1, y0:y1], gray[x0:x1, y0:y1]


def prepare_image(img):
    opening_kernel = np.ones((11, 11), np.uint8)
    res = cv2.Canny(img, 100, 200)
    res = cv2.GaussianBlur(res, (15, 15), cv2.BORDER_DEFAULT)
    ret, res = cv2.threshold(
        res, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    res = cv2.dilate(res, opening_kernel, iterations=3)
    res = cv2.erode(res, opening_kernel, iterations=5)

    return cv2.subtract(img, res)


def smooth(img):
    magnitude_factor = 0.5
    edge_roberts = img_as_ubyte(magnitude_factor * filters.roberts(img))
    pipe = cv2.subtract(img, edge_roberts)
    u = img.mean() * 0.2
    std = img.std() * 0.5
    local_std = 0.2 * cv2.GaussianBlur(img, (13, 13), cv2.BORDER_DEFAULT)
    local_mean = 0.5 * cv2.blur(img, (13, 13))
    T = img_as_ubyte(cv2.subtract(cv2.subtract(u, local_std), local_mean) / 256)
    return cv2.subtract(pipe, T)


def threshold(img):
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def get_fg_and_bg(img, scale=0.02):
    thresh = threshold(img)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel5)
    sure_bg = cv2.dilate(opening, kernel3, iterations=3)
    dist_transform = cv2.distanceTransform(clear_border(opening), cv2.DIST_L2, 3)
    ret, sure_fg = cv2.threshold(
        dist_transform, scale * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    return sure_fg, sure_bg


def get_markers(img, scale=0.02):
    sure_fg, sure_bg = get_fg_and_bg(img, scale=scale)
    n_labels, markers, stats, centroids = cv2.connectedComponentsWithStats(
        sure_fg)

    return n_labels, markers, stats, centroids
