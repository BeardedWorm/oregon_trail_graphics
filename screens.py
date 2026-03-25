"""
Enhanced screen implementations with graphics and mini-games
"""

import pygame
import random
from abc import ABC, abstractmethod
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from hunting_game import HuntingTarget
from event_animations import RiverCrossingAnimation


class Screen(ABC):
    """Base screen class."""
    
    def __init__(self):
        """Initialize screen."""
        self.is_active = True
        self.next_screen = None
    
    @abstractmethod
    def handle_input(self, event):
        """Handle input."""
        pass
    
    @abstractmethod
    def update(self, delta_time: float):
        """Update screen."""
        pass
    
    @abstractmethod
    def draw(self, renderer):
        """Draw screen."""
        pass


class TravelScreen(Screen):
    """Main travel screen with character graphics."""
    
    def __init__(self, game_engine):
        """Initialize travel screen."""
        super().__init__()
        self.engine = game_engine
        self.selected_action = 0  # 0=Travel, 1=Hunt, 2=Rest, 3=Status
        self.animation_time = 0
    
    def handle_input(self, event):
        """Handle input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.selected_action = max(0, self.selected_action - 1)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.selected_action = min(3, self.selected_action + 1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._execute_action()
    
    def _execute_action(self):
        """Execute selected action."""
        if self.selected_action == 0:  # Travel
            self.engine.travel(20)
        elif self.selected_action == 1:  # Hunt
            self.engine.set_state(1)  # HUNT state
        elif self.selected_action == 2:  # Rest
            self.engine.rest(1)
        elif self.selected_action == 3:  # Status
            pass  # Show status on current screen
    
    def update(self, delta_time: float):
        """Update screen."""
        self.animation_time += delta_time
    
    def draw(self, renderer):
        """Draw screen with character graphics."""
        renderer.clear(COLORS['black'])
        
        # Draw terrain
        self._draw_terrain(renderer)
        
        # Draw top info bar
        renderer.draw_text(f"Distance: {self.engine.game_data.distance_traveled} miles",
                          20, 10, COLORS['light_green'])
        renderer.draw_text(f"Day {self.engine.game_data.current_day} - {self.engine.game_data.current_season} {self.engine.game_data.year}",
                          20, 25, COLORS['light_green'])
        
        # Draw resources (left side)
        renderer.draw_text("SUPPLIES:", 20, 50, COLORS['yellow'])
        renderer.draw_text(f"Food: {self.engine.game_data.resources.food}", 20, 65, COLORS['white'])
        renderer.draw_text(f"Ammo: {self.engine.game_data.resources.ammunition}", 20, 80, COLORS['white'])
        renderer.draw_text(f"Money: ${self.engine.game_data.resources.money}", 20, 95, COLORS['white'])
        
        # Draw party status with character graphics (center-right)
        self._draw_party_graphics(renderer)
        
        # Draw action buttons at bottom
        buttons = ["Travel", "Hunt", "Rest", "Status"]
        x_positions = [60, 175, 290, 395]
        
        for i, (button_text, x_pos) in enumerate(zip(buttons, x_positions)):
            color = COLORS['light_cyan'] if i == self.selected_action else COLORS['white']
            bg_color = COLORS['dark_gray'] if i == self.selected_action else COLORS['black']
            # Draw button background
            renderer.draw_rect(x_pos - 30, WINDOW_HEIGHT - 90, 90, 35, bg_color)
            renderer.draw_rect(x_pos - 30, WINDOW_HEIGHT - 90, 90, 35, color, filled=False, thickness=2)
            renderer.draw_text(button_text, x_pos - 20, WINDOW_HEIGHT - 80, color)
        
        renderer.draw_text("← → or A/D: Select | ENTER: Execute",
                          WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT - 25, COLORS['green'])
        
        renderer.update()
    
    def _draw_terrain(self, renderer):
        """Draw landscape."""
        # Sky
        renderer.draw_rect(0, 120, WINDOW_WIDTH, 100, COLORS['cyan'])
        # Grass
        renderer.draw_rect(0, 220, WINDOW_WIDTH, WINDOW_HEIGHT - 220, COLORS['green'])
        
        # Draw wagon on trail
        wagon_x = WINDOW_WIDTH // 3
        wagon_y = 200
        renderer.draw_rect(wagon_x, wagon_y, 60, 40, COLORS['brown'])
        renderer.draw_rect(wagon_x + 5, wagon_y + 5, 50, 20, COLORS['gray'])
        renderer.draw_circle(wagon_x + 10, wagon_y + 40, 6, COLORS['black'])
        renderer.draw_circle(wagon_x + 50, wagon_y + 40, 6, COLORS['black'])
    
    def _draw_party_graphics(self, renderer):
        """Draw party member portraits."""
        start_y = 50
        renderer.draw_text("PARTY:", 350, start_y, COLORS['light_cyan'])
        
        y = start_y + 20
        for i, member in enumerate(self.engine.game_data.party):
            # Draw character box
            char_color = COLORS['light_green'] if member.is_alive else COLORS['red']
            
            # Simple character portrait (colored square with name)
            renderer.draw_rect(350, y, 40, 40, char_color, filled=False, thickness=2)
            
            # Health bar
            health_width = int((member.health / 100) * 35)
            renderer.draw_rect(352, y + 35, health_width, 3, COLORS['green'])
            renderer.draw_rect(352 + health_width, y + 35, 35 - health_width, 3, COLORS['red'])
            
            # Name and status
            status = "✓" if member.is_alive else "✗"
            renderer.draw_text(f"{member.name}: {member.health}% {status}",
                             400, y + 5, COLORS['white'])
            
            y += 50
            if y > WINDOW_HEIGHT - 150:
                break


class HuntScreen(Screen):
    """Interactive hunting mini-game."""
    
    def __init__(self, game_engine):
        """Initialize hunt screen."""
        super().__init__()
        self.engine = game_engine
        self.hunt_time = 0
        self.targets = []
        self.shots_fired = 0
        self.animals_killed = 0
        self.meat_gathered = 0
        self.hunt_duration = 15.0
        self.mouse_pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self._spawn_animals()
    
    def _spawn_animals(self):
        """Spawn animals to hunt."""
        animal_types = ['deer', 'buffalo', 'rabbit']
        for _ in range(3):
            animal_type = random.choice(animal_types)
            x = random.randint(100, WINDOW_WIDTH - 100)
            y = random.randint(100, WINDOW_HEIGHT - 150)
            self.targets.append(HuntingTarget(x, y, animal_type))
    
    def handle_input(self, event):
        """Handle input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.shots_fired += 1
                self._check_hits()
            elif event.key == pygame.K_RETURN:
                self.engine.game_data.resources.food += self.meat_gathered
                self.engine.set_state(0)  # TRAVEL state
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
    
    def _check_hits(self):
        """Check if any targets were hit."""
        hit_range = 40
        for target in self.targets:
            if target.is_alive:
                dist = ((target.x - self.mouse_pos[0])**2 +
                       (target.y - self.mouse_pos[1])**2)**0.5
                if dist < hit_range:
                    target.is_alive = False
                    self.animals_killed += 1
                    self.meat_gathered += target.meat_amount
    
    def update(self, delta_time: float):
        """Update screen."""
        self.hunt_time += delta_time
        
        for target in self.targets:
            target.update(delta_time)
        
        # Spawn new animals
        if random.random() < 0.01 and len([t for t in self.targets if t.is_alive]) < 5:
            animal_types = ['deer', 'buffalo', 'rabbit']
            animal_type = random.choice(animal_types)
            x = random.randint(100, WINDOW_WIDTH - 100)
            y = random.randint(100, WINDOW_HEIGHT - 150)
            self.targets.append(HuntingTarget(x, y, animal_type))
        
        if self.hunt_time >= self.hunt_duration:
            self.engine.game_data.resources.food += self.meat_gathered
            self.engine.set_state(0)  # TRAVEL state
    
    def draw(self, renderer):
        """Draw hunting mini-game."""
        renderer.clear(COLORS['green'])
        
        # Draw hunting ground background
        renderer.draw_text("HUNTING GROUND", WINDOW_WIDTH // 2 - 70, 10,
                          COLORS['light_green'])
        
        # Draw animals
        for target in self.targets:
            if target.is_alive:
                color = (COLORS['green'] if target.animal_type == 'deer' else
                        (COLORS['brown'] if target.animal_type == 'buffalo' else COLORS['yellow']))
                renderer.draw_circle(int(target.x), int(target.y), target.size // 2, color)
                # Draw animal name
                renderer.draw_text(target.animal_type.upper(),
                                  int(target.x - 15), int(target.y - 10), color)
        
        # Draw crosshair
        mx, my = self.mouse_pos
        renderer.draw_circle(mx, my, 15, COLORS['red'], filled=False, thickness=2)
        renderer.draw_line(mx - 20, my, mx + 20, my, COLORS['red'])
        renderer.draw_line(mx, my - 20, mx, my + 20, COLORS['red'])
        
        # Draw stats
        renderer.draw_text(f"Time: {int(self.hunt_duration - self.hunt_time)}s",
                          20, WINDOW_HEIGHT - 100, COLORS['white'])
        renderer.draw_text(f"Shots: {self.shots_fired} | Killed: {self.animals_killed}",
                          20, WINDOW_HEIGHT - 80, COLORS['yellow'])
        renderer.draw_text(f"Meat: {self.meat_gathered} lbs",
                          20, WINDOW_HEIGHT - 60, COLORS['light_green'])
        
        renderer.draw_text("SPACE: Shoot | ENTER: Exit",
                          WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 30, COLORS['light_cyan'])
        
        renderer.update()


class RiverCrossingScreen(Screen):
    """Interactive river crossing mini-game."""
    
    def __init__(self, game_engine):
        """Initialize river crossing screen."""
        super().__init__()
        self.engine = game_engine
        self.raft_x = WINDOW_WIDTH // 2 - 20
        self.raft_y = WINDOW_HEIGHT // 2
        self.crossing_time = 0
        self.crossing_duration = 8.0
        self.obstacles = []
        self.health_lost = 0
        self._spawn_obstacles()
    
    def _spawn_obstacles(self):
        """Spawn river obstacles."""
        for _ in range(5):
            self.obstacles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(50, WINDOW_HEIGHT - 100),
                'vx': random.uniform(-100, 100),
                'vy': random.uniform(50, 150),
                'size': random.randint(10, 20)
            })
    
    def handle_input(self, event):
        """Handle input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.raft_x = max(0, self.raft_x - 20)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.raft_x = min(WINDOW_WIDTH - 40, self.raft_x + 20)
            elif event.key == pygame.K_RETURN:
                self.engine.set_state(0)  # TRAVEL state
    
    def update(self, delta_time: float):
        """Update screen."""
        self.crossing_time += delta_time
        
        # Update obstacles
        for obs in self.obstacles:
            obs['y'] += obs['vy'] * delta_time
            obs['x'] += obs['vx'] * delta_time
            
            # Check collision with raft
            if (self.raft_x < obs['x'] < self.raft_x + 40 and
                self.raft_y - obs['size'] < obs['y'] < self.raft_y + 30):
                self.health_lost += 10
                obs['y'] = -50  # Reset obstacle
        
        # Spawn new obstacles
        if random.random() < 0.05:
            self.obstacles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': -20,
                'vx': random.uniform(-50, 50),
                'vy': random.uniform(100, 200),
                'size': random.randint(8, 15)
            })
        
        # Remove off-screen obstacles
        self.obstacles = [o for o in self.obstacles if o['y'] < WINDOW_HEIGHT]
        
        if self.crossing_time >= self.crossing_duration:
            if self.health_lost < 100:
                self.engine.set_state(0)  # TRAVEL state - success
            else:
                # Major damage - party member dies
                for member in self.engine.game_data.party:
                    if member.is_alive:
                        member.health = 0
                        member.is_alive = False
                        break
                self.engine.set_state(0)
    
    def draw(self, renderer):
        """Draw river crossing mini-game."""
        renderer.clear(COLORS['blue'])
        
        renderer.draw_text("RIVER CROSSING", WINDOW_WIDTH // 2 - 70, 10,
                          COLORS['light_blue'])
        
        # Draw water waves
        wave_offset = (self.crossing_time * 20) % 40
        for x in range(0, WINDOW_WIDTH, 40):
            for y in range(0, WINDOW_HEIGHT, 40):
                renderer.draw_circle(x + int(wave_offset), y, 3, COLORS['light_blue'])
        
        # Draw raft
        renderer.draw_rect(self.raft_x, self.raft_y, 40, 30, COLORS['brown'])
        renderer.draw_rect(self.raft_x + 5, self.raft_y + 5, 30, 20, COLORS['yellow'])
        
        # Draw obstacles (logs)
        for obs in self.obstacles:
            renderer.draw_rect(obs['x'], obs['y'], obs['size'] * 2, obs['size'], COLORS['brown'])
        
        # Draw stats
        time_left = self.crossing_duration - self.crossing_time
        renderer.draw_text(f"Time: {int(time_left)}s", 20, WINDOW_HEIGHT - 100, COLORS['white'])
        renderer.draw_text(f"Damage: {int(self.health_lost)}%", 20, WINDOW_HEIGHT - 80, COLORS['red'])
        
        renderer.draw_text("← → or A/D: Dodge | ENTER: Skip",
                          WINDOW_WIDTH // 2 - 130, WINDOW_HEIGHT - 30, COLORS['light_cyan'])
        
        renderer.update()
