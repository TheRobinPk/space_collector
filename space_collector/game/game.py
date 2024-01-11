from time import perf_counter


from space_collector.game.player import Player


class Game:
    def __init__(self) -> None:
        self.start_time = perf_counter()
        self.players: list[Player] = []

    def manage_command(self, command: str) -> str:
        return "OK"

    def add_player(self, player_name: str) -> None:
        if len(self.players) >= 4:
            return
        self.players.append(Player(player_name))

    def state(self) -> dict:
        return {
            "time": perf_counter() - self.start_time,
            "players": [player.state() for player in self.players],
        }
