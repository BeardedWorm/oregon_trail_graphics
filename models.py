"""
Game models and data structures for the graphical Oregon Trail
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Season(Enum):
    SPRING = "Spring"
    SUMMER = "Summer"
    FALL = "Fall"
    WINTER = "Winter"


class Illness(Enum):
    DYSENTERY = "Dysentery"
    CHOLERA = "Cholera"
    TYPHOID = "Typhoid"
    EXHAUSTION = "Exhaustion"


@dataclass
class PartyMember:
    """Represents a party member."""
    name: str
    health: int = 100
    illness: Optional[str] = None
    days_ill: int = 0
    is_alive: bool = True


@dataclass
class Resources:
    """Represents available resources."""
    food: int = 800
    ammunition: int = 100
    spare_parts: int = 10
    medicine: int = 20
    money: int = 1600


@dataclass
class TrailLocation:
    """Represents a location on the trail."""
    name: str
    distance_from_start: int
    description: str = ""

    @staticmethod
    def all_locations():
        """Return all trail locations."""
        return [
            TrailLocation("Missouri River", 0, "Your starting point"),
            TrailLocation("Kansas River Crossing", 70, "First major crossing"),
            TrailLocation("Big Blue River", 170, "Deep river crossing"),
            TrailLocation("Fort Laramie", 500, "First major fort"),
            TrailLocation("Independence Rock", 700, "Famous landmark"),
            TrailLocation("Fort Bridger", 900, "Second major fort"),
            TrailLocation("South Pass", 950, "Mountain pass"),
            TrailLocation("Fort Hall", 1150, "Trading post"),
            TrailLocation("Snake River Crossing", 1350, "Dangerous crossing"),
            TrailLocation("Blue Mountains", 1450, "Final mountain range"),
            TrailLocation("Oregon City", 1600, "Your destination!"),
        ]


@dataclass
class GameState:
    """Represents the current game state."""
    party: List[PartyMember] = field(default_factory=list)
    resources: Resources = field(default_factory=Resources)
    current_day: int = 1
    current_season: str = "Spring"
    year: int = 1848
    distance_traveled: int = 0
    game_over: bool = False
    victory: bool = False
    deaths_log: List[str] = field(default_factory=list)

    def alive_members(self):
        """Get list of alive party members."""
        return [m for m in self.party if m.is_alive]

    def is_leader_alive(self):
        """Check if the leader is still alive."""
        return len(self.party) > 0 and self.party[0].is_alive

    def daily_food_consumption(self):
        """Calculate daily food consumption."""
        return len(self.alive_members()) * 2

    def advance_day(self):
        """Advance to the next day."""
        self.current_day += 1
        if self.current_day > 30:
            self.current_day = 1
            self.advance_season()

    def advance_season(self):
        """Advance to the next season."""
        seasons = ["Spring", "Summer", "Fall", "Winter"]
        current_idx = seasons.index(self.current_season)
        next_idx = (current_idx + 1) % 4
        self.current_season = seasons[next_idx]
        if next_idx == 0:
            self.year += 1

    def get_current_location(self):
        """Get the current location based on distance traveled."""
        locations = TrailLocation.all_locations()
        for location in reversed(locations):
            if self.distance_traveled >= location.distance_from_start:
                return location
        return locations[0]
