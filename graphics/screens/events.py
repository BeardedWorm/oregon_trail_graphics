"""
Event system UI for displaying game events and encounters
"""

from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS


class EventMessage:
    """Single event message."""
    
    def __init__(self, title, text, event_type='info'):
        """Initialize event message."""
        self.title = title
        self.text = text
        self.event_type = event_type  # info, danger, success, warning
        self.displayed = False
    
    def get_color(self):
        """Get message color based on type."""
        if self.event_type == 'danger':
            return COLORS['light_red']
        elif self.event_type == 'success':
            return COLORS['light_green']
        elif self.event_type == 'warning':
            return COLORS['yellow']
        else:
            return COLORS['light_cyan']


class EventDisplay:
    """Display game events."""
    
    def __init__(self):
        """Initialize event display."""
        self.events = []
        self.current_event = None
        self.display_counter = 0
        self.display_duration = 300  # Frames
        
        # Event types with descriptions
        self.event_templates = {
            'snake_bite': {
                'title': 'SNAKE BITE!',
                'text': 'One member was bitten by a snake!',
                'type': 'danger'
            },
            'lost_in_woods': {
                'title': 'Lost in Woods',
                'text': 'You got lost in thick woods. Progress slowed.',
                'type': 'warning'
            },
            'found_berries': {
                'title': 'Food Found!',
                'text': 'You found fresh berries and other vegetation!',
                'type': 'success'
            },
            'river_crossing': {
                'title': 'River Hazard!',
                'text': 'The river crossing was treacherous. Parts damaged.',
                'type': 'warning'
            },
            'illness_outbreak': {
                'title': 'Illness!',
                'text': 'A member has fallen ill with dysentery.',
                'type': 'danger'
            },
            'supply_low': {
                'title': 'Low Supplies!',
                'text': 'You are running low on food.',
                'type': 'danger'
            },
            'weather_clear': {
                'title': 'Clear Skies',
                'text': 'Perfect weather for traveling.',
                'type': 'success'
            },
            'weather_storm': {
                'title': 'Terrible Storm!',
                'text': 'A severe storm delayed your progress.',
                'type': 'warning'
            },
            'reached_location': {
                'title': 'Landmark Reached!',
                'text': 'You have arrived at a significant landmark.',
                'type': 'success'
            },
            'hunting_success': {
                'title': 'Successful Hunt!',
                'text': 'You successfully hunted large game!',
                'type': 'success'
            },
            'hunting_failure': {
                'title': 'Hunting Failed',
                'text': 'You did not find any game today.',
                'type': 'warning'
            },
        }
    
    def add_event(self, event_key, duration=300):
        """Add an event to display."""
        if event_key in self.event_templates:
            template = self.event_templates[event_key]
            event = EventMessage(
                template['title'],
                template['text'],
                template['type']
            )
            event.duration = duration
            self.events.append(event)
    
    def add_custom_event(self, title, text, event_type='info', duration=300):
        """Add a custom event."""
        event = EventMessage(title, text, event_type)
        event.duration = duration
        self.events.append(event)
    
    def update(self, dt=1):
        """Update event display."""
        if self.current_event:
            self.display_counter -= dt
            if self.display_counter <= 0:
                if self.events:
                    self.current_event = self.events.pop(0)
                    self.display_counter = self.current_event.duration
                else:
                    self.current_event = None
        elif self.events:
            self.current_event = self.events.pop(0)
            self.display_counter = self.current_event.duration
    
    def draw(self, renderer):
        """Draw event display."""
        if not self.current_event:
            return
        
        # Draw event box
        box_x = 100
        box_y = 50
        box_width = WINDOW_WIDTH - 200
        box_height = 150
        
        # Draw background
        renderer.draw_rect(box_x, box_y, box_width, box_height, COLORS['black'])
        
        # Draw border
        border_color = self.current_event.get_color()
        renderer.draw_rect(box_x, box_y, box_width, box_height, border_color, filled=False, thickness=3)
        
        # Draw title
        renderer.draw_text(
            self.current_event.title,
            box_x + 20, box_y + 15,
            border_color,
            'large'
        )
        
        # Draw text (word wrap)
        text = self.current_event.text
        lines = self._wrap_text(text, 70)
        
        y_offset = box_y + 55
        for line in lines:
            renderer.draw_text(
                line,
                box_x + 20, y_offset,
                COLORS['light_white'],
                'medium'
            )
            y_offset += 30
        
        # Draw progress bar
        progress_ratio = 1.0 - (self.display_counter / self.current_event.duration)
        bar_width = int((progress_ratio) * (box_width - 40))
        renderer.draw_rect(box_x + 20, box_y + box_height - 15, bar_width, 8, border_color)
        renderer.draw_rect(box_x + 20, box_y + box_height - 15, box_width - 40, 8,
                          COLORS['white'], filled=False, thickness=1)
    
    def _wrap_text(self, text, char_per_line=70):
        """Wrap text into lines."""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= char_per_line:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
    
    def has_events(self):
        """Check if there are pending events."""
        return self.current_event is not None or len(self.events) > 0


class DialogBox:
    """Generic dialog box for user interaction."""
    
    def __init__(self, title, message, options=None):
        """Initialize dialog box."""
        self.title = title
        self.message = message
        self.options = options or ['OK']
        self.selected_option = 0
        self.is_open = False
    
    def select_next(self):
        """Select next option."""
        self.selected_option = (self.selected_option + 1) % len(self.options)
    
    def select_previous(self):
        """Select previous option."""
        self.selected_option = (self.selected_option - 1) % len(self.options)
    
    def get_selected_option(self):
        """Get selected option text."""
        if 0 <= self.selected_option < len(self.options):
            return self.options[self.selected_option]
        return None
    
    def draw(self, renderer):
        """Draw dialog box."""
        if not self.is_open:
            return
        
        # Draw dialog box
        box_x = WINDOW_WIDTH // 2 - 150
        box_y = WINDOW_HEIGHT // 2 - 100
        box_width = 300
        box_height = 200
        
        # Draw background
        renderer.draw_rect(box_x, box_y, box_width, box_height, COLORS['black'])
        
        # Draw border
        renderer.draw_rect(box_x, box_y, box_width, box_height, COLORS['light_cyan'], filled=False, thickness=2)
        
        # Draw title
        renderer.draw_text(
            self.title,
            box_x + 20, box_y + 15,
            COLORS['light_cyan'],
            'medium'
        )
        
        # Draw message
        lines = self.message.split('\n')
        y_offset = box_y + 50
        for line in lines:
            renderer.draw_text(line, box_x + 20, y_offset, COLORS['light_white'], 'small')
            y_offset += 25
        
        # Draw options
        option_y = box_y + box_height - 50
        option_spacing = 100
        
        for i, option in enumerate(self.options):
            x = box_x + 50 + i * option_spacing
            
            if i == self.selected_option:
                color = COLORS['light_green']
                prefix = "["
                suffix = "]"
            else:
                color = COLORS['light_white']
                prefix = " "
                suffix = " "
            
            renderer.draw_text(
                f"{prefix} {option} {suffix}",
                x, option_y,
                color,
                'medium'
            )
