"""
Character and party status screens
"""

from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS


class CharacterStatusScreen:
    """Display individual character status."""
    
    def __init__(self):
        """Initialize character status screen."""
        self.character = None
    
    def set_character(self, character_data):
        """Set character to display."""
        self.character = character_data
    
    def draw(self, renderer):
        """Draw character status."""
        if not self.character:
            return
        
        # Title
        renderer.draw_text(
            f"Status of {self.character['name']}",
            50, 30,
            COLORS['light_cyan'],
            'large'
        )
        
        # Health section
        renderer.draw_rect(50, 80, 300, 150, COLORS['black'], filled=False, thickness=2)
        renderer.draw_text("HEALTH", 60, 90, COLORS['light_green'], 'medium')
        
        health = self.character.get('health', 100)
        health_color = (COLORS['light_green'] if health > 75 else 
                       COLORS['yellow'] if health > 50 else
                       COLORS['light_red'] if health > 25 else
                       COLORS['red'])
        
        renderer.draw_text(f"Health: {health}/100", 60, 120, health_color, 'medium')
        
        # Draw health bar
        bar_width = int((health / 100) * 250)
        renderer.draw_rect(60, 150, bar_width, 20, health_color)
        renderer.draw_rect(60, 150, 250, 20, COLORS['white'], filled=False, thickness=1)
        
        # Illness section
        renderer.draw_rect(380, 80, 250, 150, COLORS['black'], filled=False, thickness=2)
        renderer.draw_text("ILLNESS", 390, 90, COLORS['light_green'], 'medium')
        
        illness = self.character.get('illness', 'None')
        illness_color = COLORS['light_red'] if illness != 'None' else COLORS['light_green']
        
        renderer.draw_text(f"Condition: {illness}", 390, 120, illness_color, 'medium')
        
        if illness != 'None':
            days_ill = self.character.get('days_ill', 0)
            renderer.draw_text(f"Days ill: {days_ill}", 390, 150, COLORS['light_red'], 'medium')
        
        # Status section
        renderer.draw_rect(50, 250, WINDOW_WIDTH - 100, 120, COLORS['black'], filled=False, thickness=2)
        renderer.draw_text("STATUS", 60, 260, COLORS['light_green'], 'medium')
        
        is_alive = self.character.get('is_alive', True)
        alive_text = "ALIVE" if is_alive else "DECEASED"
        alive_color = COLORS['light_green'] if is_alive else COLORS['red']
        
        renderer.draw_text(f"Status: {alive_text}", 60, 290, alive_color, 'medium')
        
        # Instructions
        renderer.draw_text("Press SPACE to continue...", 50, WINDOW_HEIGHT - 40,
                          COLORS['light_cyan'], 'small')


class PartyStatusScreen:
    """Display entire party status."""
    
    def __init__(self):
        """Initialize party status screen."""
        self.party = []
        self.selected_index = 0
    
    def set_party(self, party_data):
        """Set party members to display."""
        self.party = party_data
    
    def select_next(self):
        """Select next party member."""
        if self.party:
            self.selected_index = (self.selected_index + 1) % len(self.party)
    
    def select_previous(self):
        """Select previous party member."""
        if self.party:
            self.selected_index = (self.selected_index - 1) % len(self.party)
    
    def get_selected_character(self):
        """Get selected character."""
        if 0 <= self.selected_index < len(self.party):
            return self.party[self.selected_index]
        return None
    
    def draw(self, renderer):
        """Draw party status."""
        # Title
        renderer.draw_text(
            "PARTY STATUS",
            WINDOW_WIDTH // 2 - 80,
            20,
            COLORS['light_cyan'],
            'large'
        )
        
        # List all party members
        start_y = 80
        item_height = 40
        
        for i, member in enumerate(self.party):
            y = start_y + i * item_height
            
            # Highlight selected
            if i == self.selected_index:
                renderer.draw_rect(40, y - 5, WINDOW_WIDTH - 80, item_height,
                                  COLORS['cyan'], filled=False, thickness=2)
                prefix = ">"
                color = COLORS['light_green']
            else:
                prefix = " "
                color = COLORS['light_white']
            
            # Member name
            name = member.get('name', f'Party Member {i+1}')
            health = member.get('health', 100)
            is_alive = member.get('is_alive', True)
            
            status = "ALIVE" if is_alive else "DEAD"
            status_color = COLORS['light_green'] if is_alive else COLORS['red']
            
            # Draw member info
            renderer.draw_text(
                f"{prefix} {i+1}. {name}",
                50, y,
                color,
                'medium'
            )
            
            # Health bar
            renderer.draw_rect(250, y, 150, 15, COLORS['red'])
            bar_width = int((health / 100) * 150)
            bar_color = COLORS['light_green'] if health > 50 else COLORS['yellow'] if health > 25 else COLORS['light_red']
            renderer.draw_rect(250, y, bar_width, 15, bar_color)
            renderer.draw_rect(250, y, 150, 15, COLORS['white'], filled=False, thickness=1)
            
            # Status
            renderer.draw_text(
                status,
                450, y,
                status_color,
                'medium'
            )
        
        # Instructions
        renderer.draw_text(
            "UP/DOWN to select member - Press 'V' to view details - SPACE to close",
            20, WINDOW_HEIGHT - 40,
            COLORS['light_cyan'],
            'small'
        )


class InventoryScreen:
    """Display inventory and supplies."""
    
    def __init__(self):
        """Initialize inventory screen."""
        self.resources = {}
    
    def set_resources(self, resources_data):
        """Set resources to display."""
        self.resources = resources_data
    
    def draw(self, renderer):
        """Draw inventory."""
        # Title
        renderer.draw_text(
            "SUPPLIES",
            WINDOW_WIDTH // 2 - 50,
            20,
            COLORS['light_cyan'],
            'large'
        )
        
        # Inventory boxes
        start_y = 100
        start_x = 80
        box_width = 200
        box_height = 100
        spacing_x = 240
        
        # Food
        renderer.draw_rect(start_x, start_y, box_width, box_height,
                          COLORS['black'], filled=False, thickness=2)
        renderer.draw_text("FOOD", start_x + 10, start_y + 10, COLORS['light_green'], 'medium')
        food = self.resources.get('food', 0)
        days_remaining = max(0, food // 2) if food > 0 else 0
        renderer.draw_text(f"{food} lbs", start_x + 10, start_y + 40, COLORS['light_white'], 'medium')
        renderer.draw_text(f"({days_remaining} days)", start_x + 10, start_y + 70, COLORS['yellow'], 'small')
        
        # Ammunition
        renderer.draw_rect(start_x + spacing_x, start_y, box_width, box_height,
                          COLORS['black'], filled=False, thickness=2)
        renderer.draw_text("AMMO", start_x + spacing_x + 10, start_y + 10, COLORS['light_green'], 'medium')
        ammo = self.resources.get('ammunition', 0)
        renderer.draw_text(f"{ammo} rounds", start_x + spacing_x + 10, start_y + 40, COLORS['light_white'], 'medium')
        
        # Medicine
        renderer.draw_rect(start_x + spacing_x * 2, start_y, box_width, box_height,
                          COLORS['black'], filled=False, thickness=2)
        renderer.draw_text("MEDICINE", start_x + spacing_x * 2 + 10, start_y + 10, COLORS['light_green'], 'medium')
        medicine = self.resources.get('medicine', 0)
        renderer.draw_text(f"{medicine} units", start_x + spacing_x * 2 + 10, start_y + 40, COLORS['light_white'], 'medium')
        
        # Spare Parts
        renderer.draw_rect(start_x, start_y + 130, box_width, box_height,
                          COLORS['black'], filled=False, thickness=2)
        renderer.draw_text("SPARE PARTS", start_x + 10, start_y + 140, COLORS['light_green'], 'medium')
        parts = self.resources.get('spare_parts', 0)
        renderer.draw_text(f"{parts} sets", start_x + 10, start_y + 170, COLORS['light_white'], 'medium')
        
        # Money
        renderer.draw_rect(start_x + spacing_x, start_y + 130, box_width, box_height,
                          COLORS['black'], filled=False, thickness=2)
        renderer.draw_text("MONEY", start_x + spacing_x + 10, start_y + 140, COLORS['light_green'], 'medium')
        money = self.resources.get('money', 0)
        renderer.draw_text(f"${money}", start_x + spacing_x + 10, start_y + 170, COLORS['yellow'], 'medium')
        
        # Instructions
        renderer.draw_text(
            "SPACE to close",
            50, WINDOW_HEIGHT - 40,
            COLORS['light_cyan'],
            'small'
        )
