import arcade

from space_collector.viewer.constants import SCORE_WIDTH, SCORE_HEIGHT


class Score:
    def __init__(self):
        self.sprite_list = arcade.SpriteList()

    def setup(self) -> None:
        self.sprite_list = arcade.SpriteList()
        background = arcade.Sprite("space_collector/viewer/images/score_background.png")
        background.width = SCORE_WIDTH
        background.height = SCORE_HEIGHT
        background.position = SCORE_WIDTH // 2, SCORE_HEIGHT // 2
        self.sprite_list.append(background)

    def draw(self) -> None:
        self.sprite_list.draw()
