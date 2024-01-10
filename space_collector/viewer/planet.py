import random

from space_collector.viewer.constants import TEAM_COLORS
from space_collector.viewer.utils import random_sprite, map_coord_to_window_coord


class Planet:
    def __init__(self, image_path: str) -> None:
        self.team = random.randint(0, 3)
        self.x = random.randint(3_000, 17_000)
        self.y = random.randint(3_000, 17_000)
        self.image_path = image_path

    def setup(self) -> None:
        # TODO use image_path
        self.sprite = random_sprite("space_collector/viewer/images/planets")
        self.sprite.width = 100
        self.sprite.height = 100
        self.sprite.color = TEAM_COLORS[self.team]

    def animate(self) -> None:
        self.sprite.position = map_coord_to_window_coord(self.x, self.y)

    def draw(self) -> None:
        self.animate()
        self.sprite.draw()
