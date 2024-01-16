import logging
import math
from dataclasses import dataclass
from typing import Callable

from space_collector.game.constants import DISTANCE_PLANET_COLLECTION, MAP_DIMENSION
from space_collector.game.math import Vector
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

    def radar_result(self, team: int) -> str:
        return f"S {team} {self.id} {int(self.x)} {int(self.y)} {int(self.broken)}"

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
        self,
        id_: int,
        x: int,
        y: int,
        angle: int,
        planets: list[Planet],
        base: tuple[int, int],
    ) -> None:
        super().__init__(id_, x, y, angle)
        self.collected: int = -1
        self.planets = planets
        self.base = Vector(base)

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        if self.collected == -1:
            not_collected_planets = [
                planet for planet in self.planets if planet.collected_by == -1
            ]
            if not_collected_planets:
                nearest_planet = min(
                    not_collected_planets, key=lambda p: distance(self, p)
                )
                if distance(self, nearest_planet) < DISTANCE_PLANET_COLLECTION:
                    self.collected = nearest_planet.id
        if self.collected != -1:
            planet = None
            for p in self.planets:
                if p.id == self.collected:
                    planet = p
                    break
            if planet is None:
                logging.error("Collected planet not found: %d", self.collected)
            elif planet.saved:
                planet.collected_by = -1
                self.collected = -1
            else:
                planet.x = self.x
                planet.y = self.y
                planet.collected_by = self.id
                if distance(self, self.base) < DISTANCE_PLANET_COLLECTION:
                    planet.saved = True
                    planet.collected_by = -1
                    self.collected = -1
                    logging.error("PLANET AT HOME")
                    # TODO manage score

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

    def __init__(
        self,
        id_: int,
        x: int,
        y: int,
        angle: int,
        planets: list[Planet],
        all_spaceships: Callable,
        base: tuple[int, int],
    ) -> None:
        super().__init__(id_, x, y, angle)
        self.planets = planets
        self.all_spaceships = all_spaceships
        self.base = base

    def radar(self) -> str:
        # TODO limit distance
        ret = []
        for planet in self.planets:
            ret.append(planet.radar_result())
        for team_id, team in enumerate(self.all_spaceships()):
            for spaceship in team:
                ret.append(spaceship.radar_result(team_id))
        ret.append(f"B {self.base[0]} {self.base[1]}")
        return ",".join(ret)
