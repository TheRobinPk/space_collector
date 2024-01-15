import logging

from space_collector.game.spaceship import Spaceship, Collector, Attacker, Explorer
from space_collector.game.constants import MAP_DIMENSION
from space_collector.game.planet import Planet
from space_collector.game.math import Matrix, Vector
from space_collector.game.player_orientations import player_orientations


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.blocked = False
        self.spaceships: list[Spaceship] = []
        self.planets: list[Planet] = []
        self.base_position = (0, 0)

    def reset_spaceships_and_planets(
        self, team: int, planets_data: list[Planet]
    ) -> None:
        orientation = player_orientations[team]
        angle = orientation.angle
        self.base_position = orientation.base_position

        base_x, base_y = self.base_position
        origin_x_unit = Vector([1, 0])
        x_unit = orientation.matrix @ origin_x_unit
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

        for planet_data in planets_data:
            planet_position = Vector([planet_data.x, planet_data.y])
            rotated_planet = orientation.rotate_around_base(planet_position)
            planet = Planet(*(rotated_planet), planet_data.size, planet_data.id)
            self.planets.append(planet)

    def manage_command(self, command_str: str) -> str:
        if self.blocked:
            return "BLOCKED"
        command = command_str.split()
        for command_type in ("MOVE", "FIRE"):
            if command[0] == command_type:
                return getattr(self, command_type.lower())(command[1:])
        raise ValueError(f"Unknown command: {command_str}")

    def spaceship_by_id(self, id_: int) -> Spaceship:
        try:
            return self.spaceships[id_ - 1]
        except IndexError:
            raise ValueError(f"Wrong spaceship ID: {id_}")

    def move(self, parameters: list[str]) -> str:
        ship_id, angle, speed = (int(param) for param in parameters)
        spaceship = self.spaceship_by_id(ship_id)
        spaceship.move(angle, speed)
        return "OK"

    def fire(self, parameters: list[str]) -> str:
        ship_id, angle = (int(param) for param in parameters)
        spaceship = self.spaceship_by_id(ship_id)
        spaceship.fire(angle)
        return "OK"

    def update(self, delta_time: float) -> None:
        if self.blocked:
            return
        for spaceship in self.spaceships:
            spaceship.update(delta_time)

    def state(self) -> dict:
        return {
            "name": self.name,
            "blocked": self.blocked,
            "base_position": self.base_position,
            "spaceships": [spaceship.state() for spaceship in self.spaceships],
            "planets": [planet.state() for planet in self.planets],
        }
