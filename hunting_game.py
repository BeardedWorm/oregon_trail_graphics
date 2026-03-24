"""
Visual hunting mini-game with animated sequences
"""

import pygame
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, TILE_SIZE
from graphics.animation import Animation, AnimationController, Keyframe, AnimatedSprite
from graphics.character_sprites import SpriteGenerator


class HuntingTarget:
    """Huntable animal target."""
    
    def __init__(self, x: float, y: float, animal_type: str = 'deer'):
        """Initialize hunting target.
        
        Args:
            x: Starting X position
            y: Starting Y position
            animal_type: Type of animal ('deer', 'buffalo', 'rabbit')
        """
        self.x = x
        self.y = y
        self.animal_type = animal_type
        self.vx = random.uniform(-50, 50)
        self.vy = random.uniform(-30, 30)
        self.health = 100
        self.is_alive = True
        
        # Animal properties
        self.animal_properties = {
            'deer': {'size': 30, 'speed': 150, 'health': 50, 'meat': 150},
            'buffalo': {'size': 50, 'speed': 100, 'health': 100, 'meat': 400},
            'rabbit': {'size': 15, 'speed': 200, 'health': 20, 'meat': 20},
        }
        
        props = self.animal_properties.get(animal_type, self.animal_properties['deer'])
        self.size = props['size']
        self.speed = props['speed']
        self.max_health = props['health']
        self.meat_amount = props['meat']
        self.health = self.max_health
        
        self.rect = pygame.Rect(x, y, self.size, self.size)
    
    def update(self, delta_time: float):
        """Update target position.
        
        Args:
            delta_time: Time since last frame
        """
        if not self.is_alive:
            return
        
        # Random movement
        self.vx += random.uniform(-20, 20) * delta_time
        self.vy += random.uniform(-20, 20) * delta_time
        
        # Limit speed
        max_speed = self.speed
        speed = (self.vx**2 + self.vy**2)**0.5
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed
        
        # Update position
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        
        # Boundary collision
        margin = 50
        if self.x < margin:
            self.x = margin
            self.vx = abs(self.vx)
        elif self.x > WINDOW_WIDTH - self.size - margin:
            self.x = WINDOW_WIDTH - self.size - margin
            self.vx = -abs(self.vx)
        
        if self.y < margin:
            self.y = margin
            self.vy = abs(self.vy)
        elif self.y > WINDOW_HEIGHT - self.size - margin:
            self.y = WINDOW_HEIGHT - self.size - margin
            self.vy = -abs(self.vy)
        
        self.rect.topleft = (int(self.x), int(self.y))
    
    def take_damage(self, damage: int) -> bool:
        """Damage the target.
        
        Args:
            damage: Damage amount
            
        Returns:
            True if target died
        """
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            return True
        return False
    
    def draw(self, surface: pygame.Surface):
        """Draw target.
        
        Args:
            surface: Surface to draw on
        """
        if not self.is_alive:
            return
        
        # Draw animal body
        color = COLORS['brown'] if self.animal_type in ['deer', 'buffalo'] else COLORS['yellow']
        pygame.draw.rect(surface, color, self.rect)
        
        # Draw health bar
        health_bar_width = self.size
        health_bar_height = 4
        health_percent = self.health / self.max_health
        filled_width = int(health_bar_width * health_percent)
        
        pygame.draw.rect(surface, COLORS['red'], 
                        (self.rect.x, self.rect.y - 8, health_bar_width, health_bar_height))
        pygame.draw.rect(surface, COLORS['green'],
                        (self.rect.x, self.rect.y - 8, filled_width, health_bar_height))
        
        # Draw health percentage
        health_text = f"{int(self.health)}/{self.max_health}"
        # Would need font to render, so just draw outline
        pygame.draw.rect(surface, COLORS['white'], self.rect, 1)


class Projectile:
    """Bullet/arrow projectile."""
    
    def __init__(self, x: float, y: float, target_x: float, target_y: float, 
                 speed: float = 300, damage: int = 20):
        """Initialize projectile.
        
        Args:
            x: Starting X
            y: Starting Y
            target_x: Target X
            target_y: Target Y
            speed: Projectile speed
            damage: Damage amount
        """
        self.x = x
        self.y = y
        self.damage = damage
        self.size = 4
        
        # Calculate direction
        import math
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.vx = (dx / distance) * speed
            self.vy = (dy / distance) * speed
        else:
            self.vx = 0
            self.vy = 0
        
        self.lifetime = 3.0
        self.age = 0.0
        self.is_alive = True
    
    def update(self, delta_time: float):
        """Update projectile.
        
        Args:
            delta_time: Time since last frame
        """
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        self.age += delta_time
        
        if self.age > self.lifetime:
            self.is_alive = False
        
        # Out of bounds check
        if self.x < 0 or self.x > WINDOW_WIDTH or self.y < 0 or self.y > WINDOW_HEIGHT:
            self.is_alive = False
    
    def draw(self, surface: pygame.Surface):
        """Draw projectile.
        
        Args:
            surface: Surface to draw on
        """
        pygame.draw.circle(surface, COLORS['yellow'], (int(self.x), int(self.y)), 
                          self.size)


class HuntingGame:
    """Visual hunting mini-game."""
    
    def __init__(self, duration: int = 30):
        """Initialize hunting game.
        
        Args:
            duration: Hunting duration in seconds
        """
        self.duration = duration
        self.elapsed_time = 0.0
        self.is_active = True
        self.is_complete = False
        
        # Game objects
        self.targets = []
        self.projectiles = []
        self.player_x = WINDOW_WIDTH // 2
        self.player_y = WINDOW_HEIGHT - 100
        
        # Game stats
        self.shots_fired = 0
        self.shots_hit = 0
        self.animals_killed = 0
        self.total_meat = 0
        
        self._spawn_targets()
    
    def _spawn_targets(self):
        """Spawn animals to hunt."""
        # Spawn 3-5 animals
        for _ in range(random.randint(3, 5)):
            x = random.uniform(100, WINDOW_WIDTH - 100)
            y = random.uniform(100, WINDOW_HEIGHT - 200)
            animal_type = random.choice(['deer', 'deer', 'buffalo', 'rabbit'])
            self.targets.append(HuntingTarget(x, y, animal_type))
    
    def fire_at_target(self, target_index: int):
        """Fire at a target.
        
        Args:
            target_index: Index of target to fire at
        """
        if target_index < 0 or target_index >= len(self.targets):
            return
        
        target = self.targets[target_index]
        self.shots_fired += 1
        
        # Create projectile
        projectile = Projectile(self.player_x, self.player_y, 
                               target.rect.centerx, target.rect.centery,
                               damage=25)
        self.projectiles.append(projectile)
    
    def update(self, delta_time: float):
        """Update hunting game.
        
        Args:
            delta_time: Time since last frame
        """
        if not self.is_active:
            return
        
        self.elapsed_time += delta_time
        
        # Check time limit
        if self.elapsed_time > self.duration:
            self.is_active = False
            self.is_complete = True
        
        # Update targets
        for target in self.targets:
            target.update(delta_time)
        
        # Update projectiles
        for projectile in list(self.projectiles):
            projectile.update(delta_time)
            
            if not projectile.is_alive:
                self.projectiles.remove(projectile)
                continue
            
            # Check collision with targets
            for target in self.targets:
                if not target.is_alive:
                    continue
                
                dist = ((projectile.x - target.rect.centerx)**2 + 
                       (projectile.y - target.rect.centery)**2)**0.5
                
                if dist < target.size / 2:
                    self.shots_hit += 1
                    if target.take_damage(projectile.damage):
                        self.animals_killed += 1
                        self.total_meat += target.meat_amount
                    projectile.is_alive = False
                    break
        
        # Remove dead projectiles
        self.projectiles = [p for p in self.projectiles if p.is_alive]
        
        # Spawn more animals if all are dead
        alive_targets = [t for t in self.targets if t.is_alive]
        if not alive_targets and self.elapsed_time < self.duration * 0.8:
            self._spawn_targets()
    
    def draw(self, surface: pygame.Surface):
        """Draw hunting game.
        
        Args:
            surface: Surface to draw on
        """
        surface.fill(COLORS['black'])
        
        # Draw targets
        for target in self.targets:
            target.draw(surface)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(surface)
        
        # Draw player
        pygame.draw.circle(surface, COLORS['light_green'], 
                          (int(self.player_x), int(self.player_y)), 10)
        
        # Draw HUD
        time_remaining = max(0, self.duration - self.elapsed_time)
        stats_text = [
            f"Time: {time_remaining:.1f}s",
            f"Shots: {self.shots_hit}/{self.shots_fired}",
            f"Animals: {self.animals_killed}",
            f"Meat: {self.total_meat}",
        ]
        
        y = 20
        for text in stats_text:
            # Would need font, so we'll use a placeholder
            y += 20
        
        # Draw instructions
        y = WINDOW_HEIGHT - 40
        # Instructions would go here
    
    def get_results(self) -> dict:
        """Get hunting results.
        
        Returns:
            Dictionary with results
        """
        return {
            'animals_killed': self.animals_killed,
            'total_meat': self.total_meat,
            'shots_fired': self.shots_fired,
            'shots_hit': self.shots_hit,
            'accuracy': (self.shots_hit / self.shots_fired * 100) if self.shots_fired > 0 else 0,
        }


class HuntingSequence:
    """Animated hunting sequence with narration."""
    
    def __init__(self):
        """Initialize hunting sequence."""
        self.game = HuntingGame(duration=30)
        self.selected_target = 0
        self.sequence_state = 'active'  # active, complete, results
    
    def handle_input(self, key: int):
        """Handle input.
        
        Args:
            key: Pygame key code
        """
        import pygame
        
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.selected_target = max(0, self.selected_target - 1)
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            alive_count = len([t for t in self.game.targets if t.is_alive])
            self.selected_target = min(alive_count - 1, self.selected_target + 1)
        elif key == pygame.K_SPACE or key == pygame.K_RETURN:
            self.game.fire_at_target(self.selected_target)
    
    def update(self, delta_time: float):
        """Update sequence.
        
        Args:
            delta_time: Time since last frame
        """
        if self.sequence_state == 'active':
            self.game.update(delta_time)
            if self.game.is_complete:
                self.sequence_state = 'results'
    
    def draw(self, surface: pygame.Surface):
        """Draw sequence.
        
        Args:
            surface: Surface to draw on
        """
        self.game.draw(surface)
