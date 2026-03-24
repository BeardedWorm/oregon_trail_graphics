"""
Weather effects and particle systems
"""

import pygame
import random
from config import COLORS
from enum import Enum
from typing import List, Tuple


class WeatherType(Enum):
    """Weather conditions."""
    CLEAR = "clear"
    RAIN = "rain"
    SNOW = "snow"
    DUST_STORM = "dust_storm"
    FOG = "fog"
    HAIL = "hail"


class Particle(pygame.sprite.Sprite):
    """Single particle for effects."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 size: int, color: Tuple[int, int, int], lifetime: float):
        """Initialize particle.
        
        Args:
            x: Starting X position
            y: Starting Y position
            vx: Velocity X
            vy: Velocity Y
            size: Particle size
            color: RGB color
            lifetime: Lifetime in seconds
        """
        super().__init__()
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self._draw_particle()
    
    def _draw_particle(self):
        """Draw particle."""
        pygame.draw.circle(self.image, self.color, (self.size // 2, self.size // 2), 
                          max(1, self.size // 2))
    
    def update(self, delta_time: float):
        """Update particle.
        
        Args:
            delta_time: Time since last frame
        """
        self.age += delta_time
        
        # Update position
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        
        # Update alpha based on lifetime
        alpha = int(255 * (1.0 - self.age / self.lifetime))
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (*self.color, alpha), 
                          (self.size // 2, self.size // 2), max(1, self.size // 2))
        
        self.rect.topleft = (int(self.x), int(self.y))
    
    def is_alive(self) -> bool:
        """Check if particle is alive."""
        return self.age < self.lifetime


class ParticleEmitter:
    """Emits particles for effects."""
    
    def __init__(self, x: float, y: float, width: int, height: int):
        """Initialize emitter.
        
        Args:
            x: Emitter X position
            y: Emitter Y position
            width: Emitter width
            height: Emitter height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.particles = pygame.sprite.Group()
        self.emission_rate = 0
        self.is_active = True
    
    def emit(self, count: int, vx: float, vy: float, vx_spread: float, vy_spread: float,
            size: int, color: Tuple[int, int, int], lifetime: float):
        """Emit particles.
        
        Args:
            count: Number of particles
            vx: Base velocity X
            vy: Base velocity Y
            vx_spread: Velocity X randomness
            vy_spread: Velocity Y randomness
            size: Particle size
            color: RGB color
            lifetime: Particle lifetime
        """
        for _ in range(count):
            x = self.x + random.uniform(0, self.width)
            y = self.y + random.uniform(0, self.height)
            vx_actual = vx + random.uniform(-vx_spread, vx_spread)
            vy_actual = vy + random.uniform(-vy_spread, vy_spread)
            
            particle = Particle(x, y, vx_actual, vy_actual, size, color, lifetime)
            self.particles.add(particle)
    
    def update(self, delta_time: float):
        """Update emitter.
        
        Args:
            delta_time: Time since last frame
        """
        self.particles.update(delta_time)
        
        # Remove dead particles
        for particle in list(self.particles):
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def draw(self, surface: pygame.Surface):
        """Draw particles.
        
        Args:
            surface: Surface to draw on
        """
        self.particles.draw(surface)
    
    def stop(self):
        """Stop emission."""
        self.is_active = False
    
    def clear(self):
        """Clear all particles."""
        self.particles.empty()


class WeatherEffect:
    """Base weather effect."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize weather effect.
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.emitter = ParticleEmitter(0, 0, screen_width, screen_height)
        self.intensity = 1.0
        self.time = 0.0
    
    def update(self, delta_time: float):
        """Update weather effect.
        
        Args:
            delta_time: Time since last frame
        """
        self.time += delta_time
        self.emitter.update(delta_time)
    
    def draw(self, surface: pygame.Surface):
        """Draw weather effect.
        
        Args:
            surface: Surface to draw on
        """
        self.emitter.draw(surface)
    
    def set_intensity(self, intensity: float):
        """Set effect intensity.
        
        Args:
            intensity: Intensity 0-1
        """
        self.intensity = max(0.0, min(1.0, intensity))


class RainEffect(WeatherEffect):
    """Rain weather effect."""
    
    def update(self, delta_time: float):
        """Update rain effect.
        
        Args:
            delta_time: Time since last frame
        """
        super().update(delta_time)
        
        # Emit raindrops
        emission_count = int(50 * self.intensity)
        self.emitter.emit(emission_count, 0, 300, 20, 50, 2, COLORS['cyan'], 0.5)


class SnowEffect(WeatherEffect):
    """Snow weather effect."""
    
    def update(self, delta_time: float):
        """Update snow effect.
        
        Args:
            delta_time: Time since last frame
        """
        super().update(delta_time)
        
        # Emit snowflakes
        emission_count = int(30 * self.intensity)
        self.emitter.emit(emission_count, random.uniform(-50, 50), 100, 
                         20, 20, 3, COLORS['light_white'], 2.0)


class DustStormEffect(WeatherEffect):
    """Dust storm weather effect."""
    
    def update(self, delta_time: float):
        """Update dust storm effect.
        
        Args:
            delta_time: Time since last frame
        """
        super().update(delta_time)
        
        # Emit dust particles
        emission_count = int(80 * self.intensity)
        self.emitter.emit(emission_count, random.uniform(100, 300), 
                         random.uniform(-50, 50), 50, 50, 4, COLORS['brown'], 1.5)


class FogEffect(WeatherEffect):
    """Fog weather effect."""
    
    def draw(self, surface: pygame.Surface):
        """Draw fog effect.
        
        Args:
            surface: Surface to draw on
        """
        # Create fog overlay
        fog_surface = pygame.Surface((self.screen_width, self.screen_height))
        fog_color = COLORS['gray']
        alpha = int(100 * self.intensity)
        fog_surface.set_alpha(alpha)
        fog_surface.fill(fog_color)
        surface.blit(fog_surface, (0, 0))


class HailEffect(WeatherEffect):
    """Hail weather effect."""
    
    def update(self, delta_time: float):
        """Update hail effect.
        
        Args:
            delta_time: Time since last frame
        """
        super().update(delta_time)
        
        # Emit hailstones
        emission_count = int(60 * self.intensity)
        self.emitter.emit(emission_count, 0, 400, 30, 50, 4, COLORS['white'], 0.3)


class WeatherSystem:
    """Manages all weather effects."""
    
    WEATHER_EFFECTS = {
        WeatherType.CLEAR: None,
        WeatherType.RAIN: RainEffect,
        WeatherType.SNOW: SnowEffect,
        WeatherType.DUST_STORM: DustStormEffect,
        WeatherType.FOG: FogEffect,
        WeatherType.HAIL: HailEffect,
    }
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize weather system.
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_weather = WeatherType.CLEAR
        self.current_effect = None
        self.transition_time = 0.0
        self.transition_duration = 1.0
        self.target_weather = WeatherType.CLEAR
    
    def set_weather(self, weather_type: WeatherType, intensity: float = 1.0, 
                   transition_duration: float = 1.0):
        """Set weather condition.
        
        Args:
            weather_type: Type of weather
            intensity: Effect intensity 0-1
            transition_duration: Duration to transition
        """
        if weather_type != self.current_weather:
            self.target_weather = weather_type
            self.transition_duration = transition_duration
            self.transition_time = 0.0
        
        if self.current_effect:
            self.current_effect.set_intensity(intensity)
    
    def update(self, delta_time: float):
        """Update weather system.
        
        Args:
            delta_time: Time since last frame
        """
        # Handle weather transition
        if self.current_weather != self.target_weather:
            self.transition_time += delta_time
            
            if self.transition_time >= self.transition_duration:
                self.current_weather = self.target_weather
                self.transition_time = 0.0
                
                # Create new effect
                effect_class = self.WEATHER_EFFECTS[self.current_weather]
                self.current_effect = effect_class(self.screen_width, 
                                                   self.screen_height) if effect_class else None
        
        # Update current effect
        if self.current_effect:
            self.current_effect.update(delta_time)
    
    def draw(self, surface: pygame.Surface):
        """Draw weather effects.
        
        Args:
            surface: Surface to draw on
        """
        if self.current_effect:
            self.current_effect.draw(surface)
    
    def get_current_weather(self) -> WeatherType:
        """Get current weather type.
        
        Returns:
            Current weather type
        """
        return self.current_weather


class LightningEffect:
    """Lightning flash effect."""
    
    def __init__(self, screen_width: int, screen_height: int, intensity: float = 1.0):
        """Initialize lightning effect.
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
            intensity: Flash intensity
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.intensity = intensity
        self.flash_time = 0.0
        self.is_flashing = False
    
    def trigger(self, duration: float = 0.1):
        """Trigger lightning flash.
        
        Args:
            duration: Flash duration
        """
        self.flash_time = duration
        self.is_flashing = True
    
    def update(self, delta_time: float):
        """Update lightning effect.
        
        Args:
            delta_time: Time since last frame
        """
        if self.is_flashing:
            self.flash_time -= delta_time
            if self.flash_time <= 0:
                self.is_flashing = False
    
    def draw(self, surface: pygame.Surface):
        """Draw lightning effect.
        
        Args:
            surface: Surface to draw on
        """
        if self.is_flashing:
            flash_surface = pygame.Surface((self.screen_width, self.screen_height))
            flash_alpha = int(200 * (self.flash_time / 0.1))
            flash_surface.set_alpha(flash_alpha)
            flash_surface.fill(COLORS['white'])
            surface.blit(flash_surface, (0, 0))
