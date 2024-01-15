import logging

import arcade

from space_collector.viewer.animation import AnimatedValue, Animation, Step
from space_collector.viewer.utils import map_coord_to_window_coord, hue_changed_texture
from space_collector.viewer.constants import TEAM_HUES


class SpaceShip:
    image_path = ""

    def __init__(self, x: int, y: int, angle: int, team: int) -> None:
        self.team = team
        self.x = AnimatedValue(x)
        self.y = AnimatedValue(y)
        self.angle = angle  # TODO animation compliquée avec modulo ?
        self.width = 100
        self.height = 100

    def setup(self) -> None:
        self.sprite = arcade.Sprite(
            texture=hue_changed_texture(self.image_path, TEAM_HUES[self.team])
        )
        self.sprite.width = self.width
        self.sprite.height = self.height

    def animate(self) -> None:
        self.sprite.angle = int(self.angle - 90)
        self.sprite.position = map_coord_to_window_coord(self.x.value, self.y.value)

    def draw(self) -> None:
        self.animate()
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
        self.angle = server_data["angle"]


class Attacker(SpaceShip):
    image_path = "space_collector/viewer/images/spaceships/attacker.png"

    def __init__(self, x: int, y: int, angle: int, team: int) -> None:
        super().__init__(x, y, angle, team)
        self.width = 30
        self.height = 30


class Collector(SpaceShip):
    image_path = "space_collector/viewer/images/spaceships/collector.png"

    def __init__(self, x: int, y: int, angle: int, team: int) -> None:
        super().__init__(x, y, angle, team)
        self.width = 50
        self.height = 50


class Explorator(SpaceShip):
    image_path = "space_collector/viewer/images/spaceships/explorator.png"

    def __init__(self, x: int, y: int, angle: int, team: int) -> None:
        super().__init__(x, y, angle, team)
        self.width = 40
        self.height = 40
