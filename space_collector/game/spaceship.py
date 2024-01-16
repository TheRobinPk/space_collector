import math
from dataclasses import dataclass
from typing import ClassVar

from space_collector.game.constants import DISTANCE_PLANET_COLLECTION, MAP_DIMENSION
from space_collector.game.planet import Planet


def distance(item, other) -> float:
    return math.hypot(other.x - item.x, other.y - item.y)


@dataclass
class Spaceship:
    MAX_SPEED = 1000
    TYPE = "spaceship"

    def __init__(self, id_: int, x: float, y: float, angle: int) -> None:
        self.id = id_
        self.x = x
        self.y = y
        self.angle = angle
        self.speed: int = 0
        self.broken: bool = False

    def update(self, delta_time: float) -> None:
        self.x += delta_time * self.speed * math.cos(math.radians(self.angle))
        self.x = max(0, min(self.x, MAP_DIMENSION))
        self.y += delta_time * self.speed * math.sin(math.radians(self.angle))
        self.y = max(0, min(self.y, MAP_DIMENSION))

    def move(self, angle: int, speed: int) -> None:
        self.angle = angle
        self.speed = speed

    def state(self) -> dict:
        state = {
            "id": self.id,
            "x": int(self.x),
            "y": int(self.y),
            "angle": self.angle,
            "speed": self.speed,
            "broken": self.broken,
            "type": self.TYPE,
        }
        return state


class Collector(Spaceship):
    MAX_SPEED = 1000
    TYPE = "collector"

    def __init__(
        self, id_: int, x: int, y: int, angle: int, planets: list[Planet]
    ) -> None:
        super().__init__(id_, x, y, angle)
        self.collected: int = -1
        self.planets = planets

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        if self.collected == -1:
            nearest_planet = min(self.planets, key=lambda p: distance(self, p))
            if distance(self, nearest_planet) < DISTANCE_PLANET_COLLECTION:
                self.collected = nearest_planet.id

    def state(self) -> dict:
        state = super().state()
        state["collected"] = self.collected
        return state


class Attacker(Spaceship):
    MAX_SPEED = 3000
    TYPE = "attacker"

    def __init__(self, id_: int, x: int, y: int, angle: int) -> None:
        super().__init__(id_, x, y, angle)
        self.fire_started: bool = False
        self.fire_angle: int = 0

    def fire(self, angle: int) -> None:
        self.fire_started = True
        self.fire_angle = angle

    def state(self) -> dict:
        state = super().state()
        state["fire"] = self.fire_started
        state["fire_angle"] = self.fire_angle
        self.fire_started = False  # TODO fix ugly hack
        return state


class Explorer(Spaceship):
    MAX_SPEED = 2000
    TYPE = "explorer"
