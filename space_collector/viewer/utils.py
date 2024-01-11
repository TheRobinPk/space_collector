import random
from pathlib import Path

import arcade

from space_collector.viewer.constants import (
    MAP_DIMENSION,
    MAP_MIN_X,
    MAP_MAX_X,
    MAP_MIN_Y,
    MAP_MAX_Y,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCORE_WIDTH,
)

MAP_WIDTH = MAP_MAX_X - MAP_MIN_X
MAP_HEIGHT = MAP_MAX_Y - MAP_MIN_Y


def map_coord_to_window_coord(x: float, y: float) -> tuple[int, int]:
    return (
        int(x / MAP_DIMENSION * MAP_WIDTH) + MAP_MIN_X,
        int(y / MAP_DIMENSION * MAP_HEIGHT) + MAP_MIN_Y,
    )


def find_image_files(directory: Path | str) -> list[Path]:
    if isinstance(directory, str):
        directory = Path(directory)
    return [
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix in (".jpg", ".png", ".jpeg")
    ]


def random_sprite(path: str) -> arcade.Sprite:
    sprite_image = random.choice(find_image_files(path))
    sprite = arcade.Sprite(sprite_image)
    sprite.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    sprite.width = SCREEN_WIDTH
    sprite.height = SCREEN_HEIGHT
    return sprite
