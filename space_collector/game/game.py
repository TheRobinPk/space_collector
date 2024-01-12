import random
from time import perf_counter


from space_collector.game.player import Player
from space_collector.game.planet import Planet


class Game:
    def __init__(self) -> None:
        self.start_time = perf_counter()
        self.last_update_time = self.start_time
        self.players: list[Player] = []
        self.planet_positions = [
            Planet(
                x=random.randint(-3000, 3000),
                y=random.randint(3000, 17000),
                size=random.randint(10, 60),
                id=random.randint(1, 65535),
            )
            for _ in range(random.randint(2, 5))
        ]

    def manage_command(self, command: str) -> str:
        return "OK"

    def add_player(self, player_name: str) -> None:
        if len(self.players) >= 4:
            return
        player = Player(player_name)
        player.reset_spaceships_and_planets(len(self.players), self.planet_positions)
        self.players.append(player)

    def update(self) -> None:
        delta_time = perf_counter() - self.last_update_time
        for player in self.players:
            for spaceship in player.spaceships:
                spaceship.x += 1000 * delta_time
        self.last_update_time += delta_time

    def state(self) -> dict:
        return {
            "time": perf_counter() - self.start_time,
            "players": [player.state() for player in self.players],
        }
