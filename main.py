"""
Oregon Trail - Graphical Version
Main entry point for the Pygame-based graphical implementation
"""

import pygame
import sys
import os
from pathlib import Path
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS,
    COLORS, PALETTE_NAME
)
from graphics import Renderer
from game_engine import GameEngine
from screens import TravelScreen
from difficulty_settings import DifficultyLevel
from input_system import InputMode


class Game:
    def __init__(self):
        """Initialize the game."""
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        pygame.init()
        
        # Set up display
        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            flags=pygame.SCALED
        )
        pygame.display.set_caption(WINDOW_TITLE)
        pygame.display.set_icon(pygame.Surface((1, 1)))
        
        # Initialize renderer
        self.renderer = Renderer(self.screen)
        
        # Initialize game engine
        self.engine = GameEngine(self.renderer)
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_started = False
        
        print(f"✓ Pygame initialized ({pygame.version.ver})")
        print(f"✓ Display: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        print(f"✓ Palette: {PALETTE_NAME} (16 colors)")
        print(f"✓ FPS: {FPS}")
        print(f"✓ Renderer initialized")
        print(f"✓ Game engine ready")

    def handle_events(self):
        """Handle user input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Pop screen or exit
                    if self.engine.screen_stack:
                        self.engine.pop_screen()
                    else:
                        self.running = False
                elif event.key == pygame.K_RETURN and not self.game_started:
                    # Start game from main menu
                    self.game_started = True
                    self.engine.initialize_game()
                    self.engine.current_screen = TravelScreen(self.engine)

    def update(self, delta_time: float):
        """Update game logic."""
        self.engine.update(delta_time)

    def draw(self):
        """Render the game."""
        if self.engine.current_screen:
            self.engine.current_screen.draw(self.renderer)
        else:
            # Draw title screen
            self.renderer.clear(COLORS['black'])
            self.renderer.draw_text(
                "The Oregon Trail",
                WINDOW_WIDTH // 2 - 100,
                100,
                COLORS['light_green'],
                'large'
            )
            self.renderer.draw_text(
                "Graphical Version",
                WINDOW_WIDTH // 2 - 80,
                150,
                COLORS['light_green'],
                'small'
            )
            self.renderer.draw_text(
                "Press ENTER to start",
                WINDOW_WIDTH // 2 - 90,
                250,
                COLORS['yellow'],
                'small'
            )
            self.renderer.draw_text(
                "Press ESC to exit",
                WINDOW_WIDTH // 2 - 70,
                300,
                COLORS['cyan'],
                'small'
            )
            self.renderer.update()

    def run(self):
        """Main game loop."""
        print(f"\n{'='*50}")
        print(f"Starting {WINDOW_TITLE}")
        print(f"{'='*50}\n")
        
        while self.running:
            self.handle_events()
            delta_time = self.clock.tick(FPS) / 1000.0
            self.update(delta_time)
            self.draw()

        print(f"\nShutting down...")
        pygame.quit()
        print(f"✓ Game closed\n")
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
