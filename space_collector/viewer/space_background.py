import random
from pathlib import Path

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


class SpaceBackground:
    def __init__(self):
        self.sprite_list = arcade.SpriteList()

    def setup(self) -> None:
        self.sprite_list = arcade.SpriteList()
        background_image = random.choice(
            find_image_files("space_collector/viewer/images/backgrounds")
        )
        background = arcade.Sprite(background_image)
        background.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        background.width = SCREEN_WIDTH
        background.height = SCREEN_HEIGHT
        self.sprite_list.append(background)

    def draw(self):
        self.sprite_list.draw()
