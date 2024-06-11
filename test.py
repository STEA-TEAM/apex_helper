import math

from structures import DrawElement, Point, DrawType, LayerDrawServerMessage, ResultType
from typing import List

offset: Point = (math.floor((3840 - 2160) / 2), 0)

draw_elements: List[DrawElement] = []
draw_elements.append({
    "dimensions": {
        "height": 2160,
        "width": 2160,
        "x": offset[0],
        "y": offset[1],
    },
    "fill": None,
    "opacity": 0.8,
    "stroke": {
        "color": "#9e9e9e",
        "opacity": 1.0,
        "width": 3,
    },
    "type": DrawType.Rectangle,
})
dimension = (100, 200, 300, 400)
draw_elements.append(
    {
        "dimensions": {
            "height": dimension[3] - dimension[1],
            "width": dimension[2] - dimension[0],
            "x": offset[0] + dimension[0],
            "y": offset[1] + dimension[1],
        },
        "fill": None,
        "opacity": 0.8,
        "stroke": {
            "color": "#f44336",
            "opacity": 1.0,
            "width": 3,
        },
        "type": DrawType.Rectangle,
    }
)
draw_elements.append(
    {
        "content": "enemy",
        "dimensions": {
            "x": offset[0] + dimension[0],
            "y": offset[1] + dimension[1] - 20,
        },
        "font": None,
        "fill": {
            "color": "#f44336",
            "opacity": 1.0,
        },
        "opacity": 0.8,
        "stroke": None,
        "type": DrawType.Text,
    }
)

print(LayerDrawServerMessage(
    {
        "elements": draw_elements,
        "message": None,
        "name": "Test",
        "result": ResultType.success,
    }
))
