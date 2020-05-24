import csv
from os import walk, path, makedirs
import argparse
import time
from calculate_size import calculate_size

IMG_FORMATS = '.png'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input', help='Path to directory with images.', required=True)
    parser.add_argument(
        '--output', help='Do to directory where output will be saved.', required=True)
    return parser.parse_args()


def save_reports_in_csv(report_path, reports):
    f = open(report_path, 'w')
    with f:
        writer = csv.writer(f)
        writer.writerows(reports)


def get_report_path(output):
    return path.join(output, 'report.csv')


def get_paths(dirpath, file, output):
    file_path = path.join(dirpath, file)
    img_output_path = path.join(output, file)
    histogram_path = path.join(output, 'histogram_' + file)
    return file_path, img_output_path, histogram_path


def go_through_files(input_dir, output_dir):
    makedirs(output_dir, exist_ok=True)
    reports = []

    for (dirpath, dirnames, filenames) in walk(input_dir):
        for file in filenames:
            if file.endswith(IMG_FORMATS):
                file_path, img_output_path, histogram_path = get_paths(
                    dirpath, file, output_dir)
                print(file)
                time.sleep(2)  # time.sleep required because of segmentation faults
                calculate_size(file_path, img_output_path, histogram_path, reports)
    return reports
