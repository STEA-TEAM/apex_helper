from weapon_detector.types import RectArea


def get_image_part(img, pos: RectArea):
    return img[pos["y1"]:pos["y2"], pos["x1"]:pos["x2"]]


def get_scaled_point(scale, point: (int, int)) -> (int, int):
    return round(point[0] * scale), round(point[1] * scale)


def get_scaled_rect_area(scale, rect_area: RectArea) -> RectArea:
    return {
        "x1": round(rect_area["x1"] * scale),
        "y1": round(rect_area["y1"] * scale),
        "x2": round(rect_area["x2"] * scale),
        "y2": round(rect_area["y2"] * scale),
    }


def get_point_color(img, point: (int, int)) -> int:
    pixel = img[point[1], point[0]]
    return (pixel[2] << 16) + (pixel[1] << 8) + pixel[0]
