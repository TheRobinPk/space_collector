from dataclasses import dataclass
from importlib.resources import files

import arcade

from space_collector.viewer.constants import constants


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
    arcade.draw_text(
        text, x, y, constants.TEAM_COLORS[team], font_size=size, font_name=font
    )


@dataclass(frozen=True)
class TeamData:
    name: str
    blocked: bool
    nb_saved_planets: int
    nb_planets: int
    score: int
    team: int


class Score:
    def __init__(self):
        self.sprite_list = arcade.SpriteList()
        self.teams_data: list[TeamData] = []
        self.time = 0

    def setup(self) -> None:
        font_file = files("space_collector.viewer").joinpath("images/Sportrop.ttf")
        image_file = files("space_collector.viewer").joinpath(
            "images/score_background.png"
        )

        arcade.load_font(font_file)
        self.sprite_list = arcade.SpriteList()
        background = arcade.Sprite(image_file)
        background.width = constants.SCORE_WIDTH
        background.height = constants.SCORE_HEIGHT
        background.position = constants.SCORE_WIDTH // 2, constants.SCORE_HEIGHT // 2
        self.sprite_list.append(background)

    def draw(self) -> None:
        self.sprite_list.draw()
        draw_text(
            f"Time: {self.time:0.2f}",
            constants.SCORE_MARGIN,
            constants.SCORE_HEIGHT - constants.SCORE_TIME_MARGIN,
            1,
            size=constants.SCORE_FONT_SIZE,
            font="Sportrop",
        )
        for index, team_data in enumerate(
            sorted(self.teams_data, key=lambda td: td.score)
        ):
            team_offset = constants.SCORE_TEAM_SIZE + index * constants.SCORE_TEAM_SIZE

            draw_text(
                team_data.name[:30],
                constants.SCORE_MARGIN,
                team_offset,
                team_data.team,
                size=constants.SCORE_FONT_SIZE,
                font="Sportrop",
            )
            if team_data.blocked:
                draw_text(
                    "BLOCKED",
                    constants.SCORE_MARGIN,
                    team_offset - constants.SCORE_TEAM_SIZE // 5,
                    index,
                    size=constants.SCORE_FONT_SIZE - 5,
                    font="Sportrop",
                )
            else:
                draw_text(
                    f"Score: {team_data.score}",
                    constants.SCORE_MARGIN,
                    team_offset - constants.SCORE_TEAM_SIZE // 5,
                    team_data.team,
                    size=constants.SCORE_FONT_SIZE - 5,
                    font="Sportrop",
                )
                draw_text(
                    f"Planets: {team_data.nb_saved_planets}/{team_data.nb_planets}",
                    constants.SCORE_MARGIN,
                    team_offset - 2 * constants.SCORE_TEAM_SIZE // 5,
                    team_data.team,
                    size=constants.SCORE_FONT_SIZE - 5,
                    font="Sportrop",
                )

    def update(self, server_data: dict) -> None:
        self.time = server_data["time"]
        self.teams_data.clear()
        for team, player_data in enumerate(server_data["players"]):
            nb_planets = len(player_data["planets"])
            nb_saved_planets = len(
                [
                    planet_data
                    for planet_data in player_data["planets"]
                    if planet_data["saved"]
                ]
            )
            self.teams_data.append(
                TeamData(
                    name=player_data["name"],
                    blocked=player_data["blocked"],
                    nb_saved_planets=nb_saved_planets,
                    nb_planets=nb_planets,
                    score=player_data["score"],
                    team=team,
                )
            )
