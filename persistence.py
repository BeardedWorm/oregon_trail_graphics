"""
Save/load system with JSON persistence and compatibility with graphics version
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from models import GameState, PartyMember, Resources
from pathlib import Path


class SaveGame:
    """Container for game save data."""
    
    def __init__(self, game_state: GameState):
        """Initialize save game.
        
        Args:
            game_state: Current game state
        """
        self.game_state = game_state
        self.save_time = datetime.now().isoformat()
        self.version = "1.0-graphical"
    
    def to_dict(self) -> dict:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation
        """
        party_data = [
            {
                'name': member.name,
                'health': member.health,
                'illness': member.illness,
                'days_ill': member.days_ill,
                'is_alive': member.is_alive,
            }
            for member in self.game_state.party
        ]
        
        return {
            'version': self.version,
            'save_time': self.save_time,
            'game_state': {
                'party': party_data,
                'resources': {
                    'food': self.game_state.resources.food,
                    'ammunition': self.game_state.resources.ammunition,
                    'medicine': self.game_state.resources.medicine,
                    'spare_parts': self.game_state.resources.spare_parts,
                    'money': self.game_state.resources.money,
                },
                'current_day': self.game_state.current_day,
                'current_season': self.game_state.current_season,
                'year': self.game_state.year,
                'distance_traveled': self.game_state.distance_traveled,
                'game_over': self.game_state.game_over,
                'victory': self.game_state.victory,
                'deaths_log': self.game_state.deaths_log,
            }
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'SaveGame':
        """Create from dictionary.
        
        Args:
            data: Dictionary with save data
            
        Returns:
            SaveGame instance
        """
        game_state = GameState()
        
        # Load party
        game_state.party = [
            PartyMember(
                name=member['name'],
                health=member.get('health', 100),
                illness=member.get('illness'),
                days_ill=member.get('days_ill', 0),
                is_alive=member.get('is_alive', True),
            )
            for member in data['game_state'].get('party', [])
        ]
        
        # Load resources
        resources_data = data['game_state'].get('resources', {})
        game_state.resources = Resources(
            food=resources_data.get('food', 800),
            ammunition=resources_data.get('ammunition', 100),
            medicine=resources_data.get('medicine', 20),
            spare_parts=resources_data.get('spare_parts', 10),
            money=resources_data.get('money', 1600),
        )
        
        # Load other state
        game_state.current_day = data['game_state'].get('current_day', 1)
        game_state.current_season = data['game_state'].get('current_season', 'Spring')
        game_state.year = data['game_state'].get('year', 1848)
        game_state.distance_traveled = data['game_state'].get('distance_traveled', 0)
        game_state.game_over = data['game_state'].get('game_over', False)
        game_state.victory = data['game_state'].get('victory', False)
        game_state.deaths_log = data['game_state'].get('deaths_log', [])
        
        # Create SaveGame
        save_game = SaveGame(game_state)
        save_game.version = data.get('version', '1.0-graphical')
        save_game.save_time = data.get('save_time', datetime.now().isoformat())
        
        return save_game


class SaveManager:
    """Manages save file operations."""
    
    def __init__(self, save_dir: str = 'saves'):
        """Initialize save manager.
        
        Args:
            save_dir: Directory for save files
        """
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.current_save = None
    
    def get_save_path(self, slot: int) -> Path:
        """Get path for save slot.
        
        Args:
            slot: Save slot number
            
        Returns:
            Path object
        """
        return self.save_dir / f"save_{slot}.json"
    
    def save_game(self, game_state: GameState, slot: int = 1) -> bool:
        """Save game to slot.
        
        Args:
            game_state: Game state to save
            slot: Save slot number
            
        Returns:
            True if successful
        """
        try:
            save_game = SaveGame(game_state)
            save_path = self.get_save_path(slot)
            
            with open(save_path, 'w') as f:
                json.dump(save_game.to_dict(), f, indent=2)
            
            self.current_save = slot
            return True
        
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, slot: int) -> Optional[GameState]:
        """Load game from slot.
        
        Args:
            slot: Save slot number
            
        Returns:
            GameState or None if not found
        """
        try:
            save_path = self.get_save_path(slot)
            
            if not save_path.exists():
                return None
            
            with open(save_path, 'r') as f:
                data = json.load(f)
            
            save_game = SaveGame.from_dict(data)
            self.current_save = slot
            return save_game.game_state
        
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def delete_save(self, slot: int) -> bool:
        """Delete save file.
        
        Args:
            slot: Save slot number
            
        Returns:
            True if successful
        """
        try:
            save_path = self.get_save_path(slot)
            if save_path.exists():
                save_path.unlink()
                return True
            return False
        
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False
    
    def get_save_info(self, slot: int) -> Optional[dict]:
        """Get info about saved game.
        
        Args:
            slot: Save slot number
            
        Returns:
            Dictionary with save info or None
        """
        try:
            save_path = self.get_save_path(slot)
            
            if not save_path.exists():
                return None
            
            with open(save_path, 'r') as f:
                data = json.load(f)
            
            game_state = data['game_state']
            
            return {
                'slot': slot,
                'save_time': data.get('save_time'),
                'version': data.get('version'),
                'day': game_state.get('current_day'),
                'season': game_state.get('current_season'),
                'year': game_state.get('year'),
                'distance': game_state.get('distance_traveled'),
                'party_alive': len([p for p in game_state.get('party', [])
                                  if p.get('is_alive', True)]),
                'party_total': len(game_state.get('party', [])),
                'game_over': game_state.get('game_over', False),
                'victory': game_state.get('victory', False),
            }
        
        except Exception as e:
            print(f"Error reading save info: {e}")
            return None
    
    def list_saves(self) -> list:
        """List all available saves.
        
        Returns:
            List of save info dictionaries
        """
        saves = []
        for i in range(1, 10):
            info = self.get_save_info(i)
            if info:
                saves.append(info)
        return saves
    
    def get_latest_save(self) -> Optional[GameState]:
        """Load most recent save.
        
        Returns:
            GameState or None
        """
        saves = self.list_saves()
        if not saves:
            return None
        
        latest = max(saves, key=lambda x: x['save_time'])
        return self.load_game(latest['slot'])


class QuickSaveSystem:
    """Automatic quick save system."""
    
    def __init__(self, save_manager: SaveManager, auto_save_interval: float = 60.0):
        """Initialize quick save system.
        
        Args:
            save_manager: Save manager instance
            auto_save_interval: Interval in seconds
        """
        self.save_manager = save_manager
        self.auto_save_interval = auto_save_interval
        self.last_save_time = 0.0
        self.total_saves = 0
    
    def update(self, delta_time: float, game_state: GameState):
        """Update quick save system.
        
        Args:
            delta_time: Time since last frame
            game_state: Current game state
        """
        self.last_save_time += delta_time
        
        if self.last_save_time >= self.auto_save_interval:
            self.quick_save(game_state)
            self.last_save_time = 0.0
    
    def quick_save(self, game_state: GameState) -> bool:
        """Quick save game.
        
        Args:
            game_state: Game state to save
            
        Returns:
            True if successful
        """
        self.total_saves += 1
        return self.save_manager.save_game(game_state, slot=0)
    
    def quick_load(self) -> Optional[GameState]:
        """Quick load game.
        
        Returns:
            GameState or None
        """
        return self.save_manager.load_game(slot=0)


class SaveSlot:
    """Represents a save slot."""
    
    def __init__(self, slot: int, save_manager: SaveManager):
        """Initialize save slot.
        
        Args:
            slot: Slot number
            save_manager: Save manager instance
        """
        self.slot = slot
        self.save_manager = save_manager
        self.is_empty = not self.save_manager.get_save_path(slot).exists()
        self.info = self.save_manager.get_save_info(slot)
    
    def save(self, game_state: GameState) -> bool:
        """Save to this slot.
        
        Args:
            game_state: Game state to save
            
        Returns:
            True if successful
        """
        return self.save_manager.save_game(game_state, self.slot)
    
    def load(self) -> Optional[GameState]:
        """Load from this slot.
        
        Returns:
            GameState or None
        """
        return self.save_manager.load_game(self.slot)
    
    def delete(self) -> bool:
        """Delete this save.
        
        Returns:
            True if successful
        """
        return self.save_manager.delete_save(self.slot)


class SaveLoadUI:
    """UI for save/load screens."""
    
    def __init__(self, save_manager: SaveManager):
        """Initialize save/load UI.
        
        Args:
            save_manager: Save manager instance
        """
        self.save_manager = save_manager
        self.selected_slot = 1
        self.mode = 'load'  # load or save
    
    def get_slot_displays(self) -> list:
        """Get displayable slot information.
        
        Returns:
            List of slot info
        """
        displays = []
        for i in range(1, 10):
            info = self.save_manager.get_save_info(i)
            if info:
                displays.append(info)
            else:
                displays.append({
                    'slot': i,
                    'empty': True,
                })
        return displays
    
    def handle_slot_select(self, slot: int) -> bool:
        """Handle slot selection.
        
        Args:
            slot: Selected slot
            
        Returns:
            True if slot exists (for load mode)
        """
        self.selected_slot = slot
        
        if self.mode == 'load':
            return self.save_manager.get_save_path(slot).exists()
        return True
