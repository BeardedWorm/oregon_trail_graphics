"""
Color palette management for retro graphics
"""

from config import COLORS


class ColorPalette:
    """Manages color palettes for the game."""
    
    # CGA Mode 4 - Classic IBM PC palette
    CGA_PALETTE = {
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
    
    # EGA Palette - Extended palette
    EGA_PALETTE = {
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
    
    # Monochrome - Green screen
    MONOCHROME_GREEN = {
        'black': (0, 0, 0),
        'dark_green': (0, 100, 0),
        'green': (0, 170, 0),
        'light_green': (85, 255, 85),
    }
    
    def __init__(self, palette='cga'):
        """Initialize with a palette."""
        self.palette_name = palette.lower()
        self.palette = self._load_palette()
    
    def _load_palette(self):
        """Load the specified palette."""
        if self.palette_name == 'cga':
            return self.CGA_PALETTE.copy()
        elif self.palette_name == 'ega':
            return self.EGA_PALETTE.copy()
        elif self.palette_name == 'mono':
            return self.MONOCHROME_GREEN.copy()
        else:
            return self.CGA_PALETTE.copy()  # Default to CGA
    
    def get_color(self, name):
        """Get a color by name."""
        return self.palette.get(name, (255, 255, 255))
    
    def get_all_colors(self):
        """Get all colors in the palette."""
        return self.palette.copy()
    
    def get_rgb(self, name):
        """Get RGB values for a color."""
        return self.get_color(name)
    
    def to_hex(self, name):
        """Convert color to hex string."""
        rgb = self.get_color(name)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def lighten(self, name, amount=30):
        """Get a lighter version of a color."""
        r, g, b = self.get_color(name)
        return (min(255, r + amount), min(255, g + amount), min(255, b + amount))
    
    def darken(self, name, amount=30):
        """Get a darker version of a color."""
        r, g, b = self.get_color(name)
        return (max(0, r - amount), max(0, g - amount), max(0, b - amount))
    
    def blend(self, name1, name2, ratio=0.5):
        """Blend two colors."""
        r1, g1, b1 = self.get_color(name1)
        r2, g2, b2 = self.get_color(name2)
        
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        
        return (r, g, b)
    
    def get_contrast_color(self, name):
        """Get a contrasting color (for text on background)."""
        r, g, b = self.get_color(name)
        # Simple brightness calculation
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        if brightness > 128:
            return self.get_color('black')
        else:
            return self.get_color('light_white')
    
    @staticmethod
    def list_palettes():
        """List available palettes."""
        return ['cga', 'ega', 'mono']
    
    def __repr__(self):
        return f"ColorPalette('{self.palette_name}', {len(self.palette)} colors)"


# Global palette instance (use config colors by default)
default_palette = ColorPalette('cga')
