import logging
from threading import Thread
from time import sleep

from space_collector.network.data_handler import NetworkError
from space_collector.network.client import Client
from space_collector.viewer.window import input_queue, gui_thread


class Viewer(Client):
    def __init__(self: "Viewer", server_addr: str, port: int) -> None:
        super().__init__(server_addr, port, spectator=True)
        self.window_queue = input_queue
        Thread(target=gui_thread, daemon=True).start()

    def run(self: "Viewer") -> None:
        while True:
            try:
                data = self.read_json()
                self.window_queue.put(data)
            except NetworkError:
                logging.exception("End of network communication")
                break
        for _ in range(6):
            sleep(10)
            logging.info("sleeping")
