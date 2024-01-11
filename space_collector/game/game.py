from space_collector.game.player import Player


class Game:
    def __init__(self) -> None:
        self.players: list[Player] = []

    def manage_command(self, command: str) -> str:
        return "OK"
