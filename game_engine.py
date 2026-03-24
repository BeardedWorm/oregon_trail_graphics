"""
Core game engine with refactored event handling and state management
"""

import pygame
from enum import Enum
from typing import Callable, Dict, Optional, List
from models import GameState, PartyMember, Resources, Season


class GameState_Enum(Enum):
    """Game state modes."""
    MENU = "menu"
    TRAVEL = "travel"
    HUNT = "hunt"
    REST = "rest"
    SHOP = "shop"
    STATUS = "status"
    EVENT = "event"
    GAME_OVER = "game_over"
    VICTORY = "victory"


class InputHandler:
    """Handles keyboard and mouse input."""
    
    def __init__(self):
        """Initialize input handler."""
        self.key_callbacks = {}
        self.mouse_callbacks = {}
        self.key_states = {}
        self.mouse_pos = (0, 0)
        self.mouse_pressed = False
    
    def register_key_callback(self, key: int, callback: Callable, 
                            key_type: str = 'down'):
        """Register keyboard callback.
        
        Args:
            key: Pygame key constant
            callback: Function to call
            key_type: 'down', 'up', or 'held'
        """
        callback_key = f'key_{key}_{key_type}'
        self.key_callbacks[callback_key] = callback
    
    def register_mouse_callback(self, rect: pygame.Rect, callback: Callable,
                               event_type: str = 'click'):
        """Register mouse callback.
        
        Args:
            rect: Clickable rectangle
            callback: Function to call
            event_type: 'click', 'hover', or 'drag'
        """
        callback_key = f'mouse_{id(rect)}_{event_type}'
        self.mouse_callbacks[callback_key] = (rect, callback, event_type)
    
    def process_events(self, events: List[pygame.event.EventType]):
        """Process input events.
        
        Args:
            events: List of pygame events
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._handle_key_down(event)
            elif event.type == pygame.KEYUP:
                self._handle_key_up(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                self._handle_mouse_hover()
    
    def _handle_key_down(self, event):
        """Handle key down event."""
        callback_key = f'key_{event.key}_down'
        if callback_key in self.key_callbacks:
            self.key_callbacks[callback_key]()
        self.key_states[event.key] = True
    
    def _handle_key_up(self, event):
        """Handle key up event."""
        callback_key = f'key_{event.key}_up'
        if callback_key in self.key_callbacks:
            self.key_callbacks[callback_key]()
        self.key_states[event.key] = False
    
    def _handle_mouse_click(self, event):
        """Handle mouse click event."""
        for callback_key, (rect, callback, event_type) in self.mouse_callbacks.items():
            if event_type == 'click' and rect.collidepoint(event.pos):
                callback(event.pos)
    
    def _handle_mouse_hover(self):
        """Handle mouse hover event."""
        for callback_key, (rect, callback, event_type) in self.mouse_callbacks.items():
            if event_type == 'hover' and rect.collidepoint(self.mouse_pos):
                callback(self.mouse_pos)
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if key is currently pressed.
        
        Args:
            key: Pygame key constant
            
        Returns:
            True if key is pressed
        """
        return self.key_states.get(key, False)
    
    def clear_callbacks(self):
        """Clear all callbacks."""
        self.key_callbacks.clear()
        self.mouse_callbacks.clear()


class GameEngine:
    """Core game engine managing state, logic, and rendering."""
    
    def __init__(self, renderer):
        """Initialize game engine.
        
        Args:
            renderer: Renderer instance
        """
        self.renderer = renderer
        self.input_handler = InputHandler()
        self.game_state_enum = GameState_Enum.MENU
        self.game_data = GameState()
        self.running = True
        self.delta_time = 0.0
        self.total_time = 0.0
        
        # Game mode screens
        self.current_screen = None
        self.screen_stack = []
        
        # Callbacks
        self.state_change_callbacks = {}
    
    def initialize_game(self):
        """Initialize a new game."""
        # Create party
        self.game_data.party = [
            PartyMember("You", health=100),
            PartyMember("Spouse", health=100),
            PartyMember("Child 1", health=100),
            PartyMember("Child 2", health=100),
            PartyMember("Child 3", health=100),
        ]
        self.game_data.resources = Resources()
        self.game_data.current_day = 1
        self.game_data.current_season = "Spring"
        self.game_data.year = 1848
        self.game_data.distance_traveled = 0
        self.game_state_enum = GameState_Enum.TRAVEL
    
    def set_state(self, new_state: GameState_Enum):
        """Change game state.
        
        Args:
            new_state: New game state
        """
        old_state = self.game_state_enum
        self.game_state_enum = new_state
        
        if new_state in self.state_change_callbacks:
            self.state_change_callbacks[new_state]()
    
    def register_state_callback(self, state: GameState_Enum, callback: Callable):
        """Register callback for state change.
        
        Args:
            state: Game state
            callback: Function to call
        """
        self.state_change_callbacks[state] = callback
    
    def push_screen(self, screen):
        """Push screen onto stack.
        
        Args:
            screen: Screen to push
        """
        self.screen_stack.append(self.current_screen)
        self.current_screen = screen
    
    def pop_screen(self):
        """Pop screen from stack."""
        if self.screen_stack:
            self.current_screen = self.screen_stack.pop()
    
    def handle_input(self):
        """Process input events."""
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.screen_stack:
                        self.pop_screen()
                    else:
                        self.running = False
        
        self.input_handler.process_events(events)
    
    def update(self, delta_time: float):
        """Update game logic.
        
        Args:
            delta_time: Time since last frame
        """
        self.delta_time = delta_time
        self.total_time += delta_time
        
        # Update current screen if it has update method
        if self.current_screen and hasattr(self.current_screen, 'update'):
            self.current_screen.update(delta_time)
    
    def draw(self):
        """Render the game."""
        self.renderer.clear()
        
        # Draw current screen
        if self.current_screen and hasattr(self.current_screen, 'draw'):
            self.current_screen.draw(self.renderer)
        
        self.renderer.update()
    
    def advance_day(self):
        """Advance to next day."""
        self.game_data.current_day += 1
        
        if self.game_data.current_day > 30:
            self.game_data.current_day = 1
            self._advance_season()
        
        # Daily resource consumption
        daily_consumption = self.game_data.daily_food_consumption()
        self.game_data.resources.food -= daily_consumption
        
        if self.game_data.resources.food < 0:
            self.game_data.resources.food = 0
            self._handle_starvation()
    
    def _advance_season(self):
        """Advance to next season."""
        seasons = ["Spring", "Summer", "Fall", "Winter"]
        current_idx = seasons.index(self.game_data.current_season)
        next_idx = (current_idx + 1) % len(seasons)
        self.game_data.current_season = seasons[next_idx]
        
        if next_idx == 0:  # Wrapped to spring
            self.game_data.year += 1
    
    def _handle_starvation(self):
        """Handle party starvation."""
        # Check for starvation-related illnesses
        for member in self.game_data.alive_members():
            if member.health > 0:
                member.health = max(0, member.health - 10)
    
    def travel(self, distance: int):
        """Travel on the trail.
        
        Args:
            distance: Distance to travel in miles
        """
        self.game_data.distance_traveled += distance
        self.advance_day()
    
    def hunt(self, duration: int) -> int:
        """Go hunting for food.
        
        Args:
            duration: Number of days to hunt
            
        Returns:
            Amount of food obtained
        """
        # Base amount varies by season and ammo available
        base_amount = 100
        
        season_multipliers = {
            "Spring": 1.2,
            "Summer": 1.5,
            "Fall": 1.8,
            "Winter": 0.5
        }
        
        multiplier = season_multipliers.get(self.game_data.current_season, 1.0)
        ammo_available = min(self.game_data.resources.ammunition, 100)
        
        food_obtained = int(base_amount * multiplier * (ammo_available / 100))
        
        self.game_data.resources.food += food_obtained
        self.game_data.resources.ammunition -= min(20, ammo_available)
        
        for _ in range(duration):
            self.advance_day()
        
        return food_obtained
    
    def rest(self, duration: int):
        """Rest at current location.
        
        Args:
            duration: Number of days to rest
        """
        for member in self.game_data.alive_members():
            if member.health < 100:
                member.health = min(100, member.health + 5)
        
        for _ in range(duration):
            self.advance_day()
    
    def check_victory(self) -> bool:
        """Check if party has reached Oregon City.
        
        Returns:
            True if victorious
        """
        return self.game_data.distance_traveled >= 1600
    
    def check_game_over(self) -> bool:
        """Check if game is over.
        
        Returns:
            True if game over (leader dead or out of food)
        """
        if not self.game_data.is_leader_alive():
            return True
        
        if self.game_data.resources.food <= 0 and len(self.game_data.alive_members()) == 0:
            return True
        
        return False
