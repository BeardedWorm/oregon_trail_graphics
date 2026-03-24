"""
Graphics renderer for Pygame-based display
Handles all rendering logic for the game
"""

import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, FPS


class Renderer:
    """Handles all rendering operations."""
    
    def __init__(self, screen):
        """Initialize renderer with a pygame screen."""
        self.screen = screen
        self.fonts = {}
        self.sprites = {}
        self.setup_fonts()
    
    def setup_fonts(self):
        """Set up all game fonts."""
        self.fonts['large'] = pygame.font.Font(None, 32)
        self.fonts['medium'] = pygame.font.Font(None, 24)
        self.fonts['small'] = pygame.font.Font(None, 16)
    
    def clear(self, color=None):
        """Clear the screen with a color."""
        if color is None:
            color = COLORS['black']
        self.screen.fill(color)
    
    def draw_text(self, text, x, y, color=COLORS['white'], size='medium'):
        """Draw text on screen."""
        font = self.fonts.get(size, self.fonts['medium'])
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))
    
    def draw_rect(self, x, y, width, height, color, filled=True, thickness=1):
        """Draw a rectangle."""
        rect = pygame.Rect(x, y, width, height)
        if filled:
            pygame.draw.rect(self.screen, color, rect)
        else:
            pygame.draw.rect(self.screen, color, rect, thickness)
    
    def draw_line(self, x1, y1, x2, y2, color, thickness=1):
        """Draw a line."""
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), thickness)
    
    def draw_circle(self, x, y, radius, color, filled=True, thickness=1):
        """Draw a circle."""
        if filled:
            pygame.draw.circle(self.screen, color, (x, y), radius)
        else:
            pygame.draw.circle(self.screen, color, (x, y), radius, thickness)
    
    def update(self):
        """Update display."""
        pygame.display.flip()
    
    def draw_color_palette(self, start_x=10, start_y=80, tile_width=80, tile_height=60):
        """Draw a color palette for debugging."""
        palette_colors = list(COLORS.values())
        color_names = list(COLORS.keys())
        cols = 8
        
        for i, (color, name) in enumerate(zip(palette_colors, color_names)):
            col = i % cols
            row = i // cols
            x = start_x + col * tile_width
            y = start_y + row * tile_height
            
            rect = pygame.Rect(x, y, tile_width, tile_height)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, COLORS['white'], rect, 1)
            
            # Draw color name
            name_surface = self.fonts['small'].render(name, True, 
                                                      COLORS['white'] if sum(color) < 256 else COLORS['black'])
            self.screen.blit(name_surface, (x + 5, y + 25))
    
    def draw_hud_background(self):
        """Draw a simple HUD background."""
        # Top bar
        self.draw_rect(0, 0, WINDOW_WIDTH, 40, COLORS['cyan'])
        
        # Bottom bar
        self.draw_rect(0, WINDOW_HEIGHT - 30, WINDOW_WIDTH, 30, COLORS['blue'])
    
    def draw_menu_background(self):
        """Draw a menu background."""
        # Semi-transparent overlay effect (drawn via color)
        self.draw_rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, COLORS['black'])
