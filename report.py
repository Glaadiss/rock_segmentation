from typing import List
import matplotlib.pyplot as plt
import numpy as np
from skimage import measure

PIXELS_TO_MM = 0.2

validators = [
    lambda x: x <= 6.3,
    lambda x: 6.3 < x <= 10,
    lambda x: 10 < x <= 16,
    lambda x: 16 < x <= 25,
    lambda x: 25 < x <= 40,
    lambda x: x > 40,
]

groups_count = len(validators)


def calculate_area(region):
    return np.sqrt(region["Area"] * PIXELS_TO_MM)


def filter_background(areas):
    return filter(lambda a: a < 100, areas)


def group_by_area(areas):
    result = [[] for _ in range(groups_count)]
    for area in areas:
        for i in range(groups_count):
            if validators[i](area):
                result[i].append(area)
    return result


def create_histogram(areas, histogram_path):
    plt.hist(areas, bins=25, rwidth=0.8)
    plt.ylabel('Number of fragments')
    plt.xlabel('Size')
    plt.savefig(histogram_path)
    plt.close()


def get_areas(regions):
    return list(filter_background(map(calculate_area, regions)))


def get_distribution(groups, item_count):
    distribution = [len(elements) / item_count for elements in groups]
    return ["{0:.2%}".format(el) for el in distribution]


def create_report(markers, img, histogram_path) -> List[str]:
    regions = measure.regionprops(markers, intensity_image=img)
    areas = get_areas(regions)
    create_histogram(areas, histogram_path)
    groups = group_by_area(areas)
    return get_distribution(groups, len(regions))
