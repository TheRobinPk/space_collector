import logging

from space_collector.viewer.planet import Planet
from space_collector.viewer.spaceship import SpaceShip, Collector, Attacker, Explorator

type_name_to_class = {
    "collector": Collector,
    "attacker": Attacker,
    "explorer": Explorator,
}


class Player:
    def __init__(self, team: int) -> None:
        self.name = ""
        self.blocked = True
        self.orientation = "S"
        self.spaceships: list[SpaceShip] = []
        self.planets: list[Planet] = []
        self.team = team

    def setup(self) -> None:
        pass

    def draw(self) -> None:
        for planet in self.planets:
            planet.draw()
        for spaceship in self.spaceships:
            spaceship.draw()

    def update(self, server_data: dict, date: float) -> None:
        # logging.info("update player at %f: %s", date, str(server_data))
        self.name = server_data["name"]
        self.blocked = self.blocked

        if not self.spaceships:
            for spaceship_data in server_data["spaceships"]:
                class_ = type_name_to_class[spaceship_data["type"]]
                self.spaceships.append(
                    class_(
                        spaceship_data["x"],
                        spaceship_data["y"],
                        spaceship_data["angle"],
                        self.team,
                    )
                )
                self.spaceships[-1].setup()
        for index, spaceship_data in enumerate(server_data["spaceships"]):
            self.spaceships[index].update(spaceship_data, date)

        if not self.planets:
            for planet_data in server_data["planets"]:
                self.planets.append(
                    Planet(
                        planet_data["x"],
                        planet_data["y"],
                        self.team,
                    )
                )
                self.planets[-1].setup()
        for index, planet_data in enumerate(server_data["planets"]):
            self.planets[index].update(planet_data, date)
