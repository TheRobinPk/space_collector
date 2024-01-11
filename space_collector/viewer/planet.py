import logging
import random

from space_collector.viewer.animation import AnimatedValue, Animation
from space_collector.viewer.constants import TEAM_COLORS
from space_collector.viewer.utils import random_sprite, map_coord_to_window_coord


class Planet:
    def __init__(self, x: int, y: int, team: int) -> None:
        self.team = team
        self.x = AnimatedValue(x)
        self.y = AnimatedValue(y)
        logging.info("planet %d, %d", x, y)

    def setup(self) -> None:
        self.sprite = random_sprite("space_collector/viewer/images/planets")
        self.sprite.width = random.randint(30, 70)
        self.sprite.height = self.sprite.width

    def animate(self) -> None:
        self.sprite.position = map_coord_to_window_coord(self.x.value, self.y.value)

    def draw(self) -> None:
        self.animate()
        self.sprite.draw()

    def update(self, server_data: dict, date: float) -> None:
        pass  # TODO
