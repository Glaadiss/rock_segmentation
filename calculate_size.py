import cv2
from typing import List
from preprocessing import crop_image
from watershed import watershed
from report import create_report


def calculate_size(file_path, img_output_path, histogram_path, reports) -> (List[str]):
    img_org = cv2.imread(file_path)
    img, gray = crop_image(img_org)
    img_with_contours, markers = watershed(img, gray)
    cv2.imwrite(img_output_path, img_with_contours)
    report = create_report(markers, gray, histogram_path)
    reports.append(report)
