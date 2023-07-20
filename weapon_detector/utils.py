from numpy import ndarray as opencv_image, abs, int16, max, min, sum, uint8, where
from .types import Point, Rectangle


def get_point_color(image: opencv_image, point: Point) -> int:
    pixel = image[point[1], point[0]]
    return (pixel[2] << 16) + (pixel[1] << 8) + pixel[0]


def image_in_rectangle(image: opencv_image, rectangle: Rectangle) -> opencv_image:
    return image[rectangle[0][1]:rectangle[1][1], rectangle[0][0]:rectangle[1][0]]


def image_relative_diff(image: opencv_image, ref_color, threshold) -> opencv_image:
    result = image.astype(int16)
    result_diff = abs(result - ref_color)
    result_sum = sum(where(result_diff > 0, result_diff, 0), axis=2)
    threshold_sum = (max(result_sum) - min(result_sum)) * threshold
    return where(result_sum > threshold_sum, 255, 0).astype(uint8)
