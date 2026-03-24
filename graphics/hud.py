"""
HUD (Heads-Up Display) system for in-game information
"""

from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from graphics.sprites import SpriteGroup


class HUDElement:
    """Base HUD element."""
    
    def __init__(self, x, y, width, height):
        """Initialize HUD element."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def update(self, data):
        """Update element data."""
        pass
    
    def draw(self, renderer):
        """Draw the element."""
        pass


class HealthBar(HUDElement):
    """Health/status bar."""
    
    def __init__(self, x, y, width, height, max_value=100):
        """Initialize health bar."""
        super().__init__(x, y, width, height)
        self.current = max_value
        self.max = max_value
    
    def update(self, value):
        """Update current value."""
        self.current = max(0, min(value, self.max))
    
    def draw(self, renderer):
        """Draw health bar."""
        # Background
        renderer.draw_rect(self.x, self.y, self.width, self.height, COLORS['red'])
        
        # Current value bar
        bar_width = (self.current / self.max) * self.width
        color = COLORS['light_green'] if self.current > 50 else (COLORS['yellow'] if self.current > 25 else COLORS['light_red'])
        renderer.draw_rect(self.x, self.y, bar_width, self.height, color)
        
        # Border
        renderer.draw_rect(self.x, self.y, self.width, self.height, COLORS['white'], filled=False, thickness=1)


class ResourceDisplay(HUDElement):
    """Display for resources (food, ammo, etc.)."""
    
    def __init__(self, x, y):
        """Initialize resource display."""
        super().__init__(x, y, 150, 100)
        self.food = 0
        self.ammunition = 0
        self.medicine = 0
        self.spare_parts = 0
    
    def update(self, resources):
        """Update resource values."""
        self.food = resources.get('food', 0)
        self.ammunition = resources.get('ammunition', 0)
        self.medicine = resources.get('medicine', 0)
        self.spare_parts = resources.get('spare_parts', 0)
    
    def draw(self, renderer):
        """Draw resource display."""
        renderer.draw_rect(self.x, self.y, self.width, self.height, COLORS['black'], filled=False, thickness=2)
        
        renderer.draw_text(f"Food: {self.food} lbs", self.x + 5, self.y + 5, COLORS['light_green'], 'small')
        renderer.draw_text(f"Ammo: {self.ammunition}", self.x + 5, self.y + 25, COLORS['light_cyan'], 'small')
        renderer.draw_text(f"Med: {self.medicine}", self.x + 5, self.y + 45, COLORS['light_red'], 'small')
        renderer.draw_text(f"Parts: {self.spare_parts}", self.x + 5, self.y + 65, COLORS['yellow'], 'small')


class DateDisplay(HUDElement):
    """Display for current date."""
    
    def __init__(self, x, y):
        """Initialize date display."""
        super().__init__(x, y, 150, 50)
        self.day = 1
        self.season = "Spring"
        self.year = 1848
    
    def update(self, data):
        """Update date."""
        self.day = data.get('day', 1)
        self.season = data.get('season', 'Spring')
        self.year = data.get('year', 1848)
    
    def draw(self, renderer):
        """Draw date display."""
        renderer.draw_rect(self.x, self.y, self.width, self.height, COLORS['black'], filled=False, thickness=2)
        
        renderer.draw_text(f"Day {self.day} {self.season}", self.x + 5, self.y + 10, COLORS['light_cyan'], 'small')
        renderer.draw_text(f"Year {self.year}", self.x + 5, self.y + 30, COLORS['light_green'], 'small')


class LocationDisplay(HUDElement):
    """Display for current location."""
    
    def __init__(self, x, y):
        """Initialize location display."""
        super().__init__(x, y, 200, 40)
        self.location = "Missouri River"
        self.distance = 0
    
    def update(self, data):
        """Update location."""
        self.location = data.get('location', 'Unknown')
        self.distance = data.get('distance', 0)
    
    def draw(self, renderer):
        """Draw location display."""
        renderer.draw_rect(self.x, self.y, self.width, self.height, COLORS['black'], filled=False, thickness=2)
        
        renderer.draw_text(f"Location: {self.location}", self.x + 5, self.y + 5, COLORS['light_cyan'], 'small')
        renderer.draw_text(f"Distance: {self.distance}/1600 miles", self.x + 5, self.y + 20, COLORS['light_green'], 'small')


class GameHUD:
    """Complete HUD system."""
    
    def __init__(self):
        """Initialize HUD."""
        self.elements = []
        self.sprites = SpriteGroup()
        
        # Create HUD elements
        self.health_bars = {}  # Map of party member names to health bars
        self.resources = ResourceDisplay(10, 50)
        self.date = DateDisplay(WINDOW_WIDTH - 160, 10)
        self.location = LocationDisplay(10, 10)
        
        self.elements.append(self.resources)
        self.elements.append(self.date)
        self.elements.append(self.location)
    
    def add_party_member(self, name):
        """Add health bar for party member."""
        y_offset = 50 + len(self.health_bars) * 30
        bar = HealthBar(WINDOW_WIDTH - 210, y_offset, 200, 20, 100)
        self.health_bars[name] = bar
        self.elements.append(bar)
    
    def update_resources(self, resources):
        """Update resource display."""
        resource_dict = {
            'food': resources.get('food', 0),
            'ammunition': resources.get('ammunition', 0),
            'medicine': resources.get('medicine', 0),
            'spare_parts': resources.get('spare_parts', 0),
        }
        self.resources.update(resource_dict)
    
    def update_date(self, day, season, year):
        """Update date display."""
        self.date.update({'day': day, 'season': season, 'year': year})
    
    def update_location(self, location, distance):
        """Update location display."""
        self.location.update({'location': location, 'distance': distance})
    
    def update_health(self, member_name, health):
        """Update party member health."""
        if member_name in self.health_bars:
            self.health_bars[member_name].update(health)
    
    def draw(self, renderer):
        """Draw entire HUD."""
        for element in self.elements:
            element.draw(renderer)
    
    def update(self):
        """Update HUD state."""
        for element in self.elements:
            element.update({})


class MessageBox(HUDElement):
    """Display messages and events."""
    
    def __init__(self, x, y, width, height):
        """Initialize message box."""
        super().__init__(x, y, width, height)
        self.messages = []
        self.current_message = None
        self.display_time = 0
        self.max_display_time = 300  # Frames
    
    def add_message(self, text, duration=300):
        """Add a message."""
        self.messages.append({'text': text, 'duration': duration})
    
    def update(self, dt=1):
        """Update message display."""
        if self.current_message:
            self.display_time -= dt
            if self.display_time <= 0:
                if self.messages:
                    msg = self.messages.pop(0)
                    self.current_message = msg['text']
                    self.display_time = msg['duration']
                else:
                    self.current_message = None
        elif self.messages:
            msg = self.messages.pop(0)
            self.current_message = msg['text']
            self.display_time = msg['duration']
    
    def draw(self, renderer):
        """Draw message box."""
        if not self.current_message:
            return
        
        # Draw box background
        renderer.draw_rect(self.x, self.y, self.width, self.height, COLORS['black'])
        renderer.draw_rect(self.x, self.y, self.width, self.height, COLORS['light_cyan'], filled=False, thickness=2)
        
        # Draw message text
        renderer.draw_text(self.current_message, self.x + 10, self.y + 10, COLORS['light_white'], 'medium')
