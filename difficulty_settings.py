"""
Difficulty selection and game settings
"""

import pygame
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Optional
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS


class DifficultyLevel(Enum):
    """Game difficulty levels."""
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"


@dataclass
class DifficultySettings:
    """Settings for a difficulty level."""
    
    name: str
    description: str
    
    # Game balance
    starting_money: int
    starting_food: int
    starting_ammunition: int
    starting_medicine: int
    
    # Gameplay mechanics
    food_consumption_multiplier: float
    illness_frequency: float  # 0-1, higher = more frequent
    animal_health_multiplier: float  # affects hunting
    event_frequency_multiplier: float
    
    # Death mechanics
    permadeath_enabled: bool  # if False, party members recover
    full_wipe_on_leader_death: bool
    
    def get_summary(self) -> str:
        """Get difficulty summary.
        
        Returns:
            Summary text
        """
        return f"{self.name}: {self.description}"


class DifficultyPresets:
    """Predefined difficulty presets."""
    
    EASY = DifficultySettings(
        name="Easy",
        description="Plenty of supplies, fewer hazards",
        starting_money=2000,
        starting_food=1200,
        starting_ammunition=150,
        starting_medicine=30,
        food_consumption_multiplier=0.5,
        illness_frequency=0.2,
        animal_health_multiplier=0.7,
        event_frequency_multiplier=0.6,
        permadeath_enabled=False,
        full_wipe_on_leader_death=False,
    )
    
    NORMAL = DifficultySettings(
        name="Normal",
        description="Balanced challenge and survival",
        starting_money=1600,
        starting_food=800,
        starting_ammunition=100,
        starting_medicine=20,
        food_consumption_multiplier=1.0,
        illness_frequency=0.5,
        animal_health_multiplier=1.0,
        event_frequency_multiplier=1.0,
        permadeath_enabled=True,
        full_wipe_on_leader_death=False,
    )
    
    HARD = DifficultySettings(
        name="Hard",
        description="Authentic historical difficulty",
        starting_money=1200,
        starting_food=500,
        starting_ammunition=75,
        starting_medicine=10,
        food_consumption_multiplier=1.5,
        illness_frequency=0.8,
        animal_health_multiplier=1.3,
        event_frequency_multiplier=1.5,
        permadeath_enabled=True,
        full_wipe_on_leader_death=True,
    )
    
    @classmethod
    def get_preset(cls, level: DifficultyLevel) -> DifficultySettings:
        """Get difficulty preset.
        
        Args:
            level: Difficulty level
            
        Returns:
            Difficulty settings
        """
        presets = {
            DifficultyLevel.EASY: cls.EASY,
            DifficultyLevel.NORMAL: cls.NORMAL,
            DifficultyLevel.HARD: cls.HARD,
        }
        return presets.get(level, cls.NORMAL)


class DifficultySelector:
    """Screen for selecting difficulty."""
    
    def __init__(self):
        """Initialize difficulty selector."""
        self.selected_level = DifficultyLevel.NORMAL
        self.selected_index = 1
        self.on_select = None
        self.showing_details = False
    
    def select_level(self, level: DifficultyLevel):
        """Select difficulty level.
        
        Args:
            level: Difficulty level
        """
        self.selected_level = level
        if level == DifficultyLevel.EASY:
            self.selected_index = 0
        elif level == DifficultyLevel.NORMAL:
            self.selected_index = 1
        else:
            self.selected_index = 2
    
    def handle_input(self, event: pygame.event.EventType):
        """Handle input.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.selected_index = max(0, self.selected_index - 1)
                self._update_level()
            
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.selected_index = min(2, self.selected_index + 1)
                self._update_level()
            
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.showing_details = not self.showing_details
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.on_select:
                    self.on_select(self.selected_level)
    
    def _update_level(self):
        """Update selected level from index."""
        levels = [DifficultyLevel.EASY, DifficultyLevel.NORMAL, DifficultyLevel.HARD]
        self.selected_level = levels[self.selected_index]
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw selector.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        surface.fill(COLORS['black'])
        
        # Draw title
        renderer.draw_text("Select Difficulty", WINDOW_WIDTH // 2 - 80, 50,
                         COLORS['light_green'], 'large')
        
        # Draw difficulty options
        difficulties = [
            (DifficultyLevel.EASY, DifficultyPresets.EASY),
            (DifficultyLevel.NORMAL, DifficultyPresets.NORMAL),
            (DifficultyLevel.HARD, DifficultyPresets.HARD),
        ]
        
        x_positions = [100, WINDOW_WIDTH // 2 - 50, WINDOW_WIDTH - 150]
        
        for i, (level, settings) in enumerate(difficulties):
            x = x_positions[i]
            
            # Draw selection box
            if i == self.selected_index:
                box_color = COLORS['light_cyan']
                box_width = 120
            else:
                box_color = COLORS['white']
                box_width = 110
            
            pygame.draw.rect(surface, box_color, (x - 5, 150, box_width, 150), 2)
            
            # Draw difficulty name
            renderer.draw_text(settings.name, x + 10, 160, box_color, 'small')
            
            # Draw brief description
            y_offset = 190
            renderer.draw_text(f"${settings.starting_money}", x + 10, y_offset,
                             COLORS['yellow'], 'small')
            y_offset += 20
            renderer.draw_text(f"Food: {settings.starting_food}", x + 10, y_offset,
                             COLORS['white'], 'small')
            y_offset += 15
            renderer.draw_text(f"Ammo: {settings.starting_ammunition}", x + 10, y_offset,
                             COLORS['white'], 'small')
        
        # Draw detailed info if showing
        if self.showing_details:
            self._draw_details(surface, renderer)
        
        # Draw instructions
        renderer.draw_text("← → to select | ↑ for details | ENTER to confirm",
                         50, WINDOW_HEIGHT - 50, COLORS['light_white'], 'small')
    
    def _draw_details(self, surface: pygame.Surface, renderer):
        """Draw detailed difficulty information."""
        settings = DifficultyPresets.get_preset(self.selected_level)
        
        y = 330
        renderer.draw_text(settings.description, 50, y, COLORS['cyan'], 'small')
        
        y += 50
        
        details = [
            f"Food Consumption: {settings.food_consumption_multiplier}x",
            f"Illness Frequency: {settings.illness_frequency * 100:.0f}%",
            f"Animal Difficulty: {settings.animal_health_multiplier}x",
            f"Event Frequency: {settings.event_frequency_multiplier}x",
            f"Permadeath: {'ON' if settings.permadeath_enabled else 'OFF'}",
        ]
        
        for detail in details:
            renderer.draw_text(detail, 50, y, COLORS['white'], 'small')
            y += 20


class GameSettings:
    """Container for game settings."""
    
    def __init__(self, difficulty: DifficultyLevel = DifficultyLevel.NORMAL):
        """Initialize game settings.
        
        Args:
            difficulty: Difficulty level
        """
        self.difficulty = difficulty
        self.difficulty_settings = DifficultyPresets.get_preset(difficulty)
        self.player_name = "Unnamed"
        self.profession = "Farmer"  # Farmer, Carpenter, Merchant
        self.enable_sound = True
        self.show_gore = True
    
    def apply_difficulty(self, difficulty: DifficultyLevel):
        """Apply difficulty settings.
        
        Args:
            difficulty: Difficulty level
        """
        self.difficulty = difficulty
        self.difficulty_settings = DifficultyPresets.get_preset(difficulty)
    
    def get_starting_resources(self) -> dict:
        """Get starting resources based on settings.
        
        Returns:
            Dictionary of starting resources
        """
        settings = self.difficulty_settings
        return {
            'money': settings.starting_money,
            'food': settings.starting_food,
            'ammunition': settings.starting_ammunition,
            'medicine': settings.starting_medicine,
            'spare_parts': 10,  # Always the same
        }


class SettingsScreen:
    """Game settings screen."""
    
    def __init__(self):
        """Initialize settings screen."""
        self.game_settings = GameSettings()
        self.menu_state = 'main'  # main, difficulty, difficulty_confirm
        self.selected_option = 0
    
    def handle_input(self, event: pygame.event.EventType):
        """Handle input.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = max(0, self.selected_option - 1)
            
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.menu_state == 'main':
                    self.selected_option = min(2, self.selected_option + 1)
                else:
                    self.selected_option = max(0, self.selected_option - 1)
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.menu_state == 'main':
                    if self.selected_option == 0:
                        self.menu_state = 'difficulty'
                    elif self.selected_option == 1:
                        self.game_settings.enable_sound = not self.game_settings.enable_sound
                    elif self.selected_option == 2:
                        self.game_settings.show_gore = not self.game_settings.show_gore
            
            elif event.key == pygame.K_ESCAPE:
                self.menu_state = 'main'
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw settings screen.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        surface.fill(COLORS['black'])
        
        renderer.draw_text("Game Settings", WINDOW_WIDTH // 2 - 70, 20,
                         COLORS['light_green'], 'large')
        
        y = 100
        
        # Current difficulty
        renderer.draw_text(f"Difficulty: {self.game_settings.difficulty.value.upper()}",
                         50, y, COLORS['yellow'], 'small')
        y += 30
        
        # Sound
        sound_status = "ON" if self.game_settings.enable_sound else "OFF"
        renderer.draw_text(f"Sound: {sound_status}", 50, y, COLORS['yellow'], 'small')
        y += 30
        
        # Gore
        gore_status = "ON" if self.game_settings.show_gore else "OFF"
        renderer.draw_text(f"Gore: {gore_status}", 50, y, COLORS['yellow'], 'small')
