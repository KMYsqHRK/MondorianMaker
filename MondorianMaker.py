import random
from PIL import Image, ImageDraw
import os
import numpy as np


# 長方形を特徴づけるクラス
class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        # self.area = abs(self.x1 - self.x2) * abs(self.y1 - self.y2)


# 一定以上大きな長方形を分割して新たな配列を作る関数。
def split_rectangle(rect, canvas_size):
    width = rect.x2 - rect.x1  # rectangle classのもつ幅
    height = rect.y2 - rect.y1  # rectangle classのもつ高さ
    side_min = 60  # 小さすぎる長方形が生まれないための調整パラメータ
    if width < side_min or height < side_min:
        return [rect]

    else:
        if width > height:  # Vertical split
            split_point = random.randint(
                rect.x1 + side_min / 2, rect.x2 - side_min / 2
            )  # 範囲を設定
            return [
                Rectangle(rect.x1, rect.y1, split_point, rect.y2),
                Rectangle(split_point, rect.y1, rect.x2, rect.y2),
            ]
        else:  # Horizontal split
            split_point = random.randint(rect.y1 + side_min / 2, rect.y2 - side_min / 2)
            return [
                Rectangle(rect.x1, rect.y1, rect.x2, split_point),
                Rectangle(rect.x1, split_point, rect.x2, rect.y2),
            ]


def mondrian(width, height, iterations):
    rectangles = [Rectangle(0, 0, width, height)]

    for _ in range(iterations):
        rect = random.choice(rectangles)
        rectangles.remove(rect)
        new_rects = split_rectangle(rect, (width, height))
        rectangles.extend(new_rects)

    return rectangles


def draw_mondrian(rectangles, width, height):
    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)

    colors = ["red", "blue", "yellow"]

    for rect in rectangles:
        color = random.choice(colors) if random.random() < 0.3 else "white"
        draw.rectangle(
            [rect.x1, rect.y1, rect.x2, rect.y2], fill=color, outline="black", width=5
        )

    return image


# メイン処理
width, height = 1000, 1000
iterations = 60
new_folder_name = f"ite={iterations}"
os.mkdir(new_folder_name)

for i in range(30):
    rectangles = mondrian(width, height, iterations)
    image = draw_mondrian(rectangles, width, height)
    image.save(f"ite={iterations}/mondrian{i}.png")
