from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Castle:
    """Representation of a single castle on the map."""

    name: str
    point: int
    defense: int
    stability: int
    owner: Optional[str] = None
    cycle: int = 0

    def reset_progress(self) -> None:
        """Reset the development cycle for the castle."""
        self.cycle = 0
        self.owner = None


def create_initial_castles() -> List[Castle]:
    """Create the initial set of castles for a new game."""

    return [
        Castle(name="AKAね", point=10, defense=9, stability=9),
        Castle(name="まどか", point=6, defense=3, stability=7),
        Castle(name="さくら", point=8, defense=1, stability=3),
        Castle(name="のぞみ", point=8, defense=5, stability=6),
    ]
