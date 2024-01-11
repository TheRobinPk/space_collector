from space_collector.viewer.spaceship import SpaceShip, Collector, Attacker, Explorator

type_name_to_class = {
    "collector": Collector,
    "attacker": Attacker,
    "exlorator": Explorator,
}


class Player:
    def __init__(self, team: int) -> None:
        self.name = ""
        self.blocked = True
        self.orientation = "S"
        self.spaceships: list[SpaceShip] = []
        self.team = team

    def update(self, server_data: dict, time: float) -> None:
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
        for index, spaceship_data in enumerate(server_data["spaceships"]):
            self.spaceships[index].update(spaceship_data, time)
