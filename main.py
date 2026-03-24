"""
Oregon Trail - Graphical Version
Main entry point for the Pygame-based graphical implementation
"""

import pygame
import sys
from pathlib import Path

# Game constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = "The Oregon Trail - A Computer Game"
FPS = 60

# Color palette (16-color retro)
COLORS = {
    'black': (0, 0, 0),
    'blue': (0, 0, 170),
    'green': (0, 170, 0),
    'cyan': (0, 170, 170),
    'red': (170, 0, 0),
    'magenta': (170, 0, 170),
    'brown': (170, 85, 0),
    'white': (170, 170, 170),
    'gray': (85, 85, 85),
    'light_blue': (85, 85, 255),
    'light_green': (85, 255, 85),
    'light_cyan': (85, 255, 255),
    'light_red': (255, 85, 85),
    'light_magenta': (255, 85, 255),
    'yellow': (255, 255, 85),
    'light_white': (255, 255, 255),
}


class Game:
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 24)

    def handle_events(self):
        """Handle user input and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update game logic."""
        pass

    def draw(self):
        """Render the game."""
        self.screen.fill(COLORS['black'])
        
        # Draw title
        title_surface = self.font.render(
            "The Oregon Trail - Graphical Version", 
            True, 
            COLORS['light_green']
        )
        self.screen.blit(title_surface, (160, 100))
        
        # Draw status
        status_surface = self.font.render(
            "Development in progress - Press ESC to exit", 
            True, 
            COLORS['light_cyan']
        )
        self.screen.blit(status_surface, (140, 150))
        
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
