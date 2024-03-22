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


class Score:
    def __init__(self):
        self.sprite_list = arcade.SpriteList()
        self.teams = []
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
        for index, team in enumerate(self.teams):
            name, blocked, nb_saved_planets, nb_planets, score = team
            team_offset = constants.SCORE_TEAM_SIZE + index * constants.SCORE_TEAM_SIZE

            draw_text(
                name[:30],
                constants.SCORE_MARGIN,
                team_offset,
                index,
                size=constants.SCORE_FONT_SIZE,
                font="Sportrop",
            )
            if blocked:
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
                    f"Score: {score}",
                    constants.SCORE_MARGIN,
                    team_offset - constants.SCORE_TEAM_SIZE // 5,
                    index,
                    size=constants.SCORE_FONT_SIZE - 5,
                    font="Sportrop",
                )
                draw_text(
                    f"Planets: {nb_saved_planets}/{nb_planets}",
                    constants.SCORE_MARGIN,
                    team_offset - 2 * constants.SCORE_TEAM_SIZE // 5,
                    index,
                    size=constants.SCORE_FONT_SIZE - 5,
                    font="Sportrop",
                )

    def update(self, server_data: dict) -> None:
        self.time = server_data["time"]
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
                    player_data["score"],
                )
            )
