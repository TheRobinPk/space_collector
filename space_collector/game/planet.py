from dataclasses import dataclass


@dataclass
class Planet:
    x: int
    y: int
    size: int
    id: int

    def state(self) -> dict:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "size": self.size,
        }
