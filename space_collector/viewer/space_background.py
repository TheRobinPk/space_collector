import random
from pathlib import Path
import logging

import arcade

from space_collector.viewer.animation import AnimatedValue, Animation
from space_collector.viewer.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCORE_WIDTH
from space_collector.viewer.utils import random_sprite


def alpha(frame: int, period: int, max_value: int) -> int:
    frame %= period
    value = abs(frame / period - 0.5) * 2
    return int(max_value * value)


def linear(alpha: float, min_value: int, max_value: int) -> int:
    return min_value + int((max_value - min_value) * alpha)


class Comet:
    def __init__(self) -> None:
        self.sprite = arcade.Sprite("space_collector/viewer/images/comet.png")
        self.x = AnimatedValue(random.randint(SCORE_WIDTH, SCREEN_WIDTH))
        self.y = AnimatedValue(random.randint(0, SCREEN_HEIGHT))
        self.new_trajectory(0)

    def new_trajectory(self, start_frame: int) -> None:
        self.duration = random.random() * 3
        self.period = int(self.duration * 60)  # TODO à virer
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
        self.start_frame = start_frame

    def animate(self, frame: int) -> None:
        value = (frame - self.start_frame) / self.period
        if value >= 1:
            self.sprite.alpha = 0
            if value >= 2:
                self.new_trajectory(frame)
            return
        self.sprite.position = (self.x.value, self.y.value)
        self.sprite.alpha = int((1 - abs(value - 0.5) * 2) * 255)


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
