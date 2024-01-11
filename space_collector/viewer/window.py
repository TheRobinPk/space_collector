import logging
import random
from queue import Queue
from typing import NoReturn

import arcade

from space_collector.viewer.constants import (
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
)
from space_collector.viewer.planet import Planet
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
        self.planets: list[Planet] = [Planet("foo") for _ in range(20)]

    def setup(self) -> None:
        self.background.setup()
        self.score.setup()
        for planet in self.planets:
            planet.setup()

    def on_draw(self):
        if not self.input_queue.empty():
            data = self.input_queue.get()
            # for index, farm in enumerate(self.farms):
            #     farm.update(data["farms"][index])
            #     farm.update_climate(data["events"])
            # self.score.update(data)

        self.clear()
        self.background.draw()
        for planet in self.planets:
            planet.draw()
        self.score.draw()


def gui_thread(window: Window) -> None:
    try:
        window.setup()
        arcade.run()
    except Exception:  # noqa: PIE786
        logging.exception("uncaught exception")
