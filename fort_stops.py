"""
Fort stop mechanics with rest, resupply, and information gathering
"""

import pygame
from enum import Enum
from typing import List, Optional, Callable
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS


class FortType(Enum):
    """Types of forts."""
    TRADING_POST = "trading_post"
    MILITARY_FORT = "military_fort"
    SUPPLY_STATION = "supply_station"


class FortInformation:
    """Information a fort can provide."""
    
    def __init__(self):
        """Initialize fort information."""
        self.news = []
        self.warnings = []
        self.advice = []
        self.rumors = []
    
    def add_news(self, text: str):
        """Add news item.
        
        Args:
            text: News text
        """
        self.news.append(text)
    
    def add_warning(self, text: str):
        """Add warning.
        
        Args:
            text: Warning text
        """
        self.warnings.append(text)
    
    def add_advice(self, text: str):
        """Add advice.
        
        Args:
            text: Advice text
        """
        self.advice.append(text)
    
    def add_rumor(self, text: str):
        """Add rumor.
        
        Args:
            text: Rumor text
        """
        self.rumors.append(text)


class Fort:
    """A fort on the trail."""
    
    def __init__(self, name: str, location_name: str, fort_type: FortType):
        """Initialize fort.
        
        Args:
            name: Fort name
            location_name: Trail location name
            fort_type: Type of fort
        """
        self.name = name
        self.location_name = location_name
        self.fort_type = fort_type
        self.information = FortInformation()
        self.rest_bonus = 25  # Health restoration per day of rest
        self.supply_prices_multiplier = 1.0  # 1.0 = normal, 1.5 = expensive
        
        self._init_information()
    
    def _init_information(self):
        """Initialize fort information."""
        fort_info = {
            'Fort Laramie': {
                'news': [
                    'Many traders have passed through recently.',
                    'Reports of Indian hunting parties in the area.',
                ],
                'warnings': [
                    'Winter approaches. Stock up on supplies!',
                    'Rivers ahead may be dangerous this time of year.',
                ],
                'advice': [
                    'Rest well before the mountain passes.',
                    'Consider buying extra ammunition for hunting.',
                ],
            },
            'Fort Bridger': {
                'news': [
                    'The mountain pass is clear for travel.',
                    'Several wagon trains passed yesterday.',
                ],
                'warnings': [
                    'Bandits reported near the pass.',
                    'Water is scarce on the next stretch.',
                ],
                'advice': [
                    'Fill your water barrels here.',
                    'The shortcut through the pass is faster but riskier.',
                ],
            },
            'Fort Hall': {
                'news': [
                    'The fur trading season is at its peak.',
                    'Native traders are friendly and fair.',
                ],
                'warnings': [
                    'The Snake River crossing can be treacherous.',
                    'Wildlife is abundant but dangerous.',
                ],
                'advice': [
                    'Hunt well here before the desert.',
                    'Stock up on medicine for the final stretch.',
                ],
            },
        }
        
        if self.location_name in fort_info:
            info = fort_info[self.location_name]
            for news in info.get('news', []):
                self.information.add_news(news)
            for warning in info.get('warnings', []):
                self.information.add_warning(warning)
            for advice in info.get('advice', []):
                self.information.add_advice(advice)


class FortStop:
    """A stop at a fort."""
    
    def __init__(self, fort: Fort):
        """Initialize fort stop.
        
        Args:
            fort: Fort instance
        """
        self.fort = fort
        self.rest_days = 0
        self.is_active = True
    
    def rest(self, days: int = 1) -> int:
        """Rest at fort.
        
        Args:
            days: Number of days to rest
            
        Returns:
            Health restoration amount
        """
        self.rest_days += days
        return self.fort.rest_bonus * days
    
    def get_fort_info(self) -> FortInformation:
        """Get fort information.
        
        Returns:
            Fort information
        """
        return self.fort.information


class FortStopScreen:
    """Visual interface for fort stop."""
    
    def __init__(self, fort: Fort):
        """Initialize fort stop screen.
        
        Args:
            fort: Fort instance
        """
        self.fort = fort
        self.current_menu = 'main'  # main, rest, trade, info, news
        self.selected_option = 0
        self.rest_days_selected = 0
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw screen.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        surface.fill(COLORS['black'])
        
        # Draw fort name and location
        renderer.draw_text(f"{self.fort.name} - {self.fort.location_name}",
                         20, 20, COLORS['light_green'], 'large')
        
        if self.current_menu == 'main':
            self._draw_main_menu(surface, renderer)
        elif self.current_menu == 'rest':
            self._draw_rest_menu(surface, renderer)
        elif self.current_menu == 'info':
            self._draw_info_menu(surface, renderer)
    
    def _draw_main_menu(self, surface: pygame.Surface, renderer):
        """Draw main menu."""
        options = ['Rest', 'Trade', 'Gather Information', 'Continue']
        
        y = 100
        for i, option in enumerate(options):
            color = COLORS['light_cyan'] if i == self.selected_option else COLORS['white']
            renderer.draw_text(option, 50, y, color, 'small')
            y += 40
    
    def _draw_rest_menu(self, surface: pygame.Surface, renderer):
        """Draw rest menu."""
        renderer.draw_text("How many days to rest?", 50, 100, COLORS['yellow'], 'small')
        
        for days in range(1, 8):
            color = COLORS['light_cyan'] if days - 1 == self.selected_option else COLORS['white']
            renderer.draw_text(f"{days} day(s)", 50, 140 + (days - 1) * 30, color, 'small')
    
    def _draw_info_menu(self, surface: pygame.Surface, renderer):
        """Draw information menu."""
        info = self.fort.information
        
        y = 100
        
        if info.news:
            renderer.draw_text("News:", 50, y, COLORS['light_cyan'], 'small')
            y += 25
            for news in info.news[:2]:
                renderer.draw_text(f"• {news}", 70, y, COLORS['white'], 'small')
                y += 25
        
        if info.warnings:
            renderer.draw_text("Warnings:", 50, y, COLORS['light_red'], 'small')
            y += 25
            for warning in info.warnings[:2]:
                renderer.draw_text(f"⚠ {warning}", 70, y, COLORS['yellow'], 'small')
                y += 25
        
        if info.advice:
            renderer.draw_text("Advice:", 50, y, COLORS['light_green'], 'small')
            y += 25
            for advice in info.advice[:2]:
                renderer.draw_text(f"→ {advice}", 70, y, COLORS['white'], 'small')
                y += 25


class FortInteraction:
    """Handles fort stop interactions."""
    
    def __init__(self, fort: Fort):
        """Initialize fort interaction.
        
        Args:
            fort: Fort instance
        """
        self.fort = fort
        self.screen = FortStopScreen(fort)
        self.on_rest = None
        self.on_trade = None
        self.on_continue = None
    
    def handle_input(self, event: pygame.event.EventType):
        """Handle input.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if self.screen.current_menu == 'main':
                    self.screen.selected_option = max(0, self.screen.selected_option - 1)
                else:
                    self.screen.selected_option = max(0, self.screen.selected_option - 1)
            
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.screen.current_menu == 'main':
                    self.screen.selected_option = min(3, self.screen.selected_option + 1)
                else:
                    self.screen.selected_option = min(6, self.screen.selected_option + 1)
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._confirm_selection()
            
            elif event.key == pygame.K_ESCAPE:
                if self.screen.current_menu != 'main':
                    self.screen.current_menu = 'main'
    
    def _confirm_selection(self):
        """Confirm selection."""
        if self.screen.current_menu == 'main':
            options = ['Rest', 'Trade', 'Gather Information', 'Continue']
            selected = options[self.screen.selected_option]
            
            if selected == 'Rest':
                self.screen.current_menu = 'rest'
                self.screen.selected_option = 0
            elif selected == 'Trade':
                if self.on_trade:
                    self.on_trade()
            elif selected == 'Gather Information':
                self.screen.current_menu = 'info'
                self.screen.selected_option = 0
            elif selected == 'Continue':
                if self.on_continue:
                    self.on_continue()
        
        elif self.screen.current_menu == 'rest':
            days = self.screen.selected_option + 1
            if self.on_rest:
                self.on_rest(days)
            self.screen.current_menu = 'main'
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw interaction.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        self.screen.draw(surface, renderer)


class FortSystem:
    """System managing all fort interactions."""
    
    FORTS = {
        'Fort Laramie': Fort('Fort Laramie', 'Fort Laramie', FortType.TRADING_POST),
        'Fort Bridger': Fort('Fort Bridger', 'Fort Bridger', FortType.TRADING_POST),
        'Fort Hall': Fort('Fort Hall', 'Fort Hall', FortType.TRADING_POST),
    }
    
    @classmethod
    def get_fort(cls, location_name: str) -> Optional[Fort]:
        """Get fort for location.
        
        Args:
            location_name: Location name
            
        Returns:
            Fort instance or None
        """
        return cls.FORTS.get(location_name)
    
    @classmethod
    def has_fort(cls, location_name: str) -> bool:
        """Check if location has a fort.
        
        Args:
            location_name: Location name
            
        Returns:
            True if has fort
        """
        return location_name in cls.FORTS
    
    @classmethod
    def create_interaction(cls, location_name: str) -> Optional[FortInteraction]:
        """Create fort interaction for location.
        
        Args:
            location_name: Location name
            
        Returns:
            FortInteraction or None
        """
        fort = cls.get_fort(location_name)
        if fort:
            return FortInteraction(fort)
        return None


class LocationStop:
    """Stop at any location."""
    
    def __init__(self, location_name: str):
        """Initialize location stop.
        
        Args:
            location_name: Location name
        """
        self.location_name = location_name
        self.has_fort = FortSystem.has_fort(location_name)
        self.fort_interaction = None
        
        if self.has_fort:
            self.fort_interaction = FortSystem.create_interaction(location_name)
    
    def can_rest(self) -> bool:
        """Check if can rest at location.
        
        Returns:
            True if can rest
        """
        return self.has_fort
    
    def can_trade(self) -> bool:
        """Check if can trade at location.
        
        Returns:
            True if can trade
        """
        return self.has_fort
