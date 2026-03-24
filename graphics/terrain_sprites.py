"""
Terrain and location graphics generation
"""

import pygame
from config import COLORS, TILE_SIZE


class TerrainTileGenerator:
    """Generate terrain tiles programmatically."""
    
    @staticmethod
    def create_grass_tile(size=32, color=COLORS['green']):
        """Create grass terrain tile."""
        surface = pygame.Surface((size, size))
        surface.fill(color)
        
        # Add grass texture (simple dots)
        for x in range(0, size, 8):
            for y in range(0, size, 8):
                if (x // 8 + y // 8) % 2 == 0:
                    pygame.draw.rect(surface, COLORS['light_green'], (x, y, 4, 4))
        
        return surface
    
    @staticmethod
    def create_dirt_tile(size=32):
        """Create dirt/plain terrain tile."""
        surface = pygame.Surface((size, size))
        surface.fill(COLORS['brown'])
        
        # Add dirt texture
        for x in range(0, size, 4):
            for y in range(0, size, 4):
                if (x // 4 + y // 4) % 3 == 0:
                    pygame.draw.rect(surface, COLORS['yellow'], (x, y, 2, 2))
        
        return surface
    
    @staticmethod
    def create_mountain_tile(size=32):
        """Create mountain terrain tile."""
        surface = pygame.Surface((size, size))
        surface.fill(COLORS['gray'])
        
        # Draw mountain peaks
        peak_points = [(0, size), (size//2, 0), (size, size)]
        pygame.draw.polygon(surface, COLORS['light_white'], peak_points)
        
        # Add shading
        pygame.draw.line(surface, COLORS['black'], (0, size), (size//2, 0), 1)
        
        return surface
    
    @staticmethod
    def create_water_tile(size=32):
        """Create water terrain tile."""
        surface = pygame.Surface((size, size))
        surface.fill(COLORS['blue'])
        
        # Add wave pattern
        for x in range(0, size, 4):
            pygame.draw.line(surface, COLORS['light_blue'], (x, size//2), (x + 2, size//2 + 2), 1)
        
        return surface
    
    @staticmethod
    def create_forest_tile(size=32):
        """Create forest terrain tile."""
        surface = pygame.Surface((size, size))
        surface.fill(COLORS['green'])
        
        # Draw trees (simple triangles)
        tree_coords = [(8, 16), (24, 12), (16, 20)]
        for tx, ty in tree_coords:
            pygame.draw.polygon(surface, COLORS['brown'], 
                              [(tx, ty + 8), (tx - 6, ty), (tx + 6, ty)])
        
        return surface
    
    @staticmethod
    def create_snow_tile(size=32):
        """Create snow terrain tile."""
        surface = pygame.Surface((size, size))
        surface.fill(COLORS['light_white'])
        
        # Add snowflake pattern
        for x in range(0, size, 6):
            for y in range(0, size, 6):
                pygame.draw.circle(surface, COLORS['cyan'], (x, y), 1)
        
        return surface
    
    @staticmethod
    def create_river_tile(size=32):
        """Create river tile."""
        surface = pygame.Surface((size, size))
        surface.fill(COLORS['green'])
        
        # Water in middle
        pygame.draw.rect(surface, COLORS['blue'], (0, size // 3, size, size // 3))
        
        # Water movement effect
        for x in range(0, size, 4):
            pygame.draw.line(surface, COLORS['light_blue'], 
                            (x, size // 2), (x + 2, size // 2 + 1), 1)
        
        return surface


class LocationGraphics:
    """Graphics for trail locations."""
    
    @staticmethod
    def create_fort_sprite(size=40):
        """Create fort location sprite."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Main structure
        pygame.draw.rect(surface, COLORS['brown'], (5, 10, 30, 20))
        
        # Roof
        roof_points = [(5, 10), (35, 10), (30, 5), (10, 5)]
        pygame.draw.polygon(surface, COLORS['red'], roof_points)
        
        # Flag
        pygame.draw.line(surface, COLORS['brown'], (32, 5), (32, 2), 1)
        pygame.draw.polygon(surface, COLORS['light_red'], [(32, 2), (35, 4), (32, 3)])
        
        # Windows
        pygame.draw.rect(surface, COLORS['yellow'], (10, 14, 4, 4))
        pygame.draw.rect(surface, COLORS['yellow'], (22, 14, 4, 4))
        
        return surface
    
    @staticmethod
    def create_landmark_sprite(size=40):
        """Create landmark/rock formation sprite."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Large rock formation
        rock_points = [
            (10, 30), (15, 10), (25, 8), (32, 15), (30, 30)
        ]
        pygame.draw.polygon(surface, COLORS['gray'], rock_points)
        
        # Shading
        pygame.draw.line(surface, COLORS['white'], (15, 10), (25, 8), 1)
        
        return surface
    
    @staticmethod
    def create_town_sprite(size=40):
        """Create town location sprite."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Multiple buildings
        # Building 1
        pygame.draw.rect(surface, COLORS['brown'], (5, 15, 12, 20))
        pygame.draw.polygon(surface, COLORS['red'], [(5, 15), (11, 8), (17, 15)])
        
        # Building 2
        pygame.draw.rect(surface, COLORS['brown'], (23, 18, 12, 17))
        pygame.draw.polygon(surface, COLORS['red'], [(23, 18), (29, 12), (35, 18)])
        
        # Windows
        pygame.draw.rect(surface, COLORS['yellow'], (8, 20, 3, 3))
        pygame.draw.rect(surface, COLORS['yellow'], (26, 23, 3, 3))
        
        return surface
    
    @staticmethod
    def create_grave_sprite(size=20):
        """Create grave/death marker sprite."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Gravestone
        pygame.draw.polygon(surface, COLORS['gray'], 
                          [(size // 2, 2), (size - 2, size - 2), (2, size - 2)])
        
        # Cross
        pygame.draw.line(surface, COLORS['white'], 
                        (size // 2, 5), (size // 2, size - 5), 1)
        pygame.draw.line(surface, COLORS['white'], 
                        (size // 2 - 3, 10), (size // 2 + 3, 10), 1)
        
        return surface


class LocationMap:
    """Maps terrain types to graphics for each location."""
    
    LOCATION_TERRAIN = {
        'Missouri River': 'grass',
        'Kansas River Crossing': 'river',
        'Big Blue River': 'river',
        'Fort Laramie': 'fort',
        'Independence Rock': 'landmark',
        'Fort Bridger': 'fort',
        'South Pass': 'mountain',
        'Fort Hall': 'fort',
        'Snake River Crossing': 'river',
        'Blue Mountains': 'mountain',
        'Oregon City': 'town',
    }
    
    @staticmethod
    def get_terrain_for_location(location_name):
        """Get terrain type for a location."""
        return LocationMap.LOCATION_TERRAIN.get(location_name, 'grass')


class TerrainLibrary:
    """Library of all terrain and location graphics."""
    
    def __init__(self):
        """Initialize terrain library."""
        self.terrain_tiles = {}
        self.location_sprites = {}
        self._load_terrain()
        self._load_locations()
    
    def _load_terrain(self):
        """Load terrain tiles."""
        size = TILE_SIZE
        self.terrain_tiles['grass'] = TerrainTileGenerator.create_grass_tile(size)
        self.terrain_tiles['dirt'] = TerrainTileGenerator.create_dirt_tile(size)
        self.terrain_tiles['mountain'] = TerrainTileGenerator.create_mountain_tile(size)
        self.terrain_tiles['water'] = TerrainTileGenerator.create_water_tile(size)
        self.terrain_tiles['forest'] = TerrainTileGenerator.create_forest_tile(size)
        self.terrain_tiles['snow'] = TerrainTileGenerator.create_snow_tile(size)
        self.terrain_tiles['river'] = TerrainTileGenerator.create_river_tile(size)
    
    def _load_locations(self):
        """Load location graphics."""
        self.location_sprites['fort'] = LocationGraphics.create_fort_sprite(40)
        self.location_sprites['landmark'] = LocationGraphics.create_landmark_sprite(40)
        self.location_sprites['town'] = LocationGraphics.create_town_sprite(40)
        self.location_sprites['grave'] = LocationGraphics.create_grave_sprite(20)
    
    def get_terrain_tile(self, terrain_name):
        """Get terrain tile."""
        return self.terrain_tiles.get(terrain_name, self.terrain_tiles['grass'])
    
    def get_location_sprite(self, location_type):
        """Get location sprite."""
        return self.location_sprites.get(location_type)
    
    def get_terrain_for_location(self, location_name):
        """Get appropriate terrain for a location."""
        terrain_type = LocationMap.get_terrain_for_location(location_name)
        return self.get_terrain_tile(terrain_type)
    
    def list_terrain(self):
        """List available terrain types."""
        return list(self.terrain_tiles.keys())
    
    def list_locations(self):
        """List available location types."""
        return list(self.location_sprites.keys())


# Global terrain library
default_terrain_library = TerrainLibrary()
