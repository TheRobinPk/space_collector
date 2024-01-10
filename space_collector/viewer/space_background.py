import logging
import random
from time import perf_counter

import arcade

from space_collector.viewer.animation import AnimatedValue, Animation, Step
from space_collector.viewer.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCORE_WIDTH
from space_collector.viewer.utils import random_sprite


def alpha(frame: int, period: int, max_value: int) -> int:
    frame %= period
    value = abs(frame / period - 0.5) * 2
    return int(max_value * value)


class Comet:
    FADE_IN_DURATION = 0.3

    def __init__(self) -> None:
        self.sprite = arcade.Sprite("space_collector/viewer/images/comet.png")
        self.x = AnimatedValue(random.randint(SCORE_WIDTH, SCREEN_WIDTH))
        self.y = AnimatedValue(random.randint(0, SCREEN_HEIGHT))
        self.alpha = AnimatedValue(0)
        self.new_trajectory()

    def new_trajectory(self) -> None:
        self.duration = random.random() * 2 + 2 * self.FADE_IN_DURATION
        self.start_time = perf_counter()

        self.x.add_animation(
            Animation(
                start_value=self.x.value,
                end_value=random.randint(SCORE_WIDTH, SCREEN_WIDTH),
                duration=self.duration,
            )
        )
        self.y.add_animation(
            Animation(
                start_value=self.y.value,
                end_value=random.randint(0, SCREEN_HEIGHT),
                duration=self.duration,
            )
        )
        self.alpha.add_animations(
            initial_value=self.alpha.value,
            steps=[
                Step(value=255, duration=self.FADE_IN_DURATION),
                Step(value=255, duration=self.duration - 2 * self.FADE_IN_DURATION),
                Step(value=0, duration=self.FADE_IN_DURATION),
            ],
        )

    def animate(self, frame: int) -> None:
        if perf_counter() - self.start_time > 2 * self.duration:
            self.new_trajectory()
        self.sprite.position = (self.x.value, self.y.value)
        self.sprite.alpha = self.alpha.value


class SpaceBackground:
    def __init__(self):
        self.sprite_list = arcade.SpriteList()
        self.frame_index = 0

    def setup(self) -> None:
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(
            random_sprite("space_collector/viewer/images/backgrounds")
        )
        self.starfield1 = random_sprite("space_collector/viewer/images/starfields")
        self.sprite_list.append(self.starfield1)
        self.starfield2 = random_sprite("space_collector/viewer/images/starfields")
        self.sprite_list.append(self.starfield2)
        self.comet1 = Comet()
        self.sprite_list.append(self.comet1.sprite)
        self.comet2 = Comet()
        self.sprite_list.append(self.comet2.sprite)

    def draw(self) -> None:
        self.frame_index += 1
        self.comet1.animate(self.frame_index)
        self.comet2.animate(self.frame_index)
        self.starfield1.alpha = alpha(self.frame_index, 202, 30)
        self.starfield2.alpha = alpha(self.frame_index, 507, 40)
        self.sprite_list.draw()
