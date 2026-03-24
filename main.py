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
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        
        print(f"✓ Pygame initialized ({pygame.version.ver})")
        print(f"✓ Display: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        print(f"✓ Palette: {PALETTE_NAME} (16 colors)")
        print(f"✓ FPS: {FPS}")
        print(f"✓ Renderer initialized")

    def handle_events(self):
        """Handle user input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(f"Mouse clicked at: {pos}")

    def update(self):
        """Update game logic."""
        pass

    def draw(self):
        """Render the game."""
        self.renderer.clear(COLORS['black'])
        
        # Draw HUD background
        self.renderer.draw_hud_background()
        
        # Draw title
        self.renderer.draw_text(
            "The Oregon Trail - Graphical Version",
            WINDOW_WIDTH // 2 - 150,
            10,
            COLORS['light_green'],
            'large'
        )
        
        # Draw palette label
        self.renderer.draw_text(
            f"Color Palette: {PALETTE_NAME}",
            20,
            80,
            COLORS['light_cyan'],
            'small'
        )
        
        # Draw color palette
        self.renderer.draw_color_palette()
        
        # Draw status at bottom
        self.renderer.draw_text(
            "Phase 1: Graphics Foundation - Press ESC to exit",
            10,
            WINDOW_HEIGHT - 25,
            COLORS['light_white'],
            'small'
        )
        
        # Update display
        self.renderer.update()

    def run(self):
        """Main game loop."""
        print(f"\n{'='*50}")
        print(f"Starting {WINDOW_TITLE}")
        print(f"{'='*50}\n")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        print(f"\nShutting down...")
        pygame.quit()
        print(f"✓ Game closed\n")
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
