import random
from pathlib import Path
import logging

import arcade

from space_collector.viewer.constants import SCREEN_HEIGHT, SCREEN_WIDTH


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

    def draw(self):
        self.frame_index += 1
        self.starfield1.alpha = alpha(self.frame_index, 1002, 30)
        self.starfield2.alpha = alpha(self.frame_index, 3107, 40)
        self.sprite_list.draw()
