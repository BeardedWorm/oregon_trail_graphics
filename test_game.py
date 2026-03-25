"""Test suite for Oregon Trail Graphical - Run with: python test_game.py"""

from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from models import GameState, PartyMember, Resources, TrailLocation
from difficulty_settings import DifficultyPresets
from trading_posts import TradingPost, LocationTradeSystem
from fort_stops import Fort, FortSystem
from error_handling import EdgeCaseValidator


def test_game_state():
    """Test GameState initialization."""
    game_state = GameState()
    assert game_state.current_day == 1
    assert game_state.year == 1848
    assert game_state.distance_traveled == 0
    print("✓ GameState creation")


def test_party():
    """Test party members."""
    party = [PartyMember("You"), PartyMember("Spouse")]
    assert len(party) == 2
    assert party[0].is_alive
    print("✓ Party members")


def test_resources():
    """Test resources."""
    resources = Resources()
    assert resources.food == 800
    assert resources.ammunition == 100
    assert resources.medicine == 20
    assert resources.money == 1600
    print("✓ Resources")


def test_difficulty():
    """Test difficulty settings."""
    easy = DifficultyPresets.EASY
    normal = DifficultyPresets.NORMAL
    hard = DifficultyPresets.HARD
    
    assert easy.name == "Easy"
    assert normal.name == "Normal"
    assert hard.name == "Hard"
    assert easy.food_consumption_multiplier == 0.5
    assert hard.food_consumption_multiplier == 1.5
    print("✓ Difficulty settings")


def test_trading():
    """Test trading posts."""
    assert LocationTradeSystem.has_trading_post("Fort Laramie")
    assert not LocationTradeSystem.has_trading_post("Missouri River")
    post = LocationTradeSystem.get_trading_post("Fort Laramie")
    assert post is not None
    print("✓ Trading posts")


def test_forts():
    """Test forts."""
    assert FortSystem.has_fort("Fort Laramie")
    assert not FortSystem.has_fort("Missouri River")
    fort = FortSystem.get_fort("Fort Laramie")
    assert fort is not None
    print("✓ Forts")


def test_validation():
    """Test validation."""
    party = [PartyMember("You"), PartyMember("Spouse")]
    assert EdgeCaseValidator.validate_party_members(party)
    
    resources = {
        'food': 800, 'ammunition': 100, 'medicine': 20,
        'spare_parts': 10, 'money': 1600
    }
    assert EdgeCaseValidator.validate_resources(resources)
    print("✓ Validation")


def test_locations():
    """Test locations."""
    locations = TrailLocation.all_locations()
    assert len(locations) == 11
    assert locations[0].name == "Missouri River"
    print("✓ Trail locations")


def test_colors():
    """Test colors."""
    assert 'black' in COLORS
    assert 'white' in COLORS
    assert 'green' in COLORS
    assert len(COLORS) == 16
    print("✓ Color palette")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("OREGON TRAIL GRAPHICAL - TEST SUITE")
    print("="*50 + "\n")
    
    try:
        test_game_state()
        test_party()
        test_resources()
        test_difficulty()
        test_trading()
        test_forts()
        test_validation()
        test_locations()
        test_colors()
        
        print("\n" + "="*50)
        print("ALL TESTS PASSED ✓")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
