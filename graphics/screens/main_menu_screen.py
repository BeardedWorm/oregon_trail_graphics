"""
Main menu screen for the game
"""

import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from graphics.sprites import SpriteGroup
from graphics.ui import MainMenu


class MainMenuScreen:
    """Main menu screen with title and navigation."""
    
    def __init__(self, renderer):
        """Initialize main menu screen."""
        self.renderer = renderer
        self.menu = MainMenu()
        self.sprites = SpriteGroup()
        self.background_scroll = 0
        self.scroll_speed = 0.5
        self.state = 'menu'  # menu, starting_new_game, loading_game, etc.
        
        # Menu callbacks
        self.menu.items[0].callback = self.on_new_game
        self.menu.items[1].callback = self.on_load_game
        self.menu.items[2].callback = self.on_leaderboard
        self.menu.items[3].callback = self.on_options
        self.menu.items[4].callback = self.on_exit
        
        self.menu.open()
    
    def on_new_game(self, value):
        """Handle new game selection."""
        self.state = 'starting_new_game'
        print("Starting new game...")
    
    def on_load_game(self, value):
        """Handle load game selection."""
        self.state = 'loading_game'
        print("Loading game...")
    
    def on_leaderboard(self, value):
        """Handle leaderboard selection."""
        self.state = 'viewing_leaderboard'
        print("Viewing leaderboard...")
    
    def on_options(self, value):
        """Handle options selection."""
        self.state = 'viewing_options'
        print("Opening options...")
    
    def on_exit(self, value):
        """Handle exit selection."""
        self.state = 'exiting'
        print("Exiting game...")
    
    def handle_input(self, event):
        """Handle input."""
        self.menu.handle_input(event)
    
    def update(self, dt=1):
        """Update menu state."""
        self.background_scroll += self.scroll_speed
        if self.background_scroll > WINDOW_WIDTH:
            self.background_scroll = 0
        
        self.sprites.update(dt)
    
    def draw_background(self):
        """Draw scrolling background pattern."""
        # Draw repeating background pattern
        pattern_width = 50
        y = 0
        
        while y < WINDOW_HEIGHT:
            x = self.background_scroll
            while x < WINDOW_WIDTH:
                # Alternate between two colors for pattern
                color = COLORS['blue'] if ((int(x // pattern_width) + int(y // pattern_width)) % 2) == 0 else COLORS['cyan']
                self.renderer.draw_rect(int(x), int(y), pattern_width, pattern_width, color)
                x += pattern_width
            y += pattern_width
    
    def draw_title_box(self):
        """Draw decorative title box."""
        title_box_x = 50
        title_box_y = 30
        title_box_width = WINDOW_WIDTH - 100
        title_box_height = 80
        
        # Draw border
        self.renderer.draw_rect(title_box_x, title_box_y, title_box_width, title_box_height, 
                               COLORS['light_green'], filled=False, thickness=3)
        
        # Draw title
        self.renderer.draw_text(
            "THE OREGON TRAIL",
            title_box_x + 20,
            title_box_y + 15,
            COLORS['light_green'],
            'large'
        )
        
        self.renderer.draw_text(
            "A COMPUTER GAME",
            title_box_x + 40,
            title_box_y + 50,
            COLORS['light_cyan'],
            'medium'
        )
    
    def draw_stats_box(self):
        """Draw game stats box."""
        stats_x = 50
        stats_y = WINDOW_HEIGHT - 120
        stats_width = WINDOW_WIDTH - 100
        stats_height = 100
        
        # Draw border
        self.renderer.draw_rect(stats_x, stats_y, stats_width, stats_height,
                               COLORS['light_cyan'], filled=False, thickness=2)
        
        # Draw stats
        self.renderer.draw_text("Historical Facts:", stats_x + 10, stats_y + 10,
                               COLORS['light_cyan'], 'small')
        self.renderer.draw_text("Distance: 1,600+ miles to Oregon City", stats_x + 10, stats_y + 30,
                               COLORS['light_green'], 'small')
        self.renderer.draw_text("Period: 1840-1869 | Survivors: ~400,000 pioneers", stats_x + 10, stats_y + 50,
                               COLORS['light_green'], 'small')
        self.renderer.draw_text("Press UP/DOWN arrows, then ENTER to select", stats_x + 10, stats_y + 70,
                               COLORS['yellow'], 'small')
    
    def draw(self):
        """Draw main menu screen."""
        self.draw_background()
        self.draw_title_box()
        
        # Draw menu
        self.menu.draw(pygame.display.get_surface(), self.renderer)
        
        self.draw_stats_box()
        
        self.sprites.draw(pygame.display.get_surface())
    
    def get_state(self):
        """Get current menu state."""
        return self.state
    
    def reset_state(self):
        """Reset menu state."""
        self.state = 'menu'
