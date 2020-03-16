import csv
from os import walk, path, makedirs
import argparse
import time
from calculate_size import calculate_size

IMG_FORMATS = '.png'

parser = argparse.ArgumentParser()
parser.add_argument(
    '--input', help='Path to directory with images.', required=True)
parser.add_argument(
    '--output', help='Do to directory where output will be saved.', required=True)
args = parser.parse_args()


def save_reports_in_csv(report_path, reports):
    f = open(report_path, 'w')
    with f:
        writer = csv.writer(f)
        writer.writerows(reports)


def get_report_path():
    return path.join(args.output, 'report.csv')


def get_paths(dirpath, file):
    file_path = path.join(dirpath, file)
    img_output_path = path.join(args.output, file)
    histogram_path = path.join(args.output, 'histogram_' + file)
    return file_path, img_output_path, histogram_path


def go_through_files():
    makedirs(args.output, exist_ok=True)
    reports = []
    for (dirpath, dirnames, filenames) in walk(args.input):
        for file in filenames:
            if file.endswith(IMG_FORMATS):
                file_path, img_output_path, histogram_path = get_paths(
                    dirpath, file)
                print(file)
                time.sleep(2)  # time.sleep required because of segmentation faults
                calculate_size(file_path, img_output_path, histogram_path, reports)
    return reports


save_reports_in_csv(get_report_path(), go_through_files())
print('Report created!')
