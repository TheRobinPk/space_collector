import random
from pathlib import Path
import logging

import arcade

from space_collector.viewer.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCORE_WIDTH


def find_image_files(directory: Path | str) -> list[Path]:
    if isinstance(directory, str):
        directory = Path(directory)
    return [
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix in (".jpg", ".png", ".jpeg")
    ]


def random_image(path: str) -> arcade.Sprite:
    sprite_image = random.choice(find_image_files(path))
    sprite = arcade.Sprite(sprite_image)
    sprite.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    sprite.width = SCREEN_WIDTH
    sprite.height = SCREEN_HEIGHT
    return sprite


def alpha(frame: int, period: int, max_value: int) -> int:
    frame %= period
    value = abs(frame / period - 0.5) * 2
    return int(max_value * value)


def linear(alpha: float, min_value: int, max_value: int) -> int:
    return min_value + int((max_value - min_value) * alpha)


class Comet:
    def __init__(self) -> None:
        self.sprite = arcade.Sprite("space_collector/viewer/images/comet.png")
        self.new_trajectory(0)

    def new_trajectory(self, start_frame: int) -> None:
        logging.info(start_frame)
        self.start_x = random.randint(SCORE_WIDTH, SCREEN_WIDTH)
        self.start_y = random.randint(SCORE_WIDTH, SCREEN_HEIGHT)
        self.end_x = random.randint(0, SCREEN_WIDTH)
        self.end_y = random.randint(0, SCREEN_HEIGHT)
        self.period = random.randint(30, 100)
        self.start_frame = start_frame

    def animate(self, frame: int) -> None:
        logging.info(frame)
        value = (frame - self.start_frame) / self.period
        if value >= 1:
            self.sprite.alpha = 0
            if value >= 2:
                self.new_trajectory(frame)
            return
        self.sprite.position = (
            linear(value, self.start_x, self.end_x),
            linear(value, self.start_y, self.end_y),
        )
        self.sprite.alpha = int((1 - abs(value - 0.5) * 2) * 255)


class SpaceBackground:
    def __init__(self):
        self.sprite_list = arcade.SpriteList()
        self.frame_index = 0

    def setup(self) -> None:
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(
            random_image("space_collector/viewer/images/backgrounds")
        )
        self.starfield1 = random_image("space_collector/viewer/images/starfields")
        self.sprite_list.append(self.starfield1)
        self.starfield2 = random_image("space_collector/viewer/images/starfields")
        self.sprite_list.append(self.starfield2)
        self.comet1 = Comet()
        self.sprite_list.append(self.comet1.sprite)
        self.comet2 = Comet()
        self.sprite_list.append(self.comet2.sprite)

    def draw(self) -> None:
        self.frame_index += 1
        self.comet1.animate(self.frame_index)
        self.comet2.animate(self.frame_index)
        self.starfield1.alpha = alpha(self.frame_index, 202, 30)
        self.starfield2.alpha = alpha(self.frame_index, 507, 40)
        self.sprite_list.draw()
