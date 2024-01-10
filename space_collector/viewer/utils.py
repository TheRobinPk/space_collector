import random
from pathlib import Path

import arcade

from space_collector.viewer.constants import (
    MAP_DIMENSION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCORE_WIDTH,
)


def map_coord_to_window_coord(x, y) -> tuple[int, int]:
    return (
        int(x / MAP_DIMENSION * (SCREEN_WIDTH - SCORE_WIDTH)) + SCORE_WIDTH,
        int(y / MAP_DIMENSION * SCREEN_HEIGHT),
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
