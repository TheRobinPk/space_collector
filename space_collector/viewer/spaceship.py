import logging

import arcade

from space_collector.game.constants import MAP_DIMENSION
from space_collector.viewer.animation import AnimatedValue, Animation, Step
from space_collector.viewer.utils import (
    MAP_WIDTH,
    map_coord_to_window_coord,
    hue_changed_texture,
)
from space_collector.viewer.constants import TEAM_HUES

HIGH_ENERGY_LENGTH = int(2000 / MAP_DIMENSION * MAP_WIDTH)


class SpaceShip:
    image_path = ""

    def __init__(self, x: int, y: int, angle: int, team: int) -> None:
        self.team = team
        self.x = AnimatedValue(x)
        self.y = AnimatedValue(y)
        self.angle = angle  # TODO animation compliquée avec modulo ?
        self.width = 100
        self.height = 100
        self.fire = False
        self.fire_angle = 0

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
        self.fire = server_data["fire"]
        self.fire_angle = server_data["fire_angle"]


class Attacker(SpaceShip):
    image_path = "space_collector/viewer/images/spaceships/attacker.png"

    def __init__(self, x: int, y: int, angle: int, team: int) -> None:
        super().__init__(x, y, angle, team)
        self.width = 30
        self.height = 30

    def setup(self) -> None:
        super().setup()
        self.lightning_length = AnimatedValue(0)
        self.lightning_alpha = AnimatedValue(0)
        self.lightning_sprite = arcade.Sprite(
            texture=hue_changed_texture(
                "space_collector/viewer/images/high_energy.png", TEAM_HUES[self.team]
            )
        )
        self.lightning_sprite.width = 40
        self.lightning_sprite.height = 1

    def update(self, server_data: dict, duration: float) -> None:
        if server_data["fire"]:
            self.lightning_alpha.add_animations(
                initial_value=self.lightning_alpha.value,
                steps=[
                    Step(value=255, duration=0.05),
                    Step(value=255, duration=0.4),
                    Step(value=0, duration=0.05),
                ],
            )
            self.lightning_length.add_animations(
                initial_value=self.lightning_length.value,
                steps=[
                    Step(value=HIGH_ENERGY_LENGTH, duration=0.25),
                    Step(value=0, duration=0.25),
                ],
            )
            self.fire_angle = server_data["fire_angle"]

    def animate(self) -> None:
        super().animate()
        self.lightning_sprite.angle = int(self.fire_angle - 90)
        self.lightning_sprite.position = map_coord_to_window_coord(
            self.x.value, self.y.value
        )
        self.lightning_sprite.height = self.lightning_length.value + 1

    def draw(self) -> None:
        super().draw()
        self.lightning_sprite.draw()


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
