from dataclasses import dataclass


@dataclass
class Spaceship:
    id: int
    x: int
    y: int
    angle: int
    speed: int
    broken: bool
    type: str

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
