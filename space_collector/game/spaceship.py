from dataclasses import dataclass


@dataclass
class Spaceship:
    id: int
    x: float
    y: float
    angle: int
    speed: int
    broken: float
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
    def __init__(self, id_: int, x: float, y: float, angle: int) -> None:
        super().__init__(id_, x, y, angle, 0, False, "collector")


class Attacker(Spaceship):
    def __init__(self, id_: int, x: float, y: float, angle: int) -> None:
        super().__init__(id_, x, y, angle, 0, False, "attacker")


class Explorer(Spaceship):
    def __init__(self, id_: int, x: float, y: float, angle: int) -> None:
        super().__init__(id_, x, y, angle, 0, False, "explorer")
