from typing import cast

import numpy as np

from .types import Polygon, Rectangle, Point


def get_point_color(img, point: Point) -> int:
    pixel = img[point[1], point[0]]
    return (pixel[2] << 16) + (pixel[1] << 8) + pixel[0]


def image_in_rectangle(image, rectangle: Rectangle):
    return image[rectangle[0][1]:rectangle[1][1], rectangle[0][0]:rectangle[1][0]]


def image_relative_diff(image, ref_color, threshold):
    result = image.astype("int16")
    result_diff = np.abs(result - ref_color)
    result_sum = np.sum(np.where(result_diff > 0, result_diff, 0), axis=2)
    threshold_sum = (np.max(result_sum) - np.min(result_sum)) * threshold
    return np.where(result_sum > threshold_sum, 255, 0).astype("uint8")
