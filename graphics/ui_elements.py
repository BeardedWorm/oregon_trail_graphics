"""
UI element graphics (buttons, frames, decorations)
"""

import pygame
from config import COLORS
from typing import Tuple, Optional


class ButtonStyle:
    """Button styling."""
    
    def __init__(self, bg_color: Tuple[int, int, int], 
                 border_color: Tuple[int, int, int],
                 text_color: Tuple[int, int, int],
                 hover_color: Tuple[int, int, int] = None,
                 border_width: int = 2):
        """Initialize button style.
        
        Args:
            bg_color: Background color
            border_color: Border color
            text_color: Text color
            hover_color: Hover background color
            border_width: Border width in pixels
        """
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        self.hover_color = hover_color or bg_color
        self.border_width = border_width


class UIElementGenerator:
    """Generate UI element graphics."""
    
    @staticmethod
    def create_button(width: int, height: int, text: str, 
                     style: ButtonStyle, font: Optional[pygame.font.Font] = None,
                     is_hovered: bool = False) -> pygame.Surface:
        """Create button graphic.
        
        Args:
            width: Button width
            height: Button height
            text: Button text
            style: Button style
            font: Font for text
            is_hovered: Whether button is hovered
            
        Returns:
            Button surface
        """
        surface = pygame.Surface((width, height))
        
        # Draw background
        bg_color = style.hover_color if is_hovered else style.bg_color
        surface.fill(bg_color)
        
        # Draw border
        pygame.draw.rect(surface, style.border_color, (0, 0, width, height), 
                        style.border_width)
        
        # Draw text
        if font and text:
            text_surface = font.render(text, True, style.text_color)
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            surface.blit(text_surface, text_rect)
        
        return surface
    
    @staticmethod
    def create_frame(width: int, height: int, border_width: int = 2,
                    border_color: Tuple[int, int, int] = COLORS['green'],
                    bg_color: Tuple[int, int, int] = COLORS['black'],
                    title: str = None, font: Optional[pygame.font.Font] = None) -> pygame.Surface:
        """Create frame graphic.
        
        Args:
            width: Frame width
            height: Frame height
            border_width: Border width
            border_color: Border color
            bg_color: Background color
            title: Optional title
            font: Font for title
            
        Returns:
            Frame surface
        """
        surface = pygame.Surface((width, height))
        surface.fill(bg_color)
        
        # Draw border
        pygame.draw.rect(surface, border_color, (0, 0, width, height), border_width)
        
        # Draw decorative corners
        corner_size = 4
        corners = [
            (0, 0), (width - corner_size, 0),
            (0, height - corner_size), (width - corner_size, height - corner_size)
        ]
        for cx, cy in corners:
            pygame.draw.rect(surface, border_color, (cx, cy, corner_size, corner_size))
        
        # Draw title if provided
        if title and font:
            title_surface = font.render(title, True, border_color)
            surface.blit(title_surface, (border_width + 4, border_width + 2))
        
        return surface
    
    @staticmethod
    def create_progress_bar(width: int, height: int, progress: float,
                           fg_color: Tuple[int, int, int] = COLORS['green'],
                           bg_color: Tuple[int, int, int] = COLORS['black'],
                           border_color: Tuple[int, int, int] = COLORS['green']) -> pygame.Surface:
        """Create progress bar graphic.
        
        Args:
            width: Bar width
            height: Bar height
            progress: Progress 0-1
            fg_color: Foreground color
            bg_color: Background color
            border_color: Border color
            
        Returns:
            Progress bar surface
        """
        surface = pygame.Surface((width, height))
        surface.fill(bg_color)
        
        # Draw fill
        fill_width = int(width * max(0, min(1, progress)))
        if fill_width > 0:
            pygame.draw.rect(surface, fg_color, (0, 0, fill_width, height))
        
        # Draw border
        pygame.draw.rect(surface, border_color, (0, 0, width, height), 1)
        
        return surface
    
    @staticmethod
    def create_status_bar(width: int, height: int, value: float, max_value: float,
                         color: Tuple[int, int, int] = COLORS['green']) -> pygame.Surface:
        """Create status bar graphic (health, food, etc).
        
        Args:
            width: Bar width
            height: Bar height
            value: Current value
            max_value: Maximum value
            color: Bar color
            
        Returns:
            Status bar surface
        """
        if max_value <= 0:
            progress = 0
        else:
            progress = value / max_value
        
        # Determine bar color based on value
        if progress > 0.66:
            bar_color = COLORS['green']
        elif progress > 0.33:
            bar_color = COLORS['yellow']
        else:
            bar_color = COLORS['red']
        
        return UIElementGenerator.create_progress_bar(width, height, progress,
                                                     bar_color, COLORS['black'],
                                                     color)
    
    @staticmethod
    def create_panel(width: int, height: int, 
                    border_color: Tuple[int, int, int] = COLORS['green'],
                    bg_color: Tuple[int, int, int] = COLORS['black']) -> pygame.Surface:
        """Create panel graphic.
        
        Args:
            width: Panel width
            height: Panel height
            border_color: Border color
            bg_color: Background color
            
        Returns:
            Panel surface
        """
        surface = pygame.Surface((width, height))
        surface.fill(bg_color)
        
        # Draw border
        pygame.draw.rect(surface, border_color, (0, 0, width, height), 2)
        
        # Draw inner border
        pygame.draw.rect(surface, border_color, (1, 1, width - 2, height - 2), 1)
        
        return surface
    
    @staticmethod
    def create_icon(size: int, icon_type: str) -> pygame.Surface:
        """Create icon graphic.
        
        Args:
            size: Icon size
            icon_type: Type of icon (food, ammo, health, etc)
            
        Returns:
            Icon surface
        """
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if icon_type == 'food':
            # Draw meat/food
            pygame.draw.polygon(surface, COLORS['brown'],
                              [(size // 2, 2), (size - 2, size - 2), (2, size - 2)])
        
        elif icon_type == 'ammo':
            # Draw bullet/ammo
            pygame.draw.circle(surface, COLORS['yellow'], (size // 2, size // 2), size // 3)
            pygame.draw.rect(surface, COLORS['yellow'], (size // 3, 0, size // 3, size))
        
        elif icon_type == 'health':
            # Draw health cross
            pygame.draw.rect(surface, COLORS['red'], (size // 4, 0, size // 2, size))
            pygame.draw.rect(surface, COLORS['red'], (0, size // 4, size, size // 2))
        
        elif icon_type == 'medicine':
            # Draw medicine bottle
            pygame.draw.rect(surface, COLORS['cyan'], (size // 3, size // 3, size // 3, size // 2))
            pygame.draw.circle(surface, COLORS['cyan'], (size // 2, size // 4), size // 6)
        
        elif icon_type == 'money':
            # Draw coin
            pygame.draw.circle(surface, COLORS['yellow'], (size // 2, size // 2), size // 2 - 1)
            pygame.draw.circle(surface, COLORS['black'], (size // 2, size // 2), size // 3)
        
        elif icon_type == 'parts':
            # Draw mechanical parts
            pygame.draw.circle(surface, COLORS['gray'], (size // 4, size // 4), 2)
            pygame.draw.circle(surface, COLORS['gray'], (3 * size // 4, size // 4), 2)
            pygame.draw.circle(surface, COLORS['gray'], (size // 2, 3 * size // 4), 2)
            pygame.draw.line(surface, COLORS['gray'], (size // 4, size // 4), 
                           (3 * size // 4, size // 4), 1)
            pygame.draw.line(surface, COLORS['gray'], (size // 2, 3 * size // 4),
                           (size // 2, size // 4), 1)
        
        elif icon_type == 'speed':
            # Draw arrow pointing right
            pygame.draw.polygon(surface, COLORS['green'],
                              [(size - 2, size // 2), (2, size - 2), (2, 2)])
        
        elif icon_type == 'marker':
            # Draw location marker
            pygame.draw.polygon(surface, COLORS['red'],
                              [(size // 2, 2), (size - 2, size - 2), (2, size - 2)])
            pygame.draw.circle(surface, COLORS['yellow'], (size // 2, 3 * size // 5), 
                             size // 5)
        
        return surface
    
    @staticmethod
    def create_divider(width: int, height: int = 2,
                      color: Tuple[int, int, int] = COLORS['green']) -> pygame.Surface:
        """Create divider line.
        
        Args:
            width: Divider width
            height: Divider height
            color: Divider color
            
        Returns:
            Divider surface
        """
        surface = pygame.Surface((width, height))
        surface.fill(color)
        return surface
    
    @staticmethod
    def create_checkerboard(width: int, height: int, 
                           color1: Tuple[int, int, int] = COLORS['black'],
                           color2: Tuple[int, int, int] = COLORS['gray'],
                           square_size: int = 8) -> pygame.Surface:
        """Create checkerboard pattern.
        
        Args:
            width: Pattern width
            height: Pattern height
            color1: First color
            color2: Second color
            square_size: Square size
            
        Returns:
            Checkerboard surface
        """
        surface = pygame.Surface((width, height))
        
        for y in range(0, height, square_size):
            for x in range(0, width, square_size):
                if ((x // square_size) + (y // square_size)) % 2 == 0:
                    color = color1
                else:
                    color = color2
                pygame.draw.rect(surface, color, (x, y, square_size, square_size))
        
        return surface
    
    @staticmethod
    def create_gradient(width: int, height: int,
                       start_color: Tuple[int, int, int],
                       end_color: Tuple[int, int, int],
                       direction: str = 'vertical') -> pygame.Surface:
        """Create gradient surface.
        
        Args:
            width: Gradient width
            height: Gradient height
            start_color: Starting color
            end_color: Ending color
            direction: 'vertical' or 'horizontal'
            
        Returns:
            Gradient surface
        """
        surface = pygame.Surface((width, height))
        
        if direction == 'vertical':
            for y in range(height):
                ratio = y / max(1, height - 1)
                color = tuple(int(start_color[i] + (end_color[i] - start_color[i]) * ratio)
                             for i in range(3))
                pygame.draw.line(surface, color, (0, y), (width, y))
        else:  # horizontal
            for x in range(width):
                ratio = x / max(1, width - 1)
                color = tuple(int(start_color[i] + (end_color[i] - start_color[i]) * ratio)
                             for i in range(3))
                pygame.draw.line(surface, color, (x, 0), (x, height))
        
        return surface


class UIGraphicsLibrary:
    """Library of UI graphics."""
    
    def __init__(self):
        """Initialize UI graphics library."""
        self.buttons = {}
        self.frames = {}
        self.icons = {}
        self.elements = {}
    
    def create_button_style(self, name: str, style: ButtonStyle):
        """Create and store button style.
        
        Args:
            name: Style name
            style: Button style
        """
        self.elements[f'button_style_{name}'] = style
    
    def get_button(self, width: int, height: int, text: str = '',
                  style_name: str = 'default', is_hovered: bool = False,
                  font: Optional[pygame.font.Font] = None) -> pygame.Surface:
        """Get button graphic.
        
        Args:
            width: Button width
            height: Button height
            text: Button text
            style_name: Style name
            is_hovered: Hover state
            font: Font for text
            
        Returns:
            Button surface
        """
        # Default style if not found
        style_key = f'button_style_{style_name}'
        if style_key not in self.elements:
            style = ButtonStyle(COLORS['green'], COLORS['green'], 
                              COLORS['black'], COLORS['light_green'])
        else:
            style = self.elements[style_key]
        
        return UIElementGenerator.create_button(width, height, text, style, font, is_hovered)
    
    def get_icon(self, size: int, icon_type: str) -> pygame.Surface:
        """Get icon graphic.
        
        Args:
            size: Icon size
            icon_type: Icon type
            
        Returns:
            Icon surface
        """
        key = f'icon_{icon_type}_{size}'
        if key not in self.icons:
            self.icons[key] = UIElementGenerator.create_icon(size, icon_type)
        return self.icons[key]
    
    def get_frame(self, width: int, height: int, title: str = '',
                 font: Optional[pygame.font.Font] = None) -> pygame.Surface:
        """Get frame graphic.
        
        Args:
            width: Frame width
            height: Frame height
            title: Frame title
            font: Font for title
            
        Returns:
            Frame surface
        """
        return UIElementGenerator.create_frame(width, height, title=title, font=font)


# Global UI graphics library
default_ui_library = UIGraphicsLibrary()
