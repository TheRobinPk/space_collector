import logging
import random
import colorsys

import arcade

from space_collector.viewer.animation import AnimatedValue, Animation
from space_collector.viewer.constants import TEAM_HUES
from space_collector.viewer.utils import (
    hue_changed_texture,
    map_coord_to_window_coord,
    find_image_files,
)


class Planet:
    def __init__(self, x: int, y: int, id: int, team: int) -> None:
        self.team = team
        self.x = AnimatedValue(x)
        self.y = AnimatedValue(y)
        self.size = AnimatedValue(200)
        images = find_image_files("space_collector/viewer/images/planets")
        self.image_path = images[id % len(images)]
        logging.info("planet %d, %d", x, y)

    def setup(self) -> None:
        self.sprite = arcade.Sprite(
            texture=hue_changed_texture(self.image_path, TEAM_HUES[self.team])
        )
        self.sprite.width = random.randint(30, 70)
        self.sprite.height = self.sprite.width

    def animate(self) -> None:
        self.sprite.position = map_coord_to_window_coord(self.x.value, self.y.value)
        self.sprite.width = self.size.value
        self.sprite.height = self.size.value

    def draw(self) -> None:
        self.animate()
        color_rgb = colorsys.hsv_to_rgb(TEAM_HUES[self.team] / 360, 1, 1)
        arcade.draw_circle_outline(
            self.sprite.position[0],
            self.sprite.position[1],
            self.size.value // 2 + 2,
            (
                int(color_rgb[0] * 255),
                int(color_rgb[1] * 255),
                int(color_rgb[2] * 255),
                150,
            ),
            4,
        )
        self.sprite.draw()

    def update(self, server_data: dict, duration: float) -> None:
        self.x.add_animation(
            Animation(
                start_value=self.x.value,
                end_value=server_data["x"],
                duration=duration,
            )
        )
        self.y.add_animation(
            Animation(
                start_value=self.y.value,
                end_value=server_data["y"],
                duration=duration,
            )
        )
        self.size.add_animation(
            Animation(
                start_value=self.size.value,
                end_value=server_data["size"],
                duration=duration,
            )
        )
