"""
Performance optimization - sprite batching, caching, and efficient rendering
"""

import pygame
from typing import Dict, List, Tuple, Optional
from config import WINDOW_WIDTH, WINDOW_HEIGHT


class SpriteCache:
    """Caches frequently used sprites to avoid regeneration."""
    
    def __init__(self):
        """Initialize sprite cache."""
        self.cache = {}
        self.max_cache_size = 100
    
    def get(self, key: str) -> Optional[pygame.Surface]:
        """Get cached sprite.
        
        Args:
            key: Cache key
            
        Returns:
            Cached surface or None
        """
        return self.cache.get(key)
    
    def put(self, key: str, surface: pygame.Surface):
        """Cache sprite.
        
        Args:
            key: Cache key
            surface: Surface to cache
        """
        if len(self.cache) >= self.max_cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[key] = surface
    
    def clear(self):
        """Clear cache."""
        self.cache.clear()
    
    def get_stats(self) -> dict:
        """Get cache statistics.
        
        Returns:
            Dictionary with stats
        """
        return {
            'size': len(self.cache),
            'max_size': self.max_cache_size,
        }


class RenderBatch:
    """Groups sprites for batch rendering."""
    
    def __init__(self, surface: pygame.Surface):
        """Initialize render batch.
        
        Args:
            surface: Target surface
        """
        self.surface = surface
        self.sprites = []
        self.dirty_rects = []
    
    def add_sprite(self, sprite: pygame.Surface, rect: pygame.Rect):
        """Add sprite to batch.
        
        Args:
            sprite: Sprite surface
            rect: Destination rect
        """
        self.sprites.append((sprite, rect))
        self.dirty_rects.append(rect)
    
    def render(self):
        """Render all batched sprites."""
        for sprite, rect in self.sprites:
            self.surface.blit(sprite, rect)
        self.sprites.clear()
    
    def update_dirty_rects(self) -> List[pygame.Rect]:
        """Get dirty rects for update.
        
        Returns:
            List of rectangles that changed
        """
        rects = self.dirty_rects
        self.dirty_rects = []
        return rects


class OptimizedRenderer:
    """Renderer with optimization techniques."""
    
    def __init__(self, surface: pygame.Surface):
        """Initialize optimized renderer.
        
        Args:
            surface: Render target surface
        """
        self.surface = surface
        self.sprite_cache = SpriteCache()
        self.batch = RenderBatch(surface)
        self.frame_count = 0
        self.fps = 0
        self.last_frame_time = 0
    
    def start_batch(self):
        """Start sprite batching."""
        self.batch = RenderBatch(self.surface)
    
    def add_to_batch(self, sprite: pygame.Surface, rect: pygame.Rect):
        """Add sprite to batch.
        
        Args:
            sprite: Sprite surface
            rect: Destination rect
        """
        self.batch.add_sprite(sprite, rect)
    
    def render_batch(self):
        """Render all batched sprites."""
        self.batch.render()
    
    def get_cached_sprite(self, key: str) -> Optional[pygame.Surface]:
        """Get sprite from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached surface or None
        """
        return self.sprite_cache.get(key)
    
    def cache_sprite(self, key: str, surface: pygame.Surface):
        """Cache sprite for reuse.
        
        Args:
            key: Cache key
            surface: Surface to cache
        """
        self.sprite_cache.put(key, surface)
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics.
        
        Returns:
            Cache stats
        """
        return self.sprite_cache.get_stats()


class DirtySpriteGroup(pygame.sprite.Group):
    """Sprite group with dirty rect optimization."""
    
    def __init__(self):
        """Initialize dirty sprite group."""
        super().__init__()
        self.dirty_rects = []
        self.use_dirty_rects = True
    
    def draw(self, surface: pygame.Surface) -> List[pygame.Rect]:
        """Draw sprites with dirty rect optimization.
        
        Args:
            surface: Target surface
            
        Returns:
            List of updated rectangles
        """
        if not self.use_dirty_rects:
            return super().draw(surface)
        
        updated_rects = []
        for sprite in self.sprites():
            updated_rects.append(surface.blit(sprite.image, sprite.rect))
        
        return updated_rects
    
    def clear(self, surface: pygame.Surface, clear_callback):
        """Clear sprites efficiently.
        
        Args:
            surface: Target surface
            clear_callback: Callback to clear areas
        """
        for rect in self.dirty_rects:
            clear_callback(surface, rect)
        self.dirty_rects = []


class AnimationOptimizer:
    """Optimizes animation rendering."""
    
    def __init__(self):
        """Initialize animation optimizer."""
        self.frame_cache = {}
        self.skipped_frames = 0
        self.total_frames = 0
    
    def should_skip_frame(self, fps: int, target_fps: int = 60) -> bool:
        """Determine if frame should be skipped.
        
        Args:
            fps: Current FPS
            target_fps: Target FPS
            
        Returns:
            True if frame should be skipped
        """
        self.total_frames += 1
        if fps < target_fps * 0.8:
            self.skipped_frames += 1
            return True
        return False
    
    def cache_animation_frame(self, anim_id: str, frame: int, surface: pygame.Surface):
        """Cache animation frame.
        
        Args:
            anim_id: Animation ID
            frame: Frame number
            surface: Frame surface
        """
        key = f"{anim_id}_{frame}"
        self.frame_cache[key] = surface
    
    def get_cached_frame(self, anim_id: str, frame: int) -> Optional[pygame.Surface]:
        """Get cached animation frame.
        
        Args:
            anim_id: Animation ID
            frame: Frame number
            
        Returns:
            Cached frame or None
        """
        key = f"{anim_id}_{frame}"
        return self.frame_cache.get(key)


class MemoryOptimizer:
    """Manages memory usage."""
    
    def __init__(self):
        """Initialize memory optimizer."""
        self.allocation_tracking = {}
    
    def track_allocation(self, name: str, size_bytes: int):
        """Track memory allocation.
        
        Args:
            name: Allocation name
            size_bytes: Size in bytes
        """
        self.allocation_tracking[name] = size_bytes
    
    def get_total_memory(self) -> int:
        """Get total tracked memory.
        
        Returns:
            Total bytes
        """
        return sum(self.allocation_tracking.values())
    
    def get_memory_summary(self) -> Dict[str, int]:
        """Get memory summary.
        
        Returns:
            Dictionary of allocations
        """
        return self.allocation_tracking.copy()
    
    def cleanup(self, threshold_mb: int = 100):
        """Cleanup if memory exceeds threshold.
        
        Args:
            threshold_mb: Cleanup threshold in MB
        """
        total_mb = self.get_total_memory() / (1024 * 1024)
        if total_mb > threshold_mb:
            self.allocation_tracking.clear()


class RenderOptimizations:
    """Collection of rendering optimizations."""
    
    @staticmethod
    def surface_from_cache_or_create(cache: SpriteCache, key: str, 
                                    create_func) -> pygame.Surface:
        """Get surface from cache or create new.
        
        Args:
            cache: Sprite cache
            key: Cache key
            create_func: Function to create surface if not cached
            
        Returns:
            Surface
        """
        cached = cache.get(key)
        if cached:
            return cached
        
        surface = create_func()
        cache.put(key, surface)
        return surface
    
    @staticmethod
    def scale_surface_cached(cache: SpriteCache, surface: pygame.Surface,
                           width: int, height: int) -> pygame.Surface:
        """Scale surface with caching.
        
        Args:
            cache: Sprite cache
            surface: Source surface
            width: Target width
            height: Target height
            
        Returns:
            Scaled surface
        """
        key = f"scale_{id(surface)}_{width}_{height}"
        cached = cache.get(key)
        if cached:
            return cached
        
        scaled = pygame.transform.scale(surface, (width, height))
        cache.put(key, scaled)
        return scaled
    
    @staticmethod
    def blend_surfaces(surf1: pygame.Surface, surf2: pygame.Surface,
                      alpha: int) -> pygame.Surface:
        """Blend two surfaces.
        
        Args:
            surf1: First surface
            surf2: Second surface
            alpha: Blend alpha (0-255)
            
        Returns:
            Blended surface
        """
        result = surf1.copy()
        surf2.set_alpha(alpha)
        result.blit(surf2, (0, 0))
        return result


class RenderStatistics:
    """Tracks rendering statistics."""
    
    def __init__(self):
        """Initialize render statistics."""
        self.frame_times = []
        self.max_frame_time = 0
        self.min_frame_time = float('inf')
        self.total_frames = 0
        self.total_sprites_rendered = 0
        self.cache_hits = 0
        self.cache_misses = 0
    
    def record_frame_time(self, delta_time: float, sprite_count: int):
        """Record frame time.
        
        Args:
            delta_time: Frame time in seconds
            sprite_count: Number of sprites rendered
        """
        ms = delta_time * 1000
        self.frame_times.append(ms)
        self.max_frame_time = max(self.max_frame_time, ms)
        self.min_frame_time = min(self.min_frame_time, ms)
        self.total_frames += 1
        self.total_sprites_rendered += sprite_count
    
    def get_average_frame_time(self) -> float:
        """Get average frame time.
        
        Returns:
            Average time in ms
        """
        if not self.frame_times:
            return 0
        return sum(self.frame_times) / len(self.frame_times)
    
    def get_fps(self) -> float:
        """Get average FPS.
        
        Returns:
            Frames per second
        """
        avg_time = self.get_average_frame_time()
        if avg_time == 0:
            return 60
        return 1000 / avg_time
    
    def get_summary(self) -> dict:
        """Get statistics summary.
        
        Returns:
            Dictionary with stats
        """
        return {
            'total_frames': self.total_frames,
            'avg_frame_time': self.get_average_frame_time(),
            'min_frame_time': self.min_frame_time,
            'max_frame_time': self.max_frame_time,
            'fps': self.get_fps(),
            'total_sprites_rendered': self.total_sprites_rendered,
            'cache_hit_rate': (self.cache_hits / (self.cache_hits + self.cache_misses) * 100)
                             if (self.cache_hits + self.cache_misses) > 0 else 0,
        }
