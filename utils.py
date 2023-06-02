def get_point_color(img, point: (int, int)) -> int:
    pixel = img[point[1], point[0]]
    return (pixel[2] << 16) + (pixel[1] << 8) + pixel[0]
