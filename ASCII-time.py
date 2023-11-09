import os
import time
import functools
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen

# cols = os.get_terminal_size()[0]
rows = 10  # os.get_terminal_size()[1] - 5
cols = 10
font = TTFont("./times.ttf")
glyph_set = font.getGlyphSet()
digits = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
    ":": "colon",
    ";": "semicolon",
}


def glyph_name(ch):
    if ch in digits.keys():
        return digits[ch]
    return ch


def scale_values(array, new_min, new_max):
    array = np.asarray(array)
    minmax = np.array([np.min(array), np.max(array)])
    if minmax[0] == minmax[1]:
        return np.full_like(array, (new_min + new_max) / 2)
    # Use numpy operations for scaling
    scaled_array = ((array - minmax[0]) / np.ptp(minmax)) * (
        new_max - new_min
    ) + new_min
    return scaled_array


def points_to_xs_ys(points):
    xs = []
    ys = []
    for i in points:
        xs.append(i[0])
        ys.append(i[1])
    return xs, ys


def interp(p1, p2, t) -> tuple[int, int]:
    xd = p2[0] - p1[0]
    yd = p2[1] - p1[1]
    return (p1[0] + xd * t, p1[1] + yd * t)


def _bezier(points, t):
    if len(points) == 1:
        return points[0]
    new_points = []
    for i in range(len(points) - 1):
        new_points.append(interp(points[i], points[i + 1], t))
    return _bezier(new_points, t)


def bezier(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [_bezier(points, i) for i in np.linspace(0, 1, 1000)]


def lineto(fr, to):
    return [interp(fr, to, i) for i in np.linspace(0, 1, 100)]


def safe_index(min, max, v):
    if v < min:
        return 0
    if v > max:
        return max
    return v


def get_point_grid(points: list[tuple[int, int]]):
    grid = [[" " for _ in range(cols)] for _ in range(rows)]
    xs, ys = points_to_xs_ys(points)
    xs = scale_values(xs, 1, cols - 1)
    ys = scale_values(ys, 1, rows - 1)
    for x, y in zip(xs, ys):
        x = round(x)
        y = round(y)
        grid[safe_index(0, rows - 1, rows - y)][safe_index(0, cols - 1, x)] = "*"
    return grid


def draw_grid(grid):
    print("\n".join(["".join(i) for i in grid]))


def draw(points: list[tuple[int, int]]):
    grid = get_point_grid(points)
    draw_grid(grid)


pos = (0, 0)
shape_start = (0, 0)


def execute_instruction(inst) -> list[tuple[int, int]]:
    global pos, shape_start
    if inst[0] == "moveTo":
        pos = inst[1][0]
        shape_start = pos
        return []
    if inst[0] == "lineTo":
        ret = lineto(pos, inst[1][0])
        pos = inst[1][0]
        return ret
    if inst[0] == "qCurveTo":
        ret = bezier([pos, *inst[1]])
        pos = inst[1][-1]
        return ret
    if inst[0] == "closePath":
        return lineto(pos, shape_start)
    print(f"UNKNOWN COMMAND: {inst}")
    raise Exception("")


def execute_glyph_insructions(glyph_name):
    glyph = glyph_set[glyph_name]
    pen = RecordingPen()
    glyph.draw(pen)
    points = []
    for instruction in pen.value:
        points = points + execute_instruction(instruction)
    return points


@functools.lru_cache(maxsize=128)
def glyph(ch):
    ch = glyph_name(ch)
    return get_point_grid(execute_glyph_insructions(ch))


while True:
    points = np.concatenate(
        [glyph(i) for i in datetime.now().strftime("%H:%M:%S")], axis=1
    )
    time.sleep(0.5)
    draw_grid(points.tolist())
    print(f"\033[{points.shape[0]}A", end="")
