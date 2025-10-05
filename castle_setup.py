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
        Castle(name="姫路城", point=8, defense=7, stability=4),
        Castle(name="小田原城", point=5, defense=5, stability=5),
        Castle(name="バッキンガム", point=4, defense=2, stability=2),
        Castle(name="甲子園", point=5, defense=3, stability=7),
    ]
