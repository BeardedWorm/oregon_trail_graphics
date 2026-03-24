"""
Asset loading and management
"""

import os
import pygame
from pathlib import Path
from config import ASSET_DIR, SPRITE_DIR, FONT_DIR, TILE_DIR, UI_DIR


class AssetLoader:
    """Loads and manages game assets."""
    
    def __init__(self):
        """Initialize asset loader."""
        self.sprites = {}
        self.fonts = {}
        self.tiles = {}
        self.ui_elements = {}
        self.sounds = {}
        self.music = {}
    
    def load_image(self, name, path):
        """Load an image from file."""
        try:
            if os.path.exists(path):
                image = pygame.image.load(path)
                self.sprites[name] = image
                return image
            else:
                print(f"Warning: Image not found: {path}")
                return None
        except Exception as e:
            print(f"Error loading image {name}: {e}")
            return None
    
    def load_font(self, name, size, path=None):
        """Load a font."""
        try:
            if path and os.path.exists(path):
                font = pygame.font.Font(path, size)
            else:
                font = pygame.font.Font(None, size)
            self.fonts[name] = font
            return font
        except Exception as e:
            print(f"Error loading font {name}: {e}")
            return pygame.font.Font(None, size)
    
    def create_colored_surface(self, name, width, height, color):
        """Create a solid colored surface."""
        surface = pygame.Surface((width, height))
        surface.fill(color)
        self.sprites[name] = surface
        return surface
    
    def get_sprite(self, name):
        """Get a loaded sprite."""
        return self.sprites.get(name)
    
    def get_font(self, name):
        """Get a loaded font."""
        return self.fonts.get(name, pygame.font.Font(None, 24))
    
    def load_sprite_sheet(self, name, path, tile_width, tile_height):
        """Load a sprite sheet and split into tiles."""
        try:
            if not os.path.exists(path):
                print(f"Warning: Sprite sheet not found: {path}")
                return []
            
            sheet = pygame.image.load(path)
            tiles = []
            
            for y in range(0, sheet.get_height(), tile_height):
                for x in range(0, sheet.get_width(), tile_width):
                    tile = sheet.subsurface(pygame.Rect(x, y, tile_width, tile_height))
                    tiles.append(tile.copy())
            
            self.sprites[name] = tiles
            return tiles
        except Exception as e:
            print(f"Error loading sprite sheet {name}: {e}")
            return []
    
    def load_directory(self, directory, pattern='*.png'):
        """Load all images from a directory."""
        try:
            path = Path(directory)
            if not path.exists():
                print(f"Warning: Directory not found: {directory}")
                return {}
            
            loaded = {}
            for file_path in path.glob(pattern):
                name = file_path.stem
                image = self.load_image(name, str(file_path))
                if image:
                    loaded[name] = image
            
            return loaded
        except Exception as e:
            print(f"Error loading directory {directory}: {e}")
            return {}
    
    def scale_sprite(self, name, scale_factor):
        """Scale a sprite."""
        sprite = self.get_sprite(name)
        if sprite and isinstance(sprite, list):
            return [pygame.transform.scale(s, 
                                          (int(s.get_width() * scale_factor),
                                           int(s.get_height() * scale_factor))) 
                    for s in sprite]
        elif sprite:
            new_size = (int(sprite.get_width() * scale_factor),
                       int(sprite.get_height() * scale_factor))
            return pygame.transform.scale(sprite, new_size)
        return None
    
    def rotate_sprite(self, name, angle):
        """Rotate a sprite."""
        sprite = self.get_sprite(name)
        if sprite:
            return pygame.transform.rotate(sprite, angle)
        return None
    
    def list_sprites(self):
        """List all loaded sprites."""
        return list(self.sprites.keys())
    
    def list_fonts(self):
        """List all loaded fonts."""
        return list(self.fonts.keys())
    
    def clear_sprites(self):
        """Clear all sprites."""
        self.sprites.clear()
    
    def clear_fonts(self):
        """Clear all fonts."""
        self.fonts.clear()
    
    def preload_defaults(self):
        """Preload default assets."""
        # Load default fonts
        self.load_font('large', 32)
        self.load_font('medium', 24)
        self.load_font('small', 16)
        
        # Create default colored surfaces
        from config import COLORS
        self.create_colored_surface('default_black', 16, 16, COLORS['black'])
        self.create_colored_surface('default_green', 16, 16, COLORS['light_green'])
        self.create_colored_surface('default_red', 16, 16, COLORS['light_red'])
    
    def __repr__(self):
        return f"AssetLoader(sprites={len(self.sprites)}, fonts={len(self.fonts)})"


# Global asset loader instance
default_loader = AssetLoader()
