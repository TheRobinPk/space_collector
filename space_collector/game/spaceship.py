import math
from dataclasses import dataclass
from typing import ClassVar

from space_collector.game.constants import DISTANCE_PLANET_COLLECTION, MAP_DIMENSION
from space_collector.game.planet import Planet


def distance(item, other) -> float:
    return math.hypot(other.x - item.x, other.y - item.y)


@dataclass
class Spaceship:
    MAX_SPEED: ClassVar[int]
    id: int
    x: float
    y: float
    angle: int
    speed: int
    broken: bool
    type: str
    fire_started: bool = False
    fire_angle: int = 0
    collected: int = -1

    def update(self, delta_time: float, planets: list[Planet]) -> None:
        self.x += delta_time * self.speed * math.cos(math.radians(self.angle))
        self.x = max(0, min(self.x, MAP_DIMENSION))
        self.y += delta_time * self.speed * math.sin(math.radians(self.angle))
        self.y = max(0, min(self.y, MAP_DIMENSION))
        if self.type == "collector" and self.collected == -1 and planets:
            nearest_planet = min(planets, key=lambda p: distance(self, p))
            if distance(self, nearest_planet) < DISTANCE_PLANET_COLLECTION:
                self.collected = nearest_planet.id

    def move(self, angle: int, speed: int) -> None:
        self.angle = angle
        self.speed = speed

    def fire(self, angle: int) -> None:
        if self.type != "attacker":
            return
        self.fire_started = True
        self.fire_angle = angle

    def state(self) -> dict:
        state = {
            "id": self.id,
            "x": int(self.x),
            "y": int(self.y),
            "angle": self.angle,
            "speed": self.speed,
            "broken": self.broken,
            "type": self.type,
            "fire": self.fire_started,
            "fire_angle": self.fire_angle,
            "collected": self.collected,
        }
        self.fire_started = False  # TODO fix ugly hack
        return state


class Collector(Spaceship):
    MAX_SPEED: ClassVar[int] = 1000

    def __init__(self, id_: int, x: int, y: int, angle: int) -> None:
        super().__init__(id_, x, y, angle, 0, False, "collector")


class Attacker(Spaceship):
    MAX_SPEED: ClassVar[int] = 3000

    def __init__(self, id_: int, x: int, y: int, angle: int) -> None:
        super().__init__(id_, x, y, angle, 0, False, "attacker")


class Explorer(Spaceship):
    MAX_SPEED: ClassVar[int] = 2000

    def __init__(self, id_: int, x: int, y: int, angle: int) -> None:
        super().__init__(id_, x, y, angle, 0, False, "explorer")
