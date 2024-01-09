import argparse
import contextlib
import json
import logging
import sys
from time import sleep

MAX_NB_PLAYERS = 4
SERVER_CONNECTION_TIMEOUT = 5


from space_collector.network.data_handler import NetworkError
from space_collector.network.server import ClientData, Server


class Game:
    pass  # TODO


class GameServer(Server):
    def __init__(self: "GameServer", host: str, port: int, fast: bool):
        super().__init__(host, port)
        self.game = Game()
        self.fast = fast

    @property
    def players(self):
        return [client for client in self.clients if not client.spectator]

    def remove_client(self: "GameServer", client: ClientData) -> None:
        self.clients.remove(client)
        if not client.spectator:
            for player in self.game.players:
                if player.name == client.name:
                    player.blocked = True

    def _turn_send_to_clients(self: "GameServer") -> None:
        state = self.game.state()
        logging.info("Sending current state")
        logging.info(state)
        state_json = json.dumps(state) + "\n"
        for client in list(self.clients):
            logging.debug("sending to %s", client.name)
            try:
                client.network.write(state_json)
            except NetworkError:
                logging.exception("Problem sending state to client")
                self.remove_client(client)

    def _turn_receive_from_clients(self: "GameServer") -> None:
        for player in list(self.players):
            # ignore blocked players
            for player in self.game.players:
                if player.name == player.name and player.blocked:
                    continue

            logging.info("Waiting commands from %s", player.name)
            try:
                commands: dict = player.network.read_json(timeout=2)
            except NetworkError:
                logging.exception("timeout")
                self.remove_client(player)
                continue

            logging.debug(commands)
            for player in self.game.players:
                if player.name == player.name:
                    player_farm = player
                    break
            else:
                raise ValueError(f"Player not found ({player.name})")

            for command in commands["commands"]:
                logging.info(command)
                player_farm.add_action(command)

    def _turn(self: "GameServer"):
        # self.game.new_day()
        self._turn_send_to_clients()
        # self.game.log_messages()
        # self.game.clear_event_messages()
        self._turn_receive_from_clients()

    def _wait_connections(self: "GameServer") -> None:
        while not self.players:
            print("Waiting for player clients")
            sleep(1)

        for second in range(1, SERVER_CONNECTION_TIMEOUT + 1):
            print(f"Waiting other players ({second}/{SERVER_CONNECTION_TIMEOUT})")
            if len(self.players) == MAX_NB_PLAYERS:
                break
            sleep(1)

    def run(self: "GameServer") -> None:
        self._wait_connections()

        # for player_name in {player.name for player in self.players}:
        #     self.game.add_player(player_name)
        for day in range(1000):
            logging.info("New game turn %d", day + 1)
            self._turn()
            if not self.fast:
                sleep(0.3)
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Game server.")
    parser.add_argument(
        "-a",
        "--address",
        type=str,
        help="name of server on the network",
        default="localhost",
    )
    parser.add_argument(
        "-p", "--port", type=int, help="location where server listens", default=16210
    )
    parser.add_argument(
        "-f",
        "--fast",
        help="fast simulation",
        action="store_true",
    )

    args = parser.parse_args()

    if args.fast:
        logging.basicConfig(handlers=[logging.NullHandler()])
        with contextlib.redirect_stdout(None), contextlib.redirect_stderr(None):
            GameServer(args.address, args.port, args.fast).run()
    else:
        logging.basicConfig(
            filename="server.log",
            encoding="utf-8",
            level=logging.INFO,
            format=(
                "%(asctime)s [%(levelname)-8s] %(filename)20s(%(lineno)3s):"
                "%(funcName)-20s :: %(message)s"
            ),
            datefmt="%m/%d/%Y %H:%M:%S",
        )
        logging.info("Launching server")
        GameServer(args.address, args.port, args.fast).run()
