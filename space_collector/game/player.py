from space_collector.game.spaceship import Spaceship, Collector, Attacker, Explorer
from space_collector.game.constants import MAP_DIMENSION
from space_collector.game.planet import Planet


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
            dx = 1
            dy = 0
        elif team == 1:
            self.base_position = (0, MAP_DIMENSION // 2)
            angle = 0
            dx = 0
            dy = -1
        elif team == 2:
            self.base_position = (MAP_DIMENSION // 2, MAP_DIMENSION)
            angle = 270
            dx = -1
            dy = 0
        else:
            self.base_position = (MAP_DIMENSION, MAP_DIMENSION // 2)
            angle = 180
            dx = 0
            dy = 1

        base_x, base_y = self.base_position
        self.spaceships = [
            Attacker(1, base_x, base_y, angle),
            Attacker(2, base_x + 1500 * dx, base_y + 1500 * dy, angle),
            Attacker(3, base_x - 1500 * dx, base_y - 1500 * dy, angle),
            Attacker(4, base_x + 3000 * dx, base_y + 3000 * dy, angle),
            Attacker(5, base_x - 3000 * dx, base_y - 3000 * dy, angle),
            Explorer(6, base_x + 4500 * dx, base_y + 4500 * dy, angle),
            Explorer(7, base_x - 4500 * dx, base_y - 4500 * dy, angle),
            Collector(8, base_x + 6000 * dx, base_y + 6000 * dy, angle),
            Collector(9, base_x - 6000 * dx, base_y - 6000 * dy, angle),
        ]
        for planet_x, planet_y in planet_positions:
            self.planets.append(Planet(base_x + planet_x * dx, base_y + planet_y * dy))

    def state(self) -> dict:
        return {
            "name": self.name,
            "blocked": self.blocked,
            "base_position": self.base_position,
            "spaceships": [spaceship.state() for spaceship in self.spaceships],
            "planets": [planet.state() for planet in self.planets],
        }
