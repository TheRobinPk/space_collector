import colorsys
import sys

small_window = False


def __getattr__(name: str):
    if name == "__path__":
        return __name__
    if name == "SCREEN_WIDTH":
        return 800 if small_window else 1777
    if name == "SCREEN_HEIGHT" or name == "SCORE_HEIGHT":
        return 600 if small_window else 1000
    if name == "SCORE_WIDTH":
        return 300 if small_window else 500
    return globals()[name]


SCREEN_TITLE = "Space collector"
TEAM_HUES = {
    0: 0,
    1: 30,
    2: 65,
    3: 130,
}
TEAM_COLORS = {
    team: tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue / 360, 1, 1))
    for team, hue in TEAM_HUES.items()
}

MAP_MARGIN = 170
MAP_MIN_X = int(sys.modules[__name__].SCORE_WIDTH + MAP_MARGIN * 1.2)
MAP_MAX_X = int(sys.modules[__name__].SCREEN_WIDTH - MAP_MARGIN * 1.2)
MAP_MIN_Y = MAP_MARGIN
MAP_MAX_Y = sys.modules[__name__].SCREEN_HEIGHT - MAP_MARGIN
