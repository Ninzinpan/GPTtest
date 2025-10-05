from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Iterable, List, Protocol

from castle_setup import Castle


class GameIO(Protocol):
    """Abstraction over the presentation layer used by the engine."""

    def display(self, message: str) -> None:
        ...

    def prompt(self, message: str) -> str:
        ...

    def sleep(self, seconds: float) -> None:
        ...


class TurnOutcome(Enum):
    CONTINUE = auto()
    RESET = auto()
    COMPLETED = auto()


@dataclass
class GameState:
    castles: List[Castle]
    cpu_points: int = 0
    cpu2_points: int = 0
    player_points: int = 0
    username: str = ""


class GameEngine:
    """Core game loop independent from any rendering framework."""

    TARGET_POINTS = 10

    def __init__(self, castle_factory: Callable[[], Iterable[Castle]]):
        self._castle_factory = castle_factory
        self.state = GameState(castles=[])
        self.reset_state()

    def reset_state(self) -> None:
        self.state = GameState(castles=list(self._castle_factory()))

    def run(self, io: GameIO) -> None:
        """Run the game until completion."""

        while True:
            self.reset_state()
            self._prepare_game(io)
            result = self.main_game_loop(io)
            if result == TurnOutcome.RESET:
                continue
            break

    def _prepare_game(self, io: GameIO) -> None:
        while True:
            ready = io.prompt("準備はいいですか？ (入力: 'start') ").strip().lower()
            if ready == "start":
                break

        self.state.username = io.prompt("あなたの名前は？ ").strip()

    def print_castle_status(self, io: GameIO) -> None:
        io.display("\nキャッスルの現在の所有状況:")
        for castle in self.state.castles:
            owner = castle.owner if castle.owner else "フリー"
            cycle_info = f"開発済{castle.cycle}" if castle.cycle > 0 else ""
            io.display(
                f"- {castle.name}: ポイント {castle.point}, 防御力 {castle.defense} "
                f"({owner} {cycle_info})"
            )

    def handle_victory(self, io: GameIO, winner: str) -> None:
        io.display(f"\n{winner}は、他の全てのキャッスルを寝とろうとしている")
        io.sleep(1)
        for castle in self.state.castles:
            previous_owner = castle.owner if castle.owner else "フリー"
            if previous_owner != winner:
                io.display(f"'{castle.name}'を{previous_owner}から寝とった！")
                io.sleep(1)
            castle.owner = winner

        for castle in self.state.castles:
            if castle.cycle == 0:
                io.display(f"{winner}は'{castle.name}'を妊娠させた♡")
                castle.cycle = 2
                io.sleep(1)

        self.print_castle_status(io)

    def check_for_victory(self, io: GameIO) -> bool:
        if self.state.player_points >= self.TARGET_POINTS:
            io.display(f"\n{self.state.username}は勝利した！")
            self.handle_victory(io, self.state.username)
            return True
        if self.state.cpu_points >= self.TARGET_POINTS:
            io.display("\nCPUは勝利した！")
            self.handle_victory(io, "CPU")
            return True
        if self.state.cpu2_points >= self.TARGET_POINTS:
            io.display("\nCPU2は勝利した！")
            self.handle_victory(io, "CPU2")
            return True
        return False

    def _process_cycles(self, io: GameIO, owner: str) -> None:
        for castle in self.state.castles:
            if castle.cycle > 0 and castle.owner == owner:
                castle.cycle -= 1
                if owner == self.state.username:
                    progress_message = (
                        f"{self.state.username}の'{castle.name}'の周期が1進んだ♡"
                    )
                    complete_message = (
                        f"'{castle.name}'は{self.state.username}の子供を出産した♡"
                    )
                elif owner == "CPU":
                    progress_message = f"CPUの'{castle.name}'の周期が1進んだ♡"
                    complete_message = f"'{castle.name}'はCPUの子供を出産した♡"
                elif owner == "CPU2":
                    progress_message = f"CPU2の'{castle.name}'の周期が1進んだ♡"
                    complete_message = f"'{castle.name}'はCPU2の子供を出産した♡"
                else:
                    progress_message = f"{owner}の'{castle.name}'の周期が1進んだ♡"
                    complete_message = f"'{castle.name}'は{owner}の子供を出産した♡"

                io.display(progress_message)
                io.sleep(1)
                if castle.cycle == 0:
                    io.display(complete_message)
                    points = castle.point
                    if owner == self.state.username:
                        self.state.player_points += points
                        io.sleep(1)
                        io.display(
                            f"{self.state.username}は現在{self.state.player_points}ポイント獲得！"
                        )
                    elif owner == "CPU":
                        self.state.cpu_points += points
                        io.sleep(1)
                        io.display(f"CPUは現在{self.state.cpu_points}ポイント獲得！")
                    elif owner == "CPU2":
                        self.state.cpu2_points += points
                        io.sleep(1)
                        io.display(f"CPU2は現在{self.state.cpu2_points}ポイント獲得！")
                    io.sleep(1)

    def process_player_cycles(self, io: GameIO) -> None:
        self._process_cycles(io, self.state.username)

    def process_cpu_cycles(self, io: GameIO) -> None:
        self._process_cycles(io, "CPU")

    def process_cpu2_cycles(self, io: GameIO) -> None:
        self._process_cycles(io, "CPU2")

    def player_turn(self, io: GameIO) -> TurnOutcome:
        io.sleep(1)
        io.display(f"\n{self.state.username}は誰をナンパ/開発する？")
        io.display(f"CPUのポイント: {self.state.cpu_points}")
        io.display(f"CPU2のポイント: {self.state.cpu2_points}")
        io.display(f"{self.state.username}のポイント: {self.state.player_points}")
        self.print_castle_status(io)

        while True:
            player_input = io.prompt(
                "どのキャッスルを選びますか？ (ゲームをリセットしたい場合は 'reset'  パスしたい場合は 'skip')と入力 "
            ).strip()

            if player_input == "reset":
                io.display("\nゲームをリセットします...")
                io.sleep(1)
                return TurnOutcome.RESET

            if player_input == "skip":
                io.display(f"\n{self.state.username}はパスし、次のターンへ移動します。")
                io.sleep(1)
                return TurnOutcome.CONTINUE

            target = next(
                (castle for castle in self.state.castles if castle.name == player_input),
                None,
            )

            if target and target.owner == self.state.username:
                if target.cycle == 0:
                    io.display(
                        f"\n{self.state.username}は'{target.name}'を開発しようとしている..."
                    )
                    io.sleep(1)
                    success_chance = target.stability / 10
                    if random.random() < success_chance:
                        io.display(f"{self.state.username}は'{target.name}'を妊娠させた♡")
                        target.cycle = 2
                    else:
                        io.display(f"{self.state.username}は'{target.name}'の開発に失敗した！")
                    io.sleep(1)
                    break
                io.display(f"'{target.name}'はすでに開発済です。")
            elif target and target.owner is None:
                io.display(f"{self.state.username}は'{target.name}'をナンパした！")
                io.sleep(1)
                success_chance = (10 - (target.defense / 2)) / 10
                if random.random() < success_chance:
                    io.display(f"{self.state.username}は'{target.name}'を彼女にした♡")
                    target.owner = self.state.username
                else:
                    io.display(f"{self.state.username}は'{target.name}'のナンパに失敗した！")
                io.sleep(1)
                break
            elif target and target.owner != self.state.username and target.cycle == 0:
                io.display(f"{self.state.username}は'{target.name}'を寝とった！")
                io.sleep(1)
                success_chance = (10 + target.stability - target.defense) / 20
                if random.random() < success_chance:
                    io.display(
                        f"{self.state.username}は'{target.owner}'の'{target.name}'を寝とった♡"
                    )
                    target.owner = self.state.username
                else:
                    io.display(f"{self.state.username}は'{target.name}'の寝取りに失敗した！")
                io.sleep(1)
                break
            else:
                io.display(f"{player_input}はナンパ/開発できません。再度選択してください。")
        io.sleep(1)
        return TurnOutcome.CONTINUE

    def cpu_turn(self, io: GameIO) -> None:
        available_castles = [c for c in self.state.castles if c.owner is None]
        developed_castles = [
            c for c in self.state.castles if c.owner == "CPU" and c.cycle == 0
        ]
        owned_by_player = [
            c
            for c in self.state.castles
            if c.owner == self.state.username and c.cycle == 0
        ]

        if developed_castles:
            target = random.choice(developed_castles)
            success_chance = target.stability / 10
            io.display(f"\nCPUは'{target.name}'を開発しようとしている...")
            io.sleep(1)
            if random.random() < success_chance:
                io.display(f"CPUは'{target.name}'を妊娠させた♡")
                target.cycle = 2
            else:
                io.display(f"CPUは'{target.name}'の開発に失敗した！")
        elif available_castles:
            target = random.choice(available_castles)
            io.display(f"\nCPUは'{target.name}'をナンパした！")
            io.sleep(1)
            success_chance = (10 - (target.defense / 2)) / 10
            if random.random() < success_chance:
                io.display(f"CPUは'{target.name}'を彼女にした♡")
                target.owner = "CPU"
            else:
                io.display(f"CPUは'{target.name}'のナンパに失敗した！")
        elif owned_by_player:
            target = random.choice(owned_by_player)
            success_chance = (10 + target.stability - target.defense) / 20
            io.display(f"\nCPUは'{target.name}'を寝とろうとしている...")
            io.sleep(1)
            if random.random() < success_chance:
                io.display(
                    f"CPUは'{self.state.username}'の'{target.name}'を寝とった♡"
                )
                target.owner = "CPU"
            else:
                io.display(f"CPUは'{target.name}'の寝取りに失敗した！")
        io.sleep(1)

    def cpu2_turn(self, io: GameIO) -> None:
        available_castles = [c for c in self.state.castles if c.owner is None]
        developed_castles = [
            c for c in self.state.castles if c.owner == "CPU2" and c.cycle == 0
        ]
        owned_by_player = [
            c
            for c in self.state.castles
            if c.owner == self.state.username and c.cycle == 0
        ]
        owned_by_cpu = [c for c in self.state.castles if c.owner == "CPU" and c.cycle == 0]

        if developed_castles:
            target = random.choice(developed_castles)
            success_chance = target.stability / 10
            io.display(f"\nCPU2は'{target.name}'を開発しようとしている...")
            io.sleep(1)
            if random.random() < success_chance:
                io.display(f"CPU2は'{target.name}'を妊娠させた♡")
                target.cycle = 2
            else:
                io.display(f"CPU2は'{target.name}'の開発に失敗した！")
        elif available_castles:
            target = random.choice(available_castles)
            io.display(f"\nCPU2は'{target.name}'をナンパした！")
            io.sleep(1)
            success_chance = (10 - (target.defense / 2)) / 10
            if random.random() < success_chance:
                io.display(f"CPU2は'{target.name}'を彼女にした♡")
                target.owner = "CPU2"
            else:
                io.display(f"CPU2は'{target.name}'のナンパに失敗した！")
        elif owned_by_player:
            target = random.choice(owned_by_player)
            success_chance = (10 + target.stability - target.defense) / 20
            io.display(f"\nCPU2は'{target.name}'を寝とろうとしている...")
            io.sleep(1)
            if random.random() < success_chance:
                io.display(
                    f"CPU2は'{self.state.username}'の'{target.name}'を寝とった♡"
                )
                target.owner = "CPU2"
            else:
                io.display(f"CPU2は'{target.name}'の寝取りに失敗した！")
        elif owned_by_cpu:
            target = random.choice(owned_by_cpu)
            success_chance = (10 + target.stability - target.defense) / 20
            io.display(f"\nCPU2は'CPU'の'{target.name}'を寝とろうとしている...")
            io.sleep(1)
            if random.random() < success_chance:
                io.display(f"CPU2は'CPU'の'{target.name}'を寝とった♡")
                target.owner = "CPU2"
            else:
                io.display(f"CPU2は'{target.name}'の寝取りに失敗した！")
        io.sleep(1)

    def main_game_loop(self, io: GameIO) -> TurnOutcome:
        while not self.check_for_victory(io):
            result = self.player_turn(io)
            if result == TurnOutcome.RESET:
                return TurnOutcome.RESET
            self.process_player_cycles(io)
            if self.check_for_victory(io):
                break

            self.cpu_turn(io)
            self.process_cpu_cycles(io)
            if self.check_for_victory(io):
                break

            self.cpu2_turn(io)
            self.process_cpu2_cycles(io)
            if self.check_for_victory(io):
                break

        return TurnOutcome.COMPLETED
