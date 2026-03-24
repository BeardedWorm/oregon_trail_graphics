"""
Event animations and visual sequences for game events
"""

import pygame
import random
from enum import Enum
from typing import Callable, Optional
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from graphics.animation import TransitionAnimation, MovementAnimation
from graphics.weather import WeatherSystem, WeatherType, LightningEffect


class EventType(Enum):
    """Types of game events."""
    RIVER_CROSSING = "river_crossing"
    SNAKE_BITE = "snake_bite"
    BROKEN_AXLE = "broken_axle"
    ILLNESS = "illness"
    OXEN_DEATH = "oxen_death"
    THEFT = "theft"
    DUST_STORM = "dust_storm"
    STAMPEDE = "stampede"
    INJURY = "injury"
    STARVATION = "starvation"


class EventAnimation:
    """Base event animation."""
    
    def __init__(self, event_type: EventType, duration: float = 3.0):
        """Initialize event animation.
        
        Args:
            event_type: Type of event
            duration: Animation duration in seconds
        """
        self.event_type = event_type
        self.duration = duration
        self.elapsed = 0.0
        self.is_complete = False
        self.on_complete = None
    
    def update(self, delta_time: float):
        """Update animation.
        
        Args:
            delta_time: Time since last frame
        """
        self.elapsed += delta_time
        if self.elapsed >= self.duration:
            self.is_complete = True
            if self.on_complete:
                self.on_complete()
    
    def draw(self, surface: pygame.Surface):
        """Draw animation.
        
        Args:
            surface: Surface to draw on
        """
        pass


class RiverCrossingAnimation(EventAnimation):
    """River crossing animation."""
    
    def __init__(self):
        """Initialize river crossing animation."""
        super().__init__(EventType.RIVER_CROSSING, duration=4.0)
        self.wagon_x = 0
        self.wagon_y = WINDOW_HEIGHT // 2
        self.wave_offset = 0.0
    
    def update(self, delta_time: float):
        """Update animation."""
        super().update(delta_time)
        self.wagon_x = (self.elapsed / self.duration) * WINDOW_WIDTH
        self.wave_offset += delta_time * 5
    
    def draw(self, surface: pygame.Surface):
        """Draw animation."""
        # Draw river
        pygame.draw.rect(surface, COLORS['blue'], 
                        (0, WINDOW_HEIGHT // 2 - 30, WINDOW_WIDTH, 60))
        
        # Draw waves
        for x in range(0, WINDOW_WIDTH, 40):
            wave_x = x + self.wave_offset % 40
            pygame.draw.circle(surface, COLORS['light_blue'], 
                             (int(wave_x), int(WINDOW_HEIGHT // 2)), 5)
        
        # Draw wagon
        pygame.draw.rect(surface, COLORS['brown'], 
                        (int(self.wagon_x), int(self.wagon_y), 40, 30))
        pygame.draw.circle(surface, COLORS['black'], 
                          (int(self.wagon_x + 10), int(self.wagon_y + 30)), 5)
        pygame.draw.circle(surface, COLORS['black'],
                          (int(self.wagon_x + 30), int(self.wagon_y + 30)), 5)
        
        # Draw text
        progress = self.elapsed / self.duration
        if progress < 0.5:
            text = "Crossing river..."
        else:
            text = "River crossed!"
        # Would render text with font


class SnakeBiteAnimation(EventAnimation):
    """Snake bite event animation."""
    
    def __init__(self):
        """Initialize snake bite animation."""
        super().__init__(EventType.SNAKE_BITE, duration=2.5)
        self.shake_intensity = 0.0
        self.pulse = 0.0
    
    def update(self, delta_time: float):
        """Update animation."""
        super().update(delta_time)
        self.shake_intensity = abs((self.elapsed / self.duration) - 0.5) * 20
        self.pulse += delta_time * 10
    
    def draw(self, surface: pygame.Surface):
        """Draw animation."""
        # Screen shake effect
        shake_x = random.randint(int(-self.shake_intensity), int(self.shake_intensity))
        shake_y = random.randint(int(-self.shake_intensity), int(self.shake_intensity))
        
        # Draw tent with character inside
        tent_x = WINDOW_WIDTH // 2 - 40 + shake_x
        tent_y = WINDOW_HEIGHT // 2 - 30 + shake_y
        
        pygame.draw.polygon(surface, COLORS['light_white'],
                          [(tent_x, tent_y), (tent_x + 80, tent_y),
                           (tent_x + 40, tent_y - 30)])
        
        # Draw pulsing wound indicator
        intensity = (1 + (self.pulse % 2) - 1) / 2
        pygame.draw.circle(surface, COLORS['red'],
                          (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
                          int(30 * intensity))


class BrokenAxleAnimation(EventAnimation):
    """Broken axle event animation."""
    
    def __init__(self):
        """Initialize broken axle animation."""
        super().__init__(EventType.BROKEN_AXLE, duration=3.0)
        self.rotation = 0.0
    
    def update(self, delta_time: float):
        """Update animation."""
        super().update(delta_time)
        self.rotation += delta_time * 180
    
    def draw(self, surface: pygame.Surface):
        """Draw animation."""
        # Draw wagon tilted
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2
        
        # Draw wheel spinning
        pygame.draw.circle(surface, COLORS['brown'], (cx - 40, cy + 40), 20)
        pygame.draw.circle(surface, COLORS['gray'], (cx - 40, cy + 40), 18, 2)
        
        # Draw radii showing rotation
        angle = (self.rotation % 360) * 3.14159 / 180
        for i in range(4):
            a = angle + i * 3.14159 / 2
            x1 = cx - 40 + 18 * (a**0.5 - 1)
            y1 = cy + 40 + 18 * (a - 1.57)
            pygame.draw.line(surface, COLORS['gray'], (cx - 40, cy + 40),
                           (x1, y1), 1)


class StampedAnimation(EventAnimation):
    """Stampede event animation."""
    
    def __init__(self):
        """Initialize stampede animation."""
        super().__init__(EventType.STAMPEDE, duration=3.0)
        self.animals = [(random.randint(0, WINDOW_WIDTH), 100 + i * 30)
                       for i in range(3)]
    
    def update(self, delta_time: float):
        """Update animation."""
        super().update(delta_time)
        progress = self.elapsed / self.duration
        self.animals = [(x + progress * WINDOW_WIDTH * 2, y)
                       for x, y in [(x - progress * WINDOW_WIDTH * 2, y)
                                    for x, y in self.animals]]
    
    def draw(self, surface: pygame.Surface):
        """Draw animation."""
        # Draw stampeding buffalo
        for x, y in self.animals:
            pygame.draw.ellipse(surface, COLORS['brown'],
                              (int(x), int(y), 30, 20))


class IllnessAnimation(EventAnimation):
    """Illness event animation."""
    
    def __init__(self, illness_name: str = "Dysentery"):
        """Initialize illness animation.
        
        Args:
            illness_name: Name of illness
        """
        super().__init__(EventType.ILLNESS, duration=2.0)
        self.illness_name = illness_name
        self.pulse = 0.0
    
    def update(self, delta_time: float):
        """Update animation."""
        super().update(delta_time)
        self.pulse += delta_time * 5
    
    def draw(self, surface: pygame.Surface):
        """Draw animation."""
        # Draw character with illness indicator
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2
        
        # Draw character
        pygame.draw.circle(surface, COLORS['light_white'], (cx, cy - 20), 10)
        pygame.draw.rect(surface, COLORS['brown'], (cx - 8, cy - 10, 16, 20))
        pygame.draw.circle(surface, COLORS['brown'], (cx - 12, cy), 5)
        pygame.draw.circle(surface, COLORS['brown'], (cx + 12, cy), 5)
        
        # Draw pulsing illness indicator
        intensity = abs(1.0 + (self.pulse % 2) - 1) / 2
        pygame.draw.circle(surface, COLORS['green'],
                          (cx, cy - 30), int(15 * intensity))


class DustStormAnimation(EventAnimation):
    """Dust storm event animation."""
    
    def __init__(self):
        """Initialize dust storm animation."""
        super().__init__(EventType.DUST_STORM, duration=3.0)
        self.weather_system = WeatherSystem(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.weather_system.set_weather(WeatherType.DUST_STORM, intensity=1.0)
    
    def update(self, delta_time: float):
        """Update animation."""
        super().update(delta_time)
        self.weather_system.update(delta_time)
    
    def draw(self, surface: pygame.Surface):
        """Draw animation."""
        # Draw dark overlay
        overlay_alpha = int(200 * (self.elapsed / self.duration))
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(overlay_alpha)
        overlay.fill(COLORS['brown'])
        surface.blit(overlay, (0, 0))
        
        # Draw weather effects
        self.weather_system.draw(surface)


class EventAnimationSequence:
    """Sequence of event animations."""
    
    def __init__(self):
        """Initialize event animation sequence."""
        self.current_animation = None
        self.queue = []
        self.is_active = False
    
    def create_animation(self, event_type: EventType) -> EventAnimation:
        """Create animation for event type.
        
        Args:
            event_type: Type of event
            
        Returns:
            EventAnimation instance
        """
        animation_map = {
            EventType.RIVER_CROSSING: RiverCrossingAnimation,
            EventType.SNAKE_BITE: SnakeBiteAnimation,
            EventType.BROKEN_AXLE: BrokenAxleAnimation,
            EventType.STAMPEDE: StampedAnimation,
            EventType.ILLNESS: IllnessAnimation,
            EventType.DUST_STORM: DustStormAnimation,
        }
        
        animation_class = animation_map.get(event_type, EventAnimation)
        if event_type == EventType.ILLNESS:
            return animation_class("Unknown Illness")
        return animation_class()
    
    def enqueue_event(self, event_type: EventType):
        """Add event to queue.
        
        Args:
            event_type: Type of event
        """
        animation = self.create_animation(event_type)
        self.queue.append(animation)
        
        if not self.is_active and self.current_animation is None:
            self._start_next_animation()
    
    def _start_next_animation(self):
        """Start next animation in queue."""
        if self.queue:
            self.current_animation = self.queue.pop(0)
            self.current_animation.on_complete = self._on_animation_complete
            self.is_active = True
        else:
            self.is_active = False
    
    def _on_animation_complete(self):
        """Handle animation completion."""
        self._start_next_animation()
    
    def update(self, delta_time: float):
        """Update sequence.
        
        Args:
            delta_time: Time since last frame
        """
        if self.current_animation and self.is_active:
            self.current_animation.update(delta_time)
            if self.current_animation.is_complete:
                self._start_next_animation()
    
    def draw(self, surface: pygame.Surface):
        """Draw sequence.
        
        Args:
            surface: Surface to draw on
        """
        if self.current_animation and self.is_active:
            self.current_animation.draw(surface)
    
    def is_playing(self) -> bool:
        """Check if sequence is playing.
        
        Returns:
            True if playing
        """
        return self.is_active or bool(self.queue)
