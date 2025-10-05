from __future__ import annotations

import time

from castle_setup import create_initial_castles
from turnloop import GameEngine, GameIO


class ConsoleIO(GameIO):
    """Console-based I/O implementation. Can be swapped for pygame later."""

    def display(self, message: str) -> None:
        print(message)

    def prompt(self, message: str) -> str:
        return input(message)

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


def main() -> None:
    io = ConsoleIO()
    engine = GameEngine(create_initial_castles)
    engine.run(io)


if __name__ == "__main__":
    main()
