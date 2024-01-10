import logging
import random
import math

import arcade

from space_collector.viewer.utils import map_coord_to_window_coord
from space_collector.viewer.constants import TEAM_COLORS


class SpaceShip:
    def __init__(self, image_path: str) -> None:
        self.team = random.randint(0, 3)
        self.x = random.randint(3_000, 17_000)
        self.y = random.randint(3_000, 17_000)
        self.vx = random.randint(-10, 10)
        self.vy = random.randint(-10, 10)
        self.width = 100
        self.height = 100
        self.image_path = image_path

    def setup(self) -> None:
        self.sprite = arcade.Sprite(self.image_path)
        self.sprite.width = 100
        self.sprite.height = 100
        self.sprite.color = TEAM_COLORS[self.team]
        self.sprite.width = self.width
        self.sprite.height = self.height

    def animate(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.sprite.angle = int(math.degrees(math.atan2(self.vy, self.vx)) - 90)
        self.sprite.position = map_coord_to_window_coord(self.x, self.y)

    def draw(self) -> None:
        self.animate()
        self.sprite.draw()


class Attacker(SpaceShip):
    def __init__(self) -> None:
        super().__init__("space_collector/viewer/images/spaceships/attacker.png")
        self.width = 30
        self.height = 30


class Collector(SpaceShip):
    def __init__(self) -> None:
        super().__init__("space_collector/viewer/images/spaceships/collector.png")
        self.width = 50
        self.height = 50


class Explorator(SpaceShip):
    def __init__(self) -> None:
        super().__init__("space_collector/viewer/images/spaceships/explorator.png")
        self.width = 40
        self.height = 40
