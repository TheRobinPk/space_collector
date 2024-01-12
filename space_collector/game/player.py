import logging

from space_collector.game.spaceship import Spaceship, Collector, Attacker, Explorer
from space_collector.game.constants import MAP_DIMENSION
from space_collector.game.planet import Planet
from space_collector.game.math import Matrix, Vector


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.blocked = False
        self.spaceships: list[Spaceship] = []
        self.planets: list[Planet] = []
        self.base_position = (0, 0)

    def reset_spaceships_and_planets(
        self, team: int, planet_positions: list[tuple[int, int]]
    ) -> None:
        if team == 0:
            self.base_position = (MAP_DIMENSION // 2, 0)
            angle = 90
            matrix = Matrix([[1, 0], [0, 1]])
        elif team == 1:
            self.base_position = (0, MAP_DIMENSION // 2)
            angle = 0
            matrix = Matrix([[0, 1], [-1, 0]])
        elif team == 2:
            self.base_position = (MAP_DIMENSION // 2, MAP_DIMENSION)
            angle = 270
            matrix = Matrix([[-1, 0], [0, -1]])
        else:
            self.base_position = (MAP_DIMENSION, MAP_DIMENSION // 2)
            angle = 180
            matrix = Matrix([[0, -1], [1, 0]])

        base_x, base_y = self.base_position
        origin_x_unit = Vector([1, 0])
        x_unit = matrix @ origin_x_unit
        self.spaceships = [
            Attacker(1, base_x, base_y, angle),
            Attacker(2, base_x + 1500 * x_unit.x, base_y + 1500 * x_unit.y, angle),
            Attacker(3, base_x - 1500 * x_unit.x, base_y - 1500 * x_unit.y, angle),
            Attacker(4, base_x + 3000 * x_unit.x, base_y + 3000 * x_unit.y, angle),
            Attacker(5, base_x - 3000 * x_unit.x, base_y - 3000 * x_unit.y, angle),
            Explorer(6, base_x + 4500 * x_unit.x, base_y + 4500 * x_unit.y, angle),
            Explorer(7, base_x - 4500 * x_unit.x, base_y - 4500 * x_unit.y, angle),
            Collector(8, base_x + 6000 * x_unit.x, base_y + 6000 * x_unit.y, angle),
            Collector(9, base_x - 6000 * x_unit.x, base_y - 6000 * x_unit.y, angle),
        ]
        base_vector = Vector(self.base_position)
        for planet_position in planet_positions:
            rotated_planet = matrix @ Vector(planet_position)
            self.planets.append(Planet(*(base_vector + rotated_planet)))

    def state(self) -> dict:
        return {
            "name": self.name,
            "blocked": self.blocked,
            "base_position": self.base_position,
            "spaceships": [spaceship.state() for spaceship in self.spaceships],
            "planets": [planet.state() for planet in self.planets],
        }
