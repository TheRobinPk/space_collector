import logging
import random
from queue import Queue

import arcade

from space_collector.viewer.constants import (
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
)
from space_collector.viewer.space_background import SpaceBackground
from space_collector.viewer.score import Score
from space_collector.viewer.spaceship import Attacker, Collector, Explorator, SpaceShip


class Window(arcade.Window):
    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.background = SpaceBackground()
        self.score = Score()
        self.input_queue: Queue = Queue()
        self.spaceships: list[SpaceShip] = [Attacker() for _ in range(5)]
        self.spaceships.extend([Collector() for _ in range(5)])
        self.spaceships.extend([Explorator() for _ in range(5)])
        # self.spaceships_sprite_list = arcade.SpriteList()

    def setup(self) -> None:
        self.background.setup()
        self.score.setup()
        # self.spaceships_sprite_list.clear()
        # for spaceship in self.spaceships:
        #     self.spaceships_sprite_list.append(spaceship.sprite)

    def on_draw(self):
        if not self.input_queue.empty():
            data = self.input_queue.get()
            # for index, farm in enumerate(self.farms):
            #     farm.update(data["farms"][index])
            #     farm.update_climate(data["events"])
            # self.score.update(data)

        self.clear()
        self.background.draw()
        for spaceship in self.spaceships:
            spaceship.animate()
            spaceship.sprite.draw()
        # self.spaceships_sprite_list.draw()
        self.score.draw()


def gui_thread(window):
    try:
        window.setup()
        arcade.run()
    except Exception:  # noqa: PIE786
        logging.exception("uncaught exception")
