from importlib.resources import files

import arcade

from space_collector.viewer.constants import SCORE_WIDTH, SCORE_HEIGHT, TEAM_COLORS


def draw_text(text: str, x: int, y: int, team: int, size: int, font: str) -> None:
    halo_color = (0, 0, 0, 50)
    for offset_x in range(-2, 3):
        for offset_y in range(-2, 3):
            arcade.draw_text(
                text,
                x + offset_x,
                y + offset_y,
                halo_color,
                font_size=size,
                font_name=font,
            )
    arcade.draw_text(text, x, y, TEAM_COLORS[team], font_size=size, font_name=font)


class Score:
    def __init__(self):
        self.sprite_list = arcade.SpriteList()
        self.teams = []

    def setup(self) -> None:
        font_file = files("space_collector.viewer").joinpath("images/Sportrop.ttf")
        image_file = files("space_collector.viewer").joinpath(
            "images/score_background.png"
        )

        arcade.load_font(font_file)
        self.sprite_list = arcade.SpriteList()
        background = arcade.Sprite(image_file)
        background.width = SCORE_WIDTH
        background.height = SCORE_HEIGHT
        background.position = SCORE_WIDTH // 2, SCORE_HEIGHT // 2
        self.sprite_list.append(background)

    def draw(self) -> None:
        self.sprite_list.draw()
        for index, team in enumerate(self.teams):
            name, blocked, nb_saved_planets, nb_planets = team
            team_offset = 200 + index * 200

            draw_text(name[:30], 100, team_offset, index, size=25, font="Sportrop")
            if blocked:
                draw_text(
                    "BLOCKED", 100, team_offset - 40, index, size=20, font="Sportrop"
                )
            else:
                draw_text(
                    f"Planets: {nb_saved_planets}/{nb_planets}",
                    100,
                    team_offset - 40,
                    index,
                    size=20,
                    font="Sportrop",
                )

    def update(self, server_data: dict) -> None:
        self.teams.clear()
        for player_data in server_data["players"]:
            nb_planets = len(player_data["planets"])
            nb_saved_planets = len(
                [
                    planet_data
                    for planet_data in player_data["planets"]
                    if planet_data["saved"]
                ]
            )
            self.teams.append(
                (
                    player_data["name"],
                    player_data["blocked"],
                    nb_saved_planets,
                    nb_planets,
                )
            )
