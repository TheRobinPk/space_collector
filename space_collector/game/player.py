from space_collector.game.spaceship import Spaceship, Collector, Attacker, Explorer


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.blocked = False
        self.orientation = "S"
        self.spaceships: list[Spaceship] = []
        # TODO remove dummy init
        self.spaceships = [
            Collector(1, 100, 0, 270),
            Attacker(2, 200, 0, 270),
            Explorer(3, 300, 0, 270),
        ]

    def state(self) -> dict:
        return {
            "name": self.name,
            "blocked": self.blocked,
            "spaceships": [spaceship.state() for spaceship in self.spaceships],
        }
