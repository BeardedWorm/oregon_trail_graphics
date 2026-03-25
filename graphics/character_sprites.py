"""
Character sprite generation and management
"""

import pygame
from config import COLORS, SPRITE_SCALE


class SpriteGenerator:
    """Generate pixel-art sprites programmatically."""
    
    @staticmethod
    def create_character_sprite(size=32, skin_color=COLORS['brown'], 
                               outfit_color=COLORS['blue'], hair_color=COLORS['brown']):
        """Create a simple character sprite."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Head
        head_y = 2
        head_size = 10
        pygame.draw.rect(surface, skin_color, (size//2 - head_size//2, head_y, head_size, head_size))
        
        # Eyes
        eye_y = head_y + 3
        pygame.draw.rect(surface, COLORS['black'], (size//2 - 4, eye_y, 2, 2))
        pygame.draw.rect(surface, COLORS['black'], (size//2 + 2, eye_y, 2, 2))
        
        # Body
        body_y = head_y + head_size
        body_height = 12
        pygame.draw.rect(surface, outfit_color, (size//2 - 4, body_y, 8, body_height))
        
        # Arms
        pygame.draw.rect(surface, skin_color, (size//2 - 8, body_y + 2, 3, 6))
        pygame.draw.rect(surface, skin_color, (size//2 + 5, body_y + 2, 3, 6))
        
        # Legs
        leg_y = body_y + body_height
        pygame.draw.rect(surface, COLORS['black'], (size//2 - 4, leg_y, 3, 8))
        pygame.draw.rect(surface, COLORS['black'], (size//2 + 1, leg_y, 3, 8))
        
        return surface
    
    @staticmethod
    def create_wagon_sprite(size=32, color=COLORS['brown']):
        """Create a wagon sprite."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Wagon body
        pygame.draw.rect(surface, color, (4, 8, 24, 12))
        
        # Wheels
        pygame.draw.circle(surface, COLORS['black'], (8, 22), 3)
        pygame.draw.circle(surface, COLORS['black'], (24, 22), 3)
        
        # Wagon top cover
        points = [(4, 8), (28, 8), (26, 4), (6, 4)]
        pygame.draw.polygon(surface, COLORS['light_white'], points)
        
        return surface
    
    @staticmethod
    def create_oxen_sprite(size=24, color=COLORS['brown']):
        """Create an oxen sprite."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Body
        pygame.draw.ellipse(surface, color, (4, 6, 16, 10))
        
        # Head
        pygame.draw.circle(surface, color, (4, 8), 3)
        
        # Horns
        pygame.draw.line(surface, COLORS['brown'], (2, 4), (1, 2), 1)
        pygame.draw.line(surface, COLORS['brown'], (6, 4), (7, 2), 1)
        
        # Legs
        pygame.draw.line(surface, COLORS['brown'], (8, 16), (8, 22), 2)
        pygame.draw.line(surface, COLORS['brown'], (14, 16), (14, 22), 2)
        
        return surface
    
    @staticmethod
    def create_buffalo_sprite(size=40, color=COLORS['brown']):
        """Create a buffalo sprite."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Body
        pygame.draw.ellipse(surface, color, (8, 10, 24, 16))
        
        # Head
        head_size = 8
        pygame.draw.circle(surface, color, (8, 14), head_size)
        
        # Horns
        pygame.draw.line(surface, COLORS['brown'], (2, 8), (0, 4), 2)
        pygame.draw.line(surface, COLORS['brown'], (14, 8), (16, 4), 2)
        
        # Legs
        pygame.draw.line(surface, COLORS['black'], (12, 26), (12, 36), 2)
        pygame.draw.line(surface, COLORS['black'], (20, 26), (20, 36), 2)
        
        # Hump
        pygame.draw.polygon(surface, color, [(10, 10), (14, 6), (18, 10)])
        
        return surface
    
    @staticmethod
    def create_snake_sprite(size=24, color=None):
        """Create a snake sprite."""
        if color is None:
            color = (0, 255, 0)  # light green
        
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Simple snake: just draw rectangles
        for i in range(3):
            pygame.draw.rect(surface, color, (i * 8, 10, 8, 4))
        
        # Head
        pygame.draw.circle(surface, (255, 100, 100), (size - 3, 12), 2)
        
        return surface
    
    @staticmethod
    def create_particle_sprite(size=8, color=COLORS['yellow']):
        """Create a simple particle sprite."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (size // 2, size // 2), size // 2)
        return surface


class CharacterSpriteSet:
    """Collection of sprite states for a character."""
    
    def __init__(self, name, color_scheme=None):
        """Initialize character sprite set."""
        self.name = name
        self.color_scheme = color_scheme or {
            'skin': COLORS['brown'],
            'outfit': COLORS['blue'],
            'hair': COLORS['brown']
        }
        
        self.sprites = {
            'idle': None,
            'walking_left': None,
            'walking_right': None,
            'walking_up': None,
            'walking_down': None,
            'sick': None,
            'dead': None,
        }
        
        self._generate_sprites()
    
    def _generate_sprites(self):
        """Generate all sprite variants."""
        # Idle sprite
        self.sprites['idle'] = SpriteGenerator.create_character_sprite(
            size=32,
            skin_color=self.color_scheme['skin'],
            outfit_color=self.color_scheme['outfit'],
            hair_color=self.color_scheme['hair']
        )
        
        # Walking sprites (rotate slightly for animation effect)
        for direction in ['walking_left', 'walking_right', 'walking_up', 'walking_down']:
            self.sprites[direction] = self.sprites['idle']
        
        # Sick sprite (grayed out)
        sick_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        base = self.sprites['idle']
        sick_surface.blit(base, (0, 0))
        # Overlay sick effect
        pygame.draw.line(sick_surface, COLORS['light_red'], (10, 8), (14, 12), 1)
        pygame.draw.line(sick_surface, COLORS['light_red'], (14, 8), (10, 12), 1)
        self.sprites['sick'] = sick_surface
        
        # Dead sprite (X over character)
        dead_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        dead_surface.blit(base, (0, 0))
        pygame.draw.line(dead_surface, COLORS['light_red'], (8, 6), (24, 26), 2)
        pygame.draw.line(dead_surface, COLORS['light_red'], (24, 6), (8, 26), 2)
        self.sprites['dead'] = dead_surface
    
    def get_sprite(self, state='idle'):
        """Get sprite for given state."""
        return self.sprites.get(state, self.sprites['idle'])


class SpriteLibrary:
    """Library of all game sprites."""
    
    def __init__(self):
        """Initialize sprite library."""
        self.characters = {}
        self.objects = {}
        self.particles = {}
        self.terrain = {}
        
        self._load_default_sprites()
    
    def _load_default_sprites(self):
        """Load default sprites."""
        # Create character variants
        self.characters['pioneer_1'] = CharacterSpriteSet('Pioneer 1', {
            'skin': COLORS['brown'],
            'outfit': COLORS['blue'],
            'hair': COLORS['brown']
        })
        
        self.characters['pioneer_2'] = CharacterSpriteSet('Pioneer 2', {
            'skin': COLORS['brown'],
            'outfit': COLORS['red'],
            'hair': COLORS['brown']
        })
        
        self.characters['pioneer_3'] = CharacterSpriteSet('Pioneer 3', {
            'skin': COLORS['brown'],
            'outfit': COLORS['green'],
            'hair': COLORS['brown']
        })
        
        # Create objects
        self.objects['wagon'] = SpriteGenerator.create_wagon_sprite()
        self.objects['oxen'] = SpriteGenerator.create_oxen_sprite()
        self.objects['buffalo'] = SpriteGenerator.create_buffalo_sprite()
        self.objects['snake'] = SpriteGenerator.create_snake_sprite()
        
        # Create particles
        self.particles['dust'] = SpriteGenerator.create_particle_sprite(
            size=8, color=COLORS['yellow']
        )
        self.particles['blood'] = SpriteGenerator.create_particle_sprite(
            size=6, color=COLORS['light_red']
        )
        self.particles['heal'] = SpriteGenerator.create_particle_sprite(
            size=8, color=COLORS['light_green']
        )
    
    def get_character(self, character_name, state='idle'):
        """Get character sprite."""
        if character_name in self.characters:
            return self.characters[character_name].get_sprite(state)
        return None
    
    def get_object(self, object_name):
        """Get object sprite."""
        return self.objects.get(object_name)
    
    def get_particle(self, particle_name):
        """Get particle sprite."""
        return self.particles.get(particle_name)
    
    def get_terrain(self, terrain_name):
        """Get terrain sprite."""
        return self.terrain.get(terrain_name)
    
    def list_characters(self):
        """List available characters."""
        return list(self.characters.keys())
    
    def list_objects(self):
        """List available objects."""
        return list(self.objects.keys())
    
    def list_particles(self):
        """List available particles."""
        return list(self.particles.keys())


# Global sprite library
default_sprite_library = SpriteLibrary()
