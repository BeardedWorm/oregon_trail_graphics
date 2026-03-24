"""
Screen implementations for game menus and main gameplay
"""

import pygame
from abc import ABC, abstractmethod
from typing import Callable, Optional, List
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from graphics.ui import Menu, MenuItem
from graphics.screens.main_menu_screen import MainMenuScreen
from input_system import MenuInputHandler, GameplayInputHandler, InputMode


class Screen(ABC):
    """Base screen class."""
    
    def __init__(self):
        """Initialize screen."""
        self.is_active = True
        self.next_screen = None
    
    @abstractmethod
    def handle_input(self, input_handler):
        """Handle input.
        
        Args:
            input_handler: Input handler
        """
        pass
    
    @abstractmethod
    def update(self, delta_time: float):
        """Update screen.
        
        Args:
            delta_time: Time since last frame
        """
        pass
    
    @abstractmethod
    def draw(self, renderer):
        """Draw screen.
        
        Args:
            renderer: Renderer instance
        """
        pass


class MenuScreen(Screen):
    """Base menu screen."""
    
    def __init__(self, menu: Menu):
        """Initialize menu screen.
        
        Args:
            menu: Menu to display
        """
        super().__init__()
        self.menu = menu
        self.input_handler = MenuInputHandler(menu)
    
    def handle_input(self, input_handler):
        """Handle input."""
        for event in pygame.event.get():
            self.input_handler.process_event(event)
    
    def update(self, delta_time: float):
        """Update screen."""
        if hasattr(self.menu, 'update'):
            self.menu.update(delta_time)
    
    def draw(self, renderer):
        """Draw screen."""
        renderer.clear(COLORS['black'])
        
        if hasattr(self.menu, 'draw'):
            self.menu.draw(renderer)
        
        renderer.update()


class TravelScreen(Screen):
    """Main travel screen - displays trail map and party status."""
    
    def __init__(self, game_engine):
        """Initialize travel screen.
        
        Args:
            game_engine: Game engine instance
        """
        super().__init__()
        self.engine = game_engine
        self.input_handler = GameplayInputHandler()
        self._setup_buttons()
    
    def _setup_buttons(self):
        """Set up interactive buttons."""
        # Travel button
        travel_rect = pygame.Rect(50, WINDOW_HEIGHT - 100, 100, 40)
        self.input_handler.register_mouse_button(
            travel_rect,
            self._on_travel_click,
            self._on_travel_hover,
            self._on_travel_hover_exit
        )
        
        # Hunt button
        hunt_rect = pygame.Rect(160, WINDOW_HEIGHT - 100, 100, 40)
        self.input_handler.register_mouse_button(
            hunt_rect,
            self._on_hunt_click,
            self._on_hunt_hover,
            self._on_hunt_hover_exit
        )
        
        # Rest button
        rest_rect = pygame.Rect(270, WINDOW_HEIGHT - 100, 100, 40)
        self.input_handler.register_mouse_button(
            rest_rect,
            self._on_rest_click,
            self._on_rest_hover,
            self._on_rest_hover_exit
        )
        
        # Status button
        status_rect = pygame.Rect(380, WINDOW_HEIGHT - 100, 100, 40)
        self.input_handler.register_mouse_button(
            status_rect,
            self._on_status_click,
            self._on_status_hover,
            self._on_status_hover_exit
        )
    
    def handle_input(self, input_handler):
        """Handle input."""
        for event in pygame.event.get():
            self.input_handler.process_event(event)
    
    def update(self, delta_time: float):
        """Update screen."""
        pass
    
    def draw(self, renderer):
        """Draw screen."""
        renderer.clear(COLORS['black'])
        
        # Draw trail map
        renderer.draw_text(f"Distance: {self.engine.game_data.distance_traveled} miles",
                         20, 20, COLORS['light_green'])
        renderer.draw_text(f"Day {self.engine.game_data.current_day} - {self.engine.game_data.current_season} {self.engine.game_data.year}",
                         20, 40, COLORS['light_green'])
        
        # Draw resources
        renderer.draw_text(f"Food: {self.engine.game_data.resources.food}",
                         20, 80, COLORS['yellow'])
        renderer.draw_text(f"Ammo: {self.engine.game_data.resources.ammunition}",
                         20, 100, COLORS['yellow'])
        renderer.draw_text(f"Money: ${self.engine.game_data.resources.money}",
                         20, 120, COLORS['yellow'])
        
        # Draw party status
        renderer.draw_text("Party Status:", 20, 160, COLORS['light_cyan'])
        for i, member in enumerate(self.engine.game_data.party):
            status = "Alive" if member.is_alive else "Dead"
            renderer.draw_text(f"  {member.name}: {member.health}% - {status}",
                             40, 180 + i * 20, COLORS['white'])
        
        # Draw buttons
        renderer.draw_text("Travel", 60, WINDOW_HEIGHT - 90, COLORS['white'])
        renderer.draw_text("Hunt", 175, WINDOW_HEIGHT - 90, COLORS['white'])
        renderer.draw_text("Rest", 290, WINDOW_HEIGHT - 90, COLORS['white'])
        renderer.draw_text("Status", 395, WINDOW_HEIGHT - 90, COLORS['white'])
        
        renderer.update()
    
    def _on_travel_click(self, pos):
        """Handle travel button click."""
        self.engine.travel(20)
    
    def _on_travel_hover(self):
        """Handle travel button hover."""
        pass
    
    def _on_travel_hover_exit(self):
        """Handle travel button hover exit."""
        pass
    
    def _on_hunt_click(self, pos):
        """Handle hunt button click."""
        self.engine.set_state(GameState_Enum.HUNT)
    
    def _on_hunt_hover(self):
        """Handle hunt button hover."""
        pass
    
    def _on_hunt_hover_exit(self):
        """Handle hunt button hover exit."""
        pass
    
    def _on_rest_click(self, pos):
        """Handle rest button click."""
        self.engine.rest(1)
    
    def _on_rest_hover(self):
        """Handle rest button hover."""
        pass
    
    def _on_rest_hover_exit(self):
        """Handle rest button hover exit."""
        pass
    
    def _on_status_click(self, pos):
        """Handle status button click."""
        self.engine.set_state(GameState_Enum.STATUS)
    
    def _on_status_hover(self):
        """Handle status button hover."""
        pass
    
    def _on_status_hover_exit(self):
        """Handle status button hover exit."""
        pass


class HuntScreen(Screen):
    """Hunting screen."""
    
    def __init__(self, game_engine):
        """Initialize hunt screen.
        
        Args:
            game_engine: Game engine instance
        """
        super().__init__()
        self.engine = game_engine
        self.hunt_time = 0
    
    def handle_input(self, input_handler):
        """Handle input."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Finish hunting
                    self.engine.set_state(GameState_Enum.TRAVEL)
    
    def update(self, delta_time: float):
        """Update screen."""
        self.hunt_time += delta_time
    
    def draw(self, renderer):
        """Draw screen."""
        renderer.clear(COLORS['black'])
        renderer.draw_text("Hunting...", WINDOW_WIDTH // 2 - 40, WINDOW_HEIGHT // 2 - 20,
                         COLORS['light_green'])
        renderer.draw_text("Press ENTER to finish", WINDOW_WIDTH // 2 - 90, WINDOW_HEIGHT // 2 + 20,
                         COLORS['white'])
        renderer.update()


class StatusScreen(Screen):
    """Party status display screen."""
    
    def __init__(self, game_engine):
        """Initialize status screen.
        
        Args:
            game_engine: Game engine instance
        """
        super().__init__()
        self.engine = game_engine
    
    def handle_input(self, input_handler):
        """Handle input."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.engine.set_state(GameState_Enum.TRAVEL)
    
    def update(self, delta_time: float):
        """Update screen."""
        pass
    
    def draw(self, renderer):
        """Draw screen."""
        renderer.clear(COLORS['black'])
        
        # Draw title
        renderer.draw_text("Party Status", WINDOW_WIDTH // 2 - 60, 20,
                         COLORS['light_green'])
        
        # Draw party members
        y = 60
        for member in self.engine.game_data.party:
            status = "✓ Alive" if member.is_alive else "✗ Dead"
            renderer.draw_text(f"{member.name}: {member.health}% HP - {status}",
                             40, y, COLORS['white'])
            y += 30
        
        # Draw resources
        y += 20
        renderer.draw_text("Resources:", 40, y, COLORS['light_cyan'])
        y += 25
        renderer.draw_text(f"Food: {self.engine.game_data.resources.food} units",
                         40, y, COLORS['yellow'])
        y += 20
        renderer.draw_text(f"Ammunition: {self.engine.game_data.resources.ammunition} rounds",
                         40, y, COLORS['yellow'])
        y += 20
        renderer.draw_text(f"Spare Parts: {self.engine.game_data.resources.spare_parts}",
                         40, y, COLORS['yellow'])
        y += 20
        renderer.draw_text(f"Medicine: {self.engine.game_data.resources.medicine}",
                         40, y, COLORS['yellow'])
        y += 20
        renderer.draw_text(f"Money: ${self.engine.game_data.resources.money}",
                         40, y, COLORS['yellow'])
        
        renderer.draw_text("Press ESC to return", 40, WINDOW_HEIGHT - 30,
                         COLORS['light_white'])
        
        renderer.update()


# Import needed for type hints
from game_engine import GameState_Enum
