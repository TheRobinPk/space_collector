import math
from dataclasses import dataclass

from space_collector.game.constants import MAP_DIMENSION


@dataclass
class Spaceship:
    id: int
    x: float
    y: float
    angle: int
    speed: int
    broken: bool
    type: str

    def update(self, delta_time: float) -> None:
        self.x += delta_time * self.speed * math.cos(math.radians(self.angle))
        self.x = max(0, min(self.x, MAP_DIMENSION))
        self.y += delta_time * self.speed * math.sin(math.radians(self.angle))
        self.y = max(0, min(self.y, MAP_DIMENSION))

    def state(self) -> dict:
        return {
            "id": self.id,
            "x": int(self.x),
            "y": int(self.y),
            "angle": self.angle,
            "speed": self.speed,
            "broken": self.broken,
            "type": self.type,
        }


class Collector(Spaceship):
    def __init__(self, id_: int, x: int, y: int, angle: int) -> None:
        super().__init__(id_, x, y, angle, 0, False, "collector")


class Attacker(Spaceship):
    def __init__(self, id_: int, x: int, y: int, angle: int) -> None:
        super().__init__(id_, x, y, angle, 0, False, "attacker")


class Explorer(Spaceship):
    def __init__(self, id_: int, x: int, y: int, angle: int) -> None:
        super().__init__(id_, x, y, angle, 0, False, "explorer")
