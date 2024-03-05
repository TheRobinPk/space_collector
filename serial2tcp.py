import argparse
import logging
import random
from contextlib import suppress
from typing import NoReturn

import serial

from space_collector.network.client import Client


class PlayerGameClient(Client):
    def __init__(self, server_addr: str, port: int, serial_port_name: str) -> None:
        username = f"CHANGE_ME_{random.randint(1, 999):03d}"
        logging.basicConfig(
            filename=f"client_{username}.log",
            level=logging.INFO,
            format=(
                "%(asctime)s [%(levelname)-8s] %(filename)20s(%(lineno)3s):%(funcName)-20s :: "
                "%(message)s"
            ),
            datefmt="%m/%d/%Y %H:%M:%S",
        )
        super().__init__(server_addr, port, username, spectator=False)
        self.serial_port = serial.Serial(serial_port_name, 115200, timeout=1)

    def run(self) -> NoReturn:
        logging.info(self.readline())
        self.serial_port.write(b"START\n")
        self.serial_port.flush()
        while True:
            with suppress(serial.SerialTimeoutException):
                command = self.serial_port.readline()
                command = command.decode("utf-8").strip()
                if command:
                    response = self.send_command(command)
                    self.serial_port.write(response.encode("utf-8"))
                    self.serial_port.flush()

    def send_command(self, command: str) -> str:
        if not command.endswith("\n"):
            command += "\n"
        logging.info("Command: %s", command.strip())
        self.send(command)
        response = self.readline() + "\n"
        logging.info(response.strip())
        return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Game client.")
    parser.add_argument(
        "-a",
        "--address",
        type=str,
        help="name of server on the network",
        default="localhost",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="location where server listens",
        default=16210,
    )
    parser.add_argument(
        "-s",
        "--serial",
        type=str,
        help="serial port (115200 8N1)",
        default="/dev/ttyUSB0",
    )
    args = parser.parse_args()

    PlayerGameClient(args.address, args.port, args.serial).run()
