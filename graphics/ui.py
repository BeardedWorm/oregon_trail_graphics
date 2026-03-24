"""
Menu system for Oregon Trail
"""

import pygame
from config import COLORS, WINDOW_WIDTH, WINDOW_HEIGHT
from graphics.sprites import Sprite, SpriteGroup, TextSprite


class MenuItem:
    """Represents a single menu item."""
    
    def __init__(self, text, value=None, callback=None):
        """Initialize menu item."""
        self.text = text
        self.value = value or text
        self.callback = callback
        self.selected = False
        self.rect = None
    
    def invoke(self):
        """Call the menu item callback."""
        if self.callback:
            self.callback(self.value)


class Menu:
    """Base menu class."""
    
    def __init__(self, title="Menu", x=0, y=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        """Initialize menu."""
        self.title = title
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.items = []
        self.selected_index = 0
        self.is_open = False
        self.background_color = COLORS['black']
        self.text_color = COLORS['light_white']
        self.selected_color = COLORS['light_green']
        self.title_color = COLORS['light_cyan']
    
    def add_item(self, text, value=None, callback=None):
        """Add menu item."""
        item = MenuItem(text, value, callback)
        self.items.append(item)
        return item
    
    def select_next(self):
        """Select next menu item."""
        if self.items:
            self.selected_index = (self.selected_index + 1) % len(self.items)
    
    def select_previous(self):
        """Select previous menu item."""
        if self.items:
            self.selected_index = (self.selected_index - 1) % len(self.items)
    
    def select_index(self, index):
        """Select item by index."""
        if 0 <= index < len(self.items):
            self.selected_index = index
    
    def get_selected(self):
        """Get selected menu item."""
        if 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
        return None
    
    def invoke_selected(self):
        """Invoke selected menu item."""
        item = self.get_selected()
        if item:
            item.invoke()
    
    def clear(self):
        """Clear all menu items."""
        self.items.clear()
        self.selected_index = 0
    
    def open(self):
        """Open the menu."""
        self.is_open = True
    
    def close(self):
        """Close the menu."""
        self.is_open = False
    
    def handle_input(self, event):
        """Handle input event."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.select_next()
            elif event.key == pygame.K_UP:
                self.select_previous()
            elif event.key == pygame.K_RETURN:
                self.invoke_selected()


class TextMenu(Menu):
    """Menu with text-based display."""
    
    def __init__(self, title="Menu", **kwargs):
        """Initialize text menu."""
        super().__init__(title, **kwargs)
        self.item_spacing = 40
        self.top_padding = 100
    
    def draw(self, surface, renderer):
        """Draw the menu."""
        if not self.is_open:
            return
        
        # Draw background
        pygame.draw.rect(surface, self.background_color, 
                        (self.x, self.y, self.width, self.height))
        
        # Draw title
        renderer.draw_text(
            self.title,
            self.x + self.width // 2 - 100,
            self.y + 30,
            self.title_color,
            'large'
        )
        
        # Draw menu items
        for i, item in enumerate(self.items):
            y = self.y + self.top_padding + i * self.item_spacing
            color = self.selected_color if i == self.selected_index else self.text_color
            
            prefix = ">" if i == self.selected_index else " "
            text = f"{prefix} {item.text}"
            
            renderer.draw_text(
                text,
                self.x + 50,
                y,
                color,
                'medium'
            )


class MainMenu(TextMenu):
    """Main game menu."""
    
    def __init__(self):
        """Initialize main menu."""
        super().__init__("THE OREGON TRAIL")
        self.add_item("New Game")
        self.add_item("Load Game")
        self.add_item("View Leaderboard")
        self.add_item("Options")
        self.add_item("Exit Game")


class PauseMenu(TextMenu):
    """Pause menu during gameplay."""
    
    def __init__(self):
        """Initialize pause menu."""
        super().__init__("PAUSED")
        self.add_item("Resume Game")
        self.add_item("Save Game")
        self.add_item("Load Game")
        self.add_item("Options")
        self.add_item("Exit to Menu")


class DifficultyMenu(TextMenu):
    """Difficulty selection menu."""
    
    def __init__(self):
        """Initialize difficulty menu."""
        super().__init__("SELECT DIFFICULTY")
        self.add_item("Easy (Normal Resources)")
        self.add_item("Normal (Standard)")
        self.add_item("Hard (Scarce Resources)")
        self.add_item("Brutal (Nearly Impossible)")


class MenuSystem:
    """Manages all menus."""
    
    def __init__(self):
        """Initialize menu system."""
        self.menus = {}
        self.current_menu = None
        self.create_default_menus()
    
    def create_default_menus(self):
        """Create default menus."""
        self.add_menu('main', MainMenu())
        self.add_menu('pause', PauseMenu())
        self.add_menu('difficulty', DifficultyMenu())
    
    def add_menu(self, name, menu):
        """Add a menu."""
        self.menus[name] = menu
    
    def get_menu(self, name):
        """Get a menu by name."""
        return self.menus.get(name)
    
    def show_menu(self, name):
        """Show a menu."""
        menu = self.get_menu(name)
        if menu:
            menu.open()
            self.current_menu = name
    
    def hide_menu(self):
        """Hide current menu."""
        if self.current_menu:
            menu = self.menus.get(self.current_menu)
            if menu:
                menu.close()
            self.current_menu = None
    
    def draw(self, surface, renderer):
        """Draw current menu."""
        if self.current_menu:
            menu = self.menus.get(self.current_menu)
            if menu:
                menu.draw(surface, renderer)
    
    def handle_input(self, event):
        """Handle input for current menu."""
        if self.current_menu:
            menu = self.menus.get(self.current_menu)
            if menu:
                menu.handle_input(event)
    
    def is_menu_open(self):
        """Check if any menu is open."""
        return self.current_menu is not None
