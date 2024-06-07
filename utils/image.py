from structures import CV2Image, Rectangle

import numpy as np


def image_in_rectangle(image: CV2Image, rectangle: Rectangle) -> CV2Image:
    return image[rectangle[0][1] : rectangle[1][1], rectangle[0][0] : rectangle[1][0]]


def image_relative_diff(image: CV2Image, ref_color, threshold) -> CV2Image:
    result = image.astype(np.int16)
    result_diff = np.abs(result - ref_color)
    result_sum = np.sum(np.where(result_diff > 0, result_diff, 0), axis=2)
    threshold_sum = (np.max(result_sum) - np.min(result_sum)) * threshold
    return np.where(result_sum > threshold_sum, 255, 0).astype(np.uint8)
