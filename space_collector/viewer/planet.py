import random

from space_collector.viewer.animation import AnimatedValue, Animation
from space_collector.viewer.constants import TEAM_COLORS
from space_collector.viewer.utils import random_sprite, map_coord_to_window_coord


class Planet:
    def __init__(self, image_path: str) -> None:
        self.team = random.randint(0, 3)
        self.image_path = image_path
        self.x = AnimatedValue(random.randint(3_000, 17_000))
        self.y = AnimatedValue(random.randint(3_000, 17_000))

    def setup(self) -> None:
        # TODO use image_path
        self.sprite = random_sprite("space_collector/viewer/images/planets")
        self.sprite.width = 100
        self.sprite.height = 100
        self.sprite.color = TEAM_COLORS[self.team]
        duration = random.random() * 5
        self.x.add_animation(
            Animation(
                start_value=self.x.value,
                end_value=random.randint(3_000, 17_000),
                duration=duration,
            )
        )
        self.y.add_animation(
            Animation(
                start_value=self.y.value,
                end_value=random.randint(3_000, 17_000),
                duration=duration,
            )
        )

    def animate(self) -> None:
        self.sprite.position = map_coord_to_window_coord(self.x.value, self.y.value)

    def draw(self) -> None:
        self.animate()
        self.sprite.draw()
