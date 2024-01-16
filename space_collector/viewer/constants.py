import colorsys

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1777
SCREEN_TITLE = "Space collector"
SCORE_WIDTH = 500
SCORE_HEIGHT = SCREEN_HEIGHT
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
MAP_MIN_X = int(SCORE_WIDTH + MAP_MARGIN * 1.2)
MAP_MAX_X = int(SCREEN_WIDTH - MAP_MARGIN * 1.2)
MAP_MIN_Y = MAP_MARGIN
MAP_MAX_Y = SCREEN_HEIGHT - MAP_MARGIN
