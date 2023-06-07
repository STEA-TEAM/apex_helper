from typing import cast

import numpy as np

from .types import Polygon, Rectangle, Point


def scale_point(scale, point: Point) -> Point:
    return round(point[0] * scale), round(point[1] * scale)


def scale_rectangle(scale, rectangle: Rectangle) -> Rectangle:
    return cast(Rectangle, tuple(map(tuple, np.round(np.multiply(rectangle, scale)).astype(int))))


def scale_polygon(scale, polygon: Polygon) -> Polygon:
    return list(map(tuple, np.round(np.multiply(polygon, scale)).astype(int)))


def get_point_color(img, point: Point) -> int:
    pixel = img[point[1], point[0]]
    return (pixel[2] << 16) + (pixel[1] << 8) + pixel[0]


def image_in_rectangle(image, rectangle: Rectangle):
    return image[rectangle[0][1]:rectangle[1][1], rectangle[0][0]:rectangle[1][0]]


def image_in_polygon(image, polygon: Polygon):
    return image[polygon[0][1]:polygon[1][1], polygon[0][0]:polygon[1][0]]


def image_relative_diff(image, ref_color, threshold):
    # print(ammo_img)
    # print("Reference Color:", ref_color)
    result = image.astype("int16")
    result_diff = np.abs(result - ref_color)
    result_sum = np.sum(np.where(result_diff > 0, result_diff, 0), axis=2)
    threshold_sum = (np.max(result_sum) - np.min(result_sum)) * threshold
    return np.where(result_sum > threshold_sum, 255, 0).astype("uint8")
