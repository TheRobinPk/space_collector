from dataclasses import dataclass


@dataclass
class Planet:
    x: int
    y: int

    def state(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
        }
