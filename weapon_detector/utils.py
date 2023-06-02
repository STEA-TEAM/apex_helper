from weapon_detector.types import RectArea


def get_image_part(img, pos: RectArea):
    return img[pos["y1"]:pos["y2"], pos["x1"]:pos["x2"]]


def get_point_color(img, point: (int, int)) -> int:
    pixel = img[point[1], point[0]]
    return (pixel[2] << 16) + (pixel[1] << 8) + pixel[0]
