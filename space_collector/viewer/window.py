import logging
import random
from pathlib import Path
from queue import Queue

import arcade

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1777
SCREEN_TITLE = "Space collector"


def find_image_files(directory: Path | str) -> list[Path]:
    if isinstance(directory, str):
        directory = Path(directory)
    return [
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix in (".jpg", ".png", ".jpeg")
    ]


class Window(arcade.Window):
    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.input_queue: Queue = Queue()

    def setup(self) -> None:
        self.background_list = arcade.SpriteList()
        background_image = random.choice(
            find_image_files("space_collector/viewer/images/backgrounds")
        )
        background = arcade.Sprite(background_image)
        background.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        background.width = SCREEN_WIDTH
        background.height = SCREEN_HEIGHT
        self.background_list.append(background)

    def on_draw(self):
        if not self.input_queue.empty():
            data = self.input_queue.get()
            # for index, farm in enumerate(self.farms):
            #     farm.update(data["farms"][index])
            #     farm.update_climate(data["events"])
            # self.score.update(data)

        self.clear()
        self.background_list.draw()
        # for farm_background in self.farm_backgrounds:
        #     farm_background.draw()
        # for farm in self.farms:
        #     farm.draw()
        # self.score.draw()


def gui_thread(window):
    try:
        window.setup()
        arcade.run()
    except Exception:  # noqa: PIE786
        logging.exception("uncaught exception")
