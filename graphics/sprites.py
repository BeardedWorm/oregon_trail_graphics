"""
Sprite system for game objects
"""

import pygame
from config import SPRITE_SCALE, TILE_SIZE


class Sprite:
    """Base sprite class."""
    
    def __init__(self, x, y, width, height, color, image=None):
        """Initialize a sprite."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.animation_frame = 0
    
    def update(self, dt=0):
        """Update sprite state."""
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, surface):
        """Draw the sprite."""
        if not self.visible:
            return
        
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
    
    def move(self, dx, dy):
        """Move sprite by offset."""
        self.x += dx
        self.y += dy
        self.update()
    
    def set_position(self, x, y):
        """Set absolute position."""
        self.x = x
        self.y = y
        self.update()
    
    def collides_with(self, other):
        """Check collision with another sprite."""
        return self.rect.colliderect(other.rect)
    
    def get_bounds(self):
        """Get sprite bounds."""
        return self.rect


class AnimatedSprite(Sprite):
    """Sprite with animation support."""
    
    def __init__(self, x, y, width, height, color, frames=None):
        """Initialize animated sprite."""
        super().__init__(x, y, width, height, color)
        self.frames = frames or []
        self.current_frame = 0
        self.animation_speed = 1
        self.is_animating = False
        self.loop = True
    
    def add_frame(self, image):
        """Add animation frame."""
        self.frames.append(image)
    
    def start_animation(self, speed=1, loop=True):
        """Start animation."""
        self.animation_speed = speed
        self.is_animating = True
        self.loop = loop
        self.current_frame = 0
    
    def stop_animation(self):
        """Stop animation."""
        self.is_animating = False
    
    def update(self, dt=1):
        """Update animation frame."""
        super().update(dt)
        
        if self.is_animating and self.frames:
            self.animation_frame += self.animation_speed * dt
            
            if self.animation_frame >= len(self.frames):
                if self.loop:
                    self.animation_frame = 0
                else:
                    self.animation_frame = len(self.frames) - 1
                    self.is_animating = False
            
            self.current_frame = int(self.animation_frame)
            if self.frames and 0 <= self.current_frame < len(self.frames):
                self.image = self.frames[self.current_frame]
    
    def draw(self, surface):
        """Draw current animation frame."""
        if not self.visible:
            return
        
        if self.frames and 0 <= self.current_frame < len(self.frames):
            surface.blit(self.frames[self.current_frame], self.rect)


class SpriteGroup:
    """Collection of sprites."""
    
    def __init__(self):
        """Initialize sprite group."""
        self.sprites = []
    
    def add(self, sprite):
        """Add sprite to group."""
        self.sprites.append(sprite)
    
    def remove(self, sprite):
        """Remove sprite from group."""
        if sprite in self.sprites:
            self.sprites.remove(sprite)
    
    def update(self, dt=1):
        """Update all sprites."""
        for sprite in self.sprites:
            sprite.update(dt)
    
    def draw(self, surface):
        """Draw all sprites."""
        for sprite in self.sprites:
            sprite.draw(surface)
    
    def get_all(self):
        """Get all sprites."""
        return self.sprites.copy()
    
    def get_visible(self):
        """Get visible sprites."""
        return [s for s in self.sprites if s.visible]
    
    def collisions(self, sprite):
        """Get all sprites colliding with given sprite."""
        return [s for s in self.sprites if s != sprite and sprite.collides_with(s)]
    
    def clear(self):
        """Clear all sprites."""
        self.sprites.clear()
    
    def __len__(self):
        return len(self.sprites)
    
    def __iter__(self):
        return iter(self.sprites)


class TileSprite(Sprite):
    """Sprite for tile-based graphics."""
    
    def __init__(self, grid_x, grid_y, tile_id=0, color=None):
        """Initialize tile sprite."""
        x = grid_x * TILE_SIZE
        y = grid_y * TILE_SIZE
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, color)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_id = tile_id
    
    def set_grid_position(self, grid_x, grid_y):
        """Set position by grid coordinates."""
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = grid_x * TILE_SIZE
        self.y = grid_y * TILE_SIZE
        self.update()
    
    def get_grid_position(self):
        """Get grid coordinates."""
        return (self.grid_x, self.grid_y)


class TextSprite(Sprite):
    """Sprite for rendered text."""
    
    def __init__(self, x, y, text, font, color, background=None):
        """Initialize text sprite."""
        self.text = text
        self.font = font
        self.color = color
        self.background = background
        self.render()
        super().__init__(x, y, self.image.get_width(), self.image.get_height(), color, self.image)
    
    def render(self):
        """Render text to surface."""
        self.image = self.font.render(self.text, True, self.color, self.background)
    
    def set_text(self, text):
        """Update text."""
        self.text = text
        self.render()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
