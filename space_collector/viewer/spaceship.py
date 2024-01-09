import logging
import random
import math

import arcade

from space_collector.viewer.utils import map_coord_to_window_coord


team_colors = {
    0: (255, 128, 128, 255),
    1: (64, 255, 64, 255),
    2: (255, 255, 0, 255),
    3: (32, 196, 255, 255),
}


class SpaceShip:
    def __init__(self, image_path: str) -> None:
        self.team = random.randint(0, 3)
        self.x = random.randint(3_000, 17_000)
        self.y = random.randint(3_000, 17_000)
        self.vx = random.randint(-10, 10)
        self.vy = random.randint(-10, 10)
        self.sprite = arcade.Sprite(image_path)
        self.sprite.width = 100
        self.sprite.height = 100
        self.sprite.color = team_colors[self.team]

    def animate(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.sprite.angle = int(math.degrees(math.atan2(self.vy, self.vx)) - 90)
        self.sprite.position = map_coord_to_window_coord(self.x, self.y)


class Attacker(SpaceShip):
    def __init__(self) -> None:
        super().__init__("space_collector/viewer/images/spaceships/attacker.png")
        self.sprite.width = 30
        self.sprite.height = 30


class Collector(SpaceShip):
    def __init__(self) -> None:
        super().__init__("space_collector/viewer/images/spaceships/collector.png")
        self.sprite.width = 50
        self.sprite.height = 50


class Explorator(SpaceShip):
    def __init__(self) -> None:
        super().__init__("space_collector/viewer/images/spaceships/explorator.png")
        self.sprite.width = 40
        self.sprite.height = 40
