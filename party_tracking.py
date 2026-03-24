"""
Enhanced party member tracking with visual health and status indicators
"""

import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from typing import List, Tuple, Optional
from models import PartyMember


class PartyMemberDisplay:
    """Visual display for a party member."""
    
    def __init__(self, x: int, y: int, size: int = 60):
        """Initialize party member display.
        
        Args:
            x: X position
            y: Y position
            size: Display size
        """
        self.x = x
        self.y = y
        self.size = size
        self.member = None
        self.rect = pygame.Rect(x, y, size, size)
        self.hover = False
    
    def set_member(self, member: PartyMember):
        """Set member to display.
        
        Args:
            member: Party member
        """
        self.member = member
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw member display.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        if not self.member:
            return
        
        # Draw background
        bg_color = COLORS['gray'] if self.hover else COLORS['black']
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, COLORS['white'], self.rect, 1)
        
        # Draw character icon
        if self.member.is_alive:
            pygame.draw.circle(surface, COLORS['light_green'],
                             (self.x + self.size // 2, self.y + 15), 8)
        else:
            pygame.draw.rect(surface, COLORS['red'],
                           (self.x + self.size // 4, self.y + 8, self.size // 2, 14))
        
        # Draw health bar
        health_bar_width = self.size - 10
        health_bar_height = 6
        health_bar_x = self.x + 5
        health_bar_y = self.y + 35
        
        pygame.draw.rect(surface, COLORS['black'], 
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        
        if self.member.health > 0:
            fill_width = int(health_bar_width * (self.member.health / 100))
            health_color = COLORS['green'] if self.member.health > 50 else \
                          COLORS['yellow'] if self.member.health > 25 else COLORS['red']
            pygame.draw.rect(surface, health_color,
                           (health_bar_x, health_bar_y, fill_width, health_bar_height))
        
        pygame.draw.rect(surface, COLORS['white'],
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 1)
        
        # Draw name (abbreviated)
        name_short = self.member.name[:8]
        # Would need font to render properly


class PartyStatusPanel:
    """Panel showing all party members."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """Initialize party status panel.
        
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
        self.member_displays = []
        self.party = []
    
    def set_party(self, party: List[PartyMember]):
        """Set party to display.
        
        Args:
            party: List of party members
        """
        self.party = party
        self._create_displays()
    
    def _create_displays(self):
        """Create displays for all members."""
        self.member_displays = []
        
        display_size = 50
        spacing = 60
        
        for i, member in enumerate(self.party):
            x = self.x + 20 + (i * spacing)
            y = self.y + 40
            display = PartyMemberDisplay(x, y, display_size)
            display.set_member(member)
            self.member_displays.append(display)
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw panel.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        # Draw panel background
        pygame.draw.rect(surface, COLORS['black'], self.rect)
        pygame.draw.rect(surface, COLORS['cyan'], self.rect, 2)
        
        # Draw title
        renderer.draw_text("Party Status", self.x + 10, self.y + 8,
                         COLORS['light_cyan'], 'small')
        
        # Draw member displays
        for display in self.member_displays:
            display.draw(surface, renderer)
        
        # Draw legend
        legend_y = self.y + self.height - 20
        renderer.draw_text("Green=Alive", self.x + 20, legend_y, COLORS['green'], 'small')
        renderer.draw_text("Red=Dead", self.x + 150, legend_y, COLORS['red'], 'small')


class PartyMemberCard:
    """Detailed card for a party member."""
    
    def __init__(self, x: int, y: int, width: int = 150, height: int = 180):
        """Initialize party member card.
        
        Args:
            x: X position
            y: Y position
            width: Card width
            height: Card height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.member = None
    
    def set_member(self, member: PartyMember):
        """Set member to display.
        
        Args:
            member: Party member
        """
        self.member = member
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw card.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        if not self.member:
            return
        
        # Draw card background
        pygame.draw.rect(surface, COLORS['black'], self.rect)
        pygame.draw.rect(surface, COLORS['green'], self.rect, 2)
        
        y_offset = self.y + 10
        
        # Draw name
        renderer.draw_text(self.member.name, self.x + 10, y_offset,
                         COLORS['light_green'], 'small')
        y_offset += 25
        
        # Draw status
        status = "Alive" if self.member.is_alive else "Dead"
        status_color = COLORS['green'] if self.member.is_alive else COLORS['red']
        renderer.draw_text(f"Status: {status}", self.x + 10, y_offset,
                         status_color, 'small')
        y_offset += 20
        
        # Draw health
        renderer.draw_text(f"Health: {self.member.health}%", self.x + 10, y_offset,
                         COLORS['yellow'], 'small')
        y_offset += 20
        
        # Draw health bar
        health_bar_width = self.width - 20
        health_bar_height = 8
        pygame.draw.rect(surface, COLORS['black'],
                        (self.x + 10, y_offset, health_bar_width, health_bar_height))
        
        fill_width = int(health_bar_width * (self.member.health / 100))
        health_color = COLORS['green'] if self.member.health > 50 else \
                      COLORS['yellow'] if self.member.health > 25 else COLORS['red']
        pygame.draw.rect(surface, health_color,
                        (self.x + 10, y_offset, fill_width, health_bar_height))
        pygame.draw.rect(surface, COLORS['white'],
                        (self.x + 10, y_offset, health_bar_width, health_bar_height), 1)
        
        y_offset += 20
        
        # Draw illness if present
        if self.member.illness:
            renderer.draw_text(f"Illness: {self.member.illness}", self.x + 10, y_offset,
                             COLORS['red'], 'small')
            y_offset += 15
            renderer.draw_text(f"Days: {self.member.days_ill}", self.x + 10, y_offset,
                             COLORS['red'], 'small')


class PartyHealthOverview:
    """Overview of total party health."""
    
    def __init__(self, x: int, y: int):
        """Initialize health overview.
        
        Args:
            x: X position
            y: Y position
        """
        self.x = x
        self.y = y
        self.party = []
        self.total_health = 0
        self.avg_health = 0
        self.alive_count = 0
    
    def set_party(self, party: List[PartyMember]):
        """Set party.
        
        Args:
            party: List of party members
        """
        self.party = party
        self._calculate_stats()
    
    def _calculate_stats(self):
        """Calculate party statistics."""
        self.alive_count = len([m for m in self.party if m.is_alive])
        
        if self.alive_count > 0:
            health_sum = sum(m.health for m in self.party if m.is_alive)
            self.avg_health = health_sum / self.alive_count
        else:
            self.avg_health = 0
        
        self.total_health = sum(m.health for m in self.party)
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw overview.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        renderer.draw_text(f"Alive: {self.alive_count}/{len(self.party)}",
                         self.x, self.y, COLORS['light_green'], 'small')
        renderer.draw_text(f"Avg Health: {int(self.avg_health)}%",
                         self.x, self.y + 20, COLORS['yellow'], 'small')
        renderer.draw_text(f"Total: {self.total_health}%",
                         self.x, self.y + 40, COLORS['white'], 'small')


class PartyTracker:
    """Centralized party tracking and display."""
    
    def __init__(self):
        """Initialize party tracker."""
        self.party = []
        self.status_panel = PartyStatusPanel(10, 50, WINDOW_WIDTH - 20, 120)
        self.health_overview = PartyHealthOverview(10, 180)
        self.selected_member_index = 0
    
    def set_party(self, party: List[PartyMember]):
        """Set party to track.
        
        Args:
            party: List of party members
        """
        self.party = party
        self.status_panel.set_party(party)
        self.health_overview.set_party(party)
    
    def update(self):
        """Update tracker."""
        self.health_overview.set_party(self.party)
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw tracker.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        self.status_panel.draw(surface, renderer)
        self.health_overview.draw(surface, renderer)
    
    def get_party_summary(self) -> dict:
        """Get party summary.
        
        Returns:
            Dictionary with party stats
        """
        alive_members = [m for m in self.party if m.is_alive]
        
        return {
            'total': len(self.party),
            'alive': len(alive_members),
            'dead': len(self.party) - len(alive_members),
            'avg_health': sum(m.health for m in alive_members) / len(alive_members)
                         if alive_members else 0,
            'sick_count': len([m for m in alive_members if m.illness]),
        }


class StatusIndicator:
    """Quick status indicator for individual members."""
    
    def __init__(self, size: int = 16):
        """Initialize status indicator.
        
        Args:
            size: Indicator size
        """
        self.size = size
        self.status = 'healthy'  # healthy, injured, sick, critical
    
    def update_status(self, health: int, has_illness: bool):
        """Update status.
        
        Args:
            health: Health percentage
            has_illness: Whether member is ill
        """
        if health <= 0:
            self.status = 'dead'
        elif has_illness or health < 25:
            self.status = 'critical'
        elif health < 50:
            self.status = 'injured'
        else:
            self.status = 'healthy'
    
    def draw(self, surface: pygame.Surface, x: int, y: int):
        """Draw indicator.
        
        Args:
            surface: Surface to draw on
            x: X position
            y: Y position
        """
        color_map = {
            'healthy': COLORS['green'],
            'injured': COLORS['yellow'],
            'sick': COLORS['red'],
            'critical': COLORS['red'],
            'dead': COLORS['black'],
        }
        
        color = color_map[self.status]
        pygame.draw.circle(surface, color, (x, y), self.size // 2)
        pygame.draw.circle(surface, COLORS['white'], (x, y), self.size // 2, 1)


class PartyRoster:
    """Detailed party roster view."""
    
    def __init__(self, x: int, y: int, width: int = 400, height: int = 300):
        """Initialize party roster.
        
        Args:
            x: X position
            y: Y position
            width: Roster width
            height: Roster height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.party = []
        self.scroll_offset = 0
        self.row_height = 40
    
    def set_party(self, party: List[PartyMember]):
        """Set party roster.
        
        Args:
            party: List of party members
        """
        self.party = party
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw roster.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        # Draw panel
        pygame.draw.rect(surface, COLORS['black'], self.rect)
        pygame.draw.rect(surface, COLORS['white'], self.rect, 2)
        
        # Draw header
        renderer.draw_text("Party Roster", self.x + 10, self.y + 8,
                         COLORS['light_green'], 'small')
        
        # Draw members
        y = self.y + 30
        for i, member in enumerate(self.party):
            if y > self.y + self.height - self.row_height:
                break
            
            # Draw row background
            row_rect = pygame.Rect(self.x, y, self.width, self.row_height)
            if i % 2 == 0:
                pygame.draw.rect(surface, COLORS['gray'], row_rect)
            
            # Draw member info
            status = "●" if member.is_alive else "✗"
            status_color = COLORS['green'] if member.is_alive else COLORS['red']
            
            renderer.draw_text(f"{status} {member.name}", self.x + 10, y + 5,
                             status_color, 'small')
            renderer.draw_text(f"Health: {member.health}%", self.x + 150, y + 5,
                             COLORS['yellow'], 'small')
            
            if member.illness:
                renderer.draw_text(f"Illness: {member.illness}", self.x + 10, y + 20,
                                 COLORS['red'], 'small')
            
            y += self.row_height
