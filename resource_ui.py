"""
Resource management UI with visual indicators and displays
"""

import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from graphics.ui_elements import UIElementGenerator
from typing import Tuple


class ResourceBar:
    """Visual resource bar with icon and text."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 label: str, icon_type: str, color: Tuple[int, int, int]):
        """Initialize resource bar.
        
        Args:
            x: X position
            y: Y position
            width: Bar width
            height: Bar height
            label: Resource label
            icon_type: Icon type for display
            color: Bar color
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.icon_type = icon_type
        self.color = color
        self.current_value = 100
        self.max_value = 100
        self.rect = pygame.Rect(x, y, width, height)
    
    def set_values(self, current: int, max_value: int):
        """Set bar values.
        
        Args:
            current: Current value
            max_value: Maximum value
        """
        self.current_value = max(0, min(current, max_value))
        self.max_value = max(1, max_value)
    
    def get_fill_percentage(self) -> float:
        """Get fill percentage.
        
        Returns:
            Percentage 0-1
        """
        if self.max_value == 0:
            return 0.0
        return self.current_value / self.max_value
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw resource bar.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        # Draw label
        renderer.draw_text(self.label, self.x, self.y - 20, COLORS['light_cyan'], 'small')
        
        # Draw background
        pygame.draw.rect(surface, COLORS['black'], self.rect)
        
        # Draw filled portion
        fill_width = int(self.width * self.get_fill_percentage())
        if fill_width > 0:
            pygame.draw.rect(surface, self.color, (self.x, self.y, fill_width, self.height))
        
        # Draw border
        pygame.draw.rect(surface, self.color, self.rect, 2)
        
        # Draw value text
        value_text = f"{self.current_value}/{self.max_value}"
        value_x = self.x + self.width + 10
        renderer.draw_text(value_text, value_x, self.y + 2, COLORS['white'], 'small')


class ResourceMeter:
    """Compact resource meter for HUD."""
    
    def __init__(self, x: int, y: int, size: int = 32):
        """Initialize resource meter.
        
        Args:
            x: X position
            y: Y position
            size: Meter size
        """
        self.x = x
        self.y = y
        self.size = size
        self.current = 100
        self.max_value = 100
        self.rect = pygame.Rect(x, y, size, size)
    
    def set_value(self, current: int, max_value: int = 100):
        """Set meter value.
        
        Args:
            current: Current value
            max_value: Maximum value
        """
        self.current = max(0, min(current, max_value))
        self.max_value = max(1, max_value)
    
    def draw(self, surface: pygame.Surface, color: Tuple[int, int, int] = COLORS['green']):
        """Draw meter.
        
        Args:
            surface: Surface to draw on
            color: Meter color
        """
        # Draw background
        pygame.draw.rect(surface, COLORS['black'], self.rect)
        
        # Draw fill
        percentage = self.current / self.max_value
        fill_height = int(self.size * percentage)
        fill_rect = pygame.Rect(self.x, self.y + self.size - fill_height, 
                               self.size, fill_height)
        pygame.draw.rect(surface, color, fill_rect)
        
        # Draw border
        pygame.draw.rect(surface, color, self.rect, 1)


class ResourcePanel:
    """Panel showing all resources with status."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """Initialize resource panel.
        
        Args:
            x: X position
            y: Y position
            width: Panel width
            height: Panel height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        
        # Resources
        self.resources = {
            'food': 800,
            'ammunition': 100,
            'medicine': 20,
            'spare_parts': 10,
            'money': 1600,
        }
        
        self.max_resources = {
            'food': 2000,
            'ammunition': 200,
            'medicine': 50,
            'spare_parts': 30,
            'money': 5000,
        }
        
        self._create_bars()
    
    def _create_bars(self):
        """Create resource bars."""
        self.bars = {}
        
        colors = {
            'food': COLORS['brown'],
            'ammunition': COLORS['yellow'],
            'medicine': COLORS['red'],
            'spare_parts': COLORS['gray'],
            'money': COLORS['light_green'],
        }
        
        bar_height = 15
        bar_spacing = 35
        
        for i, (resource_name, color) in enumerate(colors.items()):
            bar_y = self.y + 30 + (i * bar_spacing)
            bar = ResourceBar(self.x + 20, bar_y, self.width - 100, bar_height,
                            resource_name.replace('_', ' ').title(),
                            resource_name, color)
            self.bars[resource_name] = bar
    
    def update_resources(self, resources: dict):
        """Update resource values.
        
        Args:
            resources: Dictionary of resource values
        """
        self.resources.update(resources)
        
        for resource_name, bar in self.bars.items():
            current = self.resources.get(resource_name, 0)
            max_val = self.max_resources.get(resource_name, 100)
            bar.set_values(current, max_val)
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw panel.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        # Draw panel background
        pygame.draw.rect(surface, COLORS['black'], self.rect)
        pygame.draw.rect(surface, COLORS['green'], self.rect, 2)
        
        # Draw title
        renderer.draw_text("Resources", self.x + 10, self.y + 8, 
                         COLORS['light_green'], 'small')
        
        # Draw bars
        for bar in self.bars.values():
            bar.draw(surface, renderer)
        
        # Draw warnings for low supplies
        y_offset = 0
        for resource_name, bar in self.bars.items():
            if bar.get_fill_percentage() < 0.2:
                warning_y = bar.y
                renderer.draw_text("⚠", self.x + self.width - 20, warning_y + 2,
                                 COLORS['red'], 'small')
            y_offset += 1


class SupplyStatus:
    """Shows supply status indicators."""
    
    def __init__(self, x: int, y: int):
        """Initialize supply status.
        
        Args:
            x: X position
            y: Y position
        """
        self.x = x
        self.y = y
        self.meters = {
            'food': ResourceMeter(x, y),
            'ammunition': ResourceMeter(x + 40, y),
            'medicine': ResourceMeter(x + 80, y),
            'spare_parts': ResourceMeter(x + 120, y),
        }
    
    def update(self, resources: dict):
        """Update supply values.
        
        Args:
            resources: Resource dictionary
        """
        self.meters['food'].set_value(resources.get('food', 0), 2000)
        self.meters['ammunition'].set_value(resources.get('ammunition', 0), 200)
        self.meters['medicine'].set_value(resources.get('medicine', 0), 50)
        self.meters['spare_parts'].set_value(resources.get('spare_parts', 0), 30)
    
    def draw(self, surface: pygame.Surface):
        """Draw status.
        
        Args:
            surface: Surface to draw on
        """
        colors = {
            'food': COLORS['brown'],
            'ammunition': COLORS['yellow'],
            'medicine': COLORS['red'],
            'spare_parts': COLORS['gray'],
        }
        
        for name, meter in self.meters.items():
            meter.draw(surface, colors[name])


class ResourceWarning:
    """Warning system for low resources."""
    
    def __init__(self):
        """Initialize resource warning."""
        self.warnings = []
        self.blink_time = 0.0
        self.blink_rate = 0.5
    
    def check_resources(self, resources: dict):
        """Check resources and generate warnings.
        
        Args:
            resources: Resource dictionary
        """
        self.warnings = []
        
        if resources.get('food', 0) < 100:
            self.warnings.append(("STARVATION WARNING", COLORS['red']))
        
        if resources.get('ammunition', 0) < 5:
            self.warnings.append(("LOW AMMUNITION", COLORS['yellow']))
        
        if resources.get('medicine', 0) < 2:
            self.warnings.append(("LOW MEDICINE", COLORS['red']))
        
        if resources.get('money', 0) < 50:
            self.warnings.append(("LOW FUNDS", COLORS['yellow']))
    
    def update(self, delta_time: float):
        """Update warning state.
        
        Args:
            delta_time: Time since last frame
        """
        self.blink_time += delta_time
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw warnings.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        # Only show if blinking (active)
        if int(self.blink_time / self.blink_rate) % 2 == 0:
            y = 10
            for warning_text, color in self.warnings:
                renderer.draw_text(warning_text, WINDOW_WIDTH - 200, y, color, 'small')
                y += 20


class ResourceShortageIndicator:
    """Indicator showing resource shortage status."""
    
    def __init__(self, x: int, y: int, size: int = 20):
        """Initialize shortage indicator.
        
        Args:
            x: X position
            y: Y position
            size: Indicator size
        """
        self.x = x
        self.y = y
        self.size = size
        self.status = 'good'  # good, warning, critical
    
    def update_status(self, food: int, ammo: int, medicine: int, parts: int):
        """Update shortage status.
        
        Args:
            food: Food amount
            ammo: Ammunition amount
            medicine: Medicine amount
            parts: Spare parts amount
        """
        if food < 50 or ammo < 2 or medicine < 1 or parts < 1:
            self.status = 'critical'
        elif food < 200 or ammo < 10 or medicine < 3 or parts < 2:
            self.status = 'warning'
        else:
            self.status = 'good'
    
    def draw(self, surface: pygame.Surface):
        """Draw indicator.
        
        Args:
            surface: Surface to draw on
        """
        color_map = {
            'good': COLORS['green'],
            'warning': COLORS['yellow'],
            'critical': COLORS['red'],
        }
        
        color = color_map[self.status]
        pygame.draw.circle(surface, color, (self.x, self.y), self.size // 2)
        pygame.draw.circle(surface, COLORS['white'], (self.x, self.y), self.size // 2, 1)


class ResourceTracker:
    """Centralized resource tracking and display."""
    
    def __init__(self):
        """Initialize resource tracker."""
        self.food = 800
        self.ammunition = 100
        self.medicine = 20
        self.spare_parts = 10
        self.money = 1600
        
        self.panel = ResourcePanel(10, 300, 300, 250)
        self.supply_status = SupplyStatus(WINDOW_WIDTH - 200, 50)
        self.shortage_indicator = ResourceShortageIndicator(WINDOW_WIDTH - 30, 30)
        self.warning_system = ResourceWarning()
    
    def set_resources(self, food: int, ammunition: int, medicine: int, 
                     spare_parts: int, money: int):
        """Set resource values.
        
        Args:
            food: Food amount
            ammunition: Ammunition amount
            medicine: Medicine amount
            spare_parts: Spare parts amount
            money: Money amount
        """
        self.food = food
        self.ammunition = ammunition
        self.medicine = medicine
        self.spare_parts = spare_parts
        self.money = money
        
        resources = {
            'food': food,
            'ammunition': ammunition,
            'medicine': medicine,
            'spare_parts': spare_parts,
            'money': money,
        }
        
        self.panel.update_resources(resources)
        self.supply_status.update(resources)
        self.shortage_indicator.update_status(food, ammunition, medicine, spare_parts)
        self.warning_system.check_resources(resources)
    
    def update(self, delta_time: float):
        """Update tracker.
        
        Args:
            delta_time: Time since last frame
        """
        self.warning_system.update(delta_time)
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw tracker.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        self.panel.draw(surface, renderer)
        self.supply_status.draw(surface)
        self.shortage_indicator.draw(surface)
        self.warning_system.draw(surface, renderer)
    
    def get_resources(self) -> dict:
        """Get current resources.
        
        Returns:
            Dictionary of resources
        """
        return {
            'food': self.food,
            'ammunition': self.ammunition,
            'medicine': self.medicine,
            'spare_parts': self.spare_parts,
            'money': self.money,
        }
