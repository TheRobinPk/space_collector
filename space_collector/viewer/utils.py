from space_collector.viewer.constants import (
    MAP_DIMENSION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCORE_WIDTH,
)


def map_coord_to_window_coord(x, y) -> tuple[int, int]:
    return (
        int(x / MAP_DIMENSION * (SCREEN_WIDTH - SCORE_WIDTH)) + SCORE_WIDTH,
        int(y / MAP_DIMENSION * SCREEN_HEIGHT),
    )
