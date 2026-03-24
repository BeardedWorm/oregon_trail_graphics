"""
Trail map visualization
"""

from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from models import TrailLocation


class TrailMap:
    """Display trail with party position and locations."""
    
    def __init__(self):
        """Initialize trail map."""
        self.locations = TrailLocation.all_locations()
        self.party_distance = 0
        self.total_distance = 1600
        
        # Map display settings
        self.map_x = 50
        self.map_y = 100
        self.map_width = WINDOW_WIDTH - 100
        self.map_height = 200
    
    def set_party_position(self, distance):
        """Update party position on trail."""
        self.party_distance = min(distance, self.total_distance)
    
    def get_pixel_position(self, distance):
        """Convert trail distance to screen position."""
        if self.total_distance == 0:
            return self.map_x
        
        ratio = distance / self.total_distance
        return self.map_x + int(ratio * self.map_width)
    
    def draw_trail_line(self, renderer):
        """Draw the main trail line."""
        # Draw trail background
        renderer.draw_rect(
            self.map_x, self.map_y + self.map_height // 2 - 2,
            self.map_width, 4,
            COLORS['brown']
        )
        
        # Draw completed trail
        completed_distance = min(self.party_distance, self.total_distance)
        completed_width = int((completed_distance / self.total_distance) * self.map_width)
        renderer.draw_rect(
            self.map_x, self.map_y + self.map_height // 2 - 2,
            completed_width, 4,
            COLORS['light_green']
        )
    
    def draw_locations(self, renderer):
        """Draw trail locations."""
        for location in self.locations:
            x = self.get_pixel_position(location.distance_from_start)
            y = self.map_y + self.map_height // 2
            
            # Draw location marker
            marker_size = 4
            renderer.draw_circle(x, y, marker_size, COLORS['light_cyan'], filled=True)
            
            # Highlight current or next location
            if location.distance_from_start <= self.party_distance:
                renderer.draw_circle(x, y, marker_size + 1, COLORS['light_green'], filled=False, thickness=1)
            elif location.distance_from_start - self.party_distance < 100:
                renderer.draw_circle(x, y, marker_size + 1, COLORS['yellow'], filled=False, thickness=1)
    
    def draw_party_position(self, renderer):
        """Draw current party position."""
        x = self.get_pixel_position(self.party_distance)
        y = self.map_y + self.map_height // 2
        
        # Draw wagon symbol
        renderer.draw_rect(x - 5, y - 8, 10, 16, COLORS['light_red'])
        renderer.draw_circle(x - 7, y + 10, 3, COLORS['light_red'], filled=True)
        renderer.draw_circle(x + 7, y + 10, 3, COLORS['light_red'], filled=True)
    
    def draw_location_labels(self, renderer):
        """Draw location names."""
        # Draw top labels
        top_locations = [self.locations[i] for i in range(0, len(self.locations), 2)]
        
        for location in top_locations:
            x = self.get_pixel_position(location.distance_from_start)
            y = self.map_y - 20
            
            # Truncate long names
            name = location.name[:12]
            renderer.draw_text(name, x - 20, y, COLORS['light_cyan'], 'small')
        
        # Draw bottom labels
        bottom_locations = [self.locations[i] for i in range(1, len(self.locations), 2)]
        
        for location in bottom_locations:
            x = self.get_pixel_position(location.distance_from_start)
            y = self.map_y + self.map_height + 5
            
            # Truncate long names
            name = location.name[:12]
            renderer.draw_text(name, x - 20, y, COLORS['light_cyan'], 'small')
    
    def draw_progress_info(self, renderer):
        """Draw progress information."""
        # Distance traveled
        renderer.draw_text(
            f"Distance: {self.party_distance} / {self.total_distance} miles",
            self.map_x, self.map_y + self.map_height + 50,
            COLORS['light_green'],
            'medium'
        )
        
        # Progress percentage
        progress_pct = int((self.party_distance / self.total_distance) * 100)
        renderer.draw_text(
            f"Progress: {progress_pct}%",
            self.map_x + 300, self.map_y + self.map_height + 50,
            COLORS['light_green'],
            'medium'
        )
        
        # Distance remaining
        remaining = max(0, self.total_distance - self.party_distance)
        renderer.draw_text(
            f"Remaining: {remaining} miles",
            self.map_x + 500, self.map_y + self.map_height + 50,
            COLORS['yellow'],
            'medium'
        )
    
    def draw(self, renderer):
        """Draw the complete map."""
        # Title
        renderer.draw_text(
            "TRAIL MAP",
            WINDOW_WIDTH // 2 - 50,
            20,
            COLORS['light_cyan'],
            'large'
        )
        
        # Draw map border
        renderer.draw_rect(
            self.map_x - 5, self.map_y - 5,
            self.map_width + 10, self.map_height + 10,
            COLORS['white'],
            filled=False,
            thickness=2
        )
        
        # Draw trail components
        self.draw_trail_line(renderer)
        self.draw_locations(renderer)
        self.draw_party_position(renderer)
        self.draw_location_labels(renderer)
        self.draw_progress_info(renderer)


class MiniMap:
    """Small version of the map for HUD."""
    
    def __init__(self, x, y, width=150, height=40):
        """Initialize mini map."""
        self.locations = TrailLocation.all_locations()
        self.party_distance = 0
        self.total_distance = 1600
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def set_party_position(self, distance):
        """Update party position."""
        self.party_distance = min(distance, self.total_distance)
    
    def get_pixel_position(self, distance):
        """Convert distance to pixel position."""
        if self.total_distance == 0:
            return self.x
        ratio = distance / self.total_distance
        return self.x + int(ratio * self.width)
    
    def draw(self, renderer):
        """Draw mini map."""
        # Draw background
        renderer.draw_rect(self.x, self.y, self.width, self.height, COLORS['black'])
        
        # Draw trail line
        renderer.draw_line(
            self.x, self.y + self.height // 2,
            self.x + self.width, self.y + self.height // 2,
            COLORS['brown'],
            thickness=2
        )
        
        # Draw completed trail
        completed_width = int((self.party_distance / self.total_distance) * self.width)
        renderer.draw_line(
            self.x, self.y + self.height // 2,
            self.x + completed_width, self.y + self.height // 2,
            COLORS['light_green'],
            thickness=2
        )
        
        # Draw party position
        party_x = self.get_pixel_position(self.party_distance)
        renderer.draw_circle(party_x, self.y + self.height // 2, 2, COLORS['light_red'], filled=True)
        
        # Draw border
        renderer.draw_rect(self.x, self.y, self.width, self.height, COLORS['light_cyan'], filled=False, thickness=1)
