"""
Trading post interactions with buying/selling mechanics
"""

import pygame
from enum import Enum
from typing import List, Callable, Optional, Tuple
from config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS


class ItemType(Enum):
    """Types of tradeable items."""
    FOOD = "food"
    AMMUNITION = "ammunition"
    MEDICINE = "medicine"
    SPARE_PARTS = "spare_parts"
    SUPPLIES = "supplies"


class TradeItem:
    """Item available for trade."""
    
    def __init__(self, item_id: str, name: str, item_type: ItemType, 
                 quantity: int, price: int, description: str = ""):
        """Initialize trade item.
        
        Args:
            item_id: Unique item ID
            name: Item name
            item_type: Type of item
            quantity: Available quantity
            price: Price per unit
            description: Item description
        """
        self.item_id = item_id
        self.name = name
        self.item_type = item_type
        self.quantity = quantity
        self.price = price
        self.description = description
    
    def is_available(self) -> bool:
        """Check if item is available.
        
        Returns:
            True if available
        """
        return self.quantity > 0


class TradingPost:
    """Trading post with inventory."""
    
    def __init__(self, name: str, location: str):
        """Initialize trading post.
        
        Args:
            name: Post name
            location: Location name
        """
        self.name = name
        self.location = location
        self.inventory = []
        self._init_inventory()
    
    def _init_inventory(self):
        """Initialize inventory."""
        # Standard trading post inventory
        self.inventory = [
            TradeItem("food_1", "Dried Meat", ItemType.FOOD, 500, 2, "Preserved meat strips"),
            TradeItem("food_2", "Hardtack", ItemType.FOOD, 300, 1, "Hard biscuits"),
            TradeItem("ammo_1", "Rifle Ammunition", ItemType.AMMUNITION, 200, 5, ".50 caliber rounds"),
            TradeItem("ammo_2", "Powder & Lead", ItemType.AMMUNITION, 150, 3, "For hand loading"),
            TradeItem("meds_1", "Laudanum", ItemType.MEDICINE, 50, 10, "Pain relief tonic"),
            TradeItem("meds_2", "Quinine", ItemType.MEDICINE, 40, 15, "Fever treatment"),
            TradeItem("parts_1", "Wagon Wheel", ItemType.SPARE_PARTS, 10, 50, "Replacement wheel"),
            TradeItem("parts_2", "Axle", ItemType.SPARE_PARTS, 8, 75, "Wagon axle"),
            TradeItem("supplies_1", "Rope", ItemType.SUPPLIES, 50, 2, "100 feet of rope"),
            TradeItem("supplies_2", "Canvas", ItemType.SUPPLIES, 30, 5, "Wagon cover material"),
        ]
    
    def get_inventory(self) -> List[TradeItem]:
        """Get available inventory.
        
        Returns:
            List of available items
        """
        return [item for item in self.inventory if item.is_available()]
    
    def sell_item(self, item_id: str, quantity: int) -> Tuple[bool, int]:
        """Sell item to player.
        
        Args:
            item_id: Item to sell
            quantity: Quantity to sell
            
        Returns:
            (Success, Total price)
        """
        item = next((i for i in self.inventory if i.item_id == item_id), None)
        if not item or item.quantity < quantity:
            return False, 0
        
        item.quantity -= quantity
        return True, item.price * quantity
    
    def buy_item(self, item_id: str, quantity: int, price_per_unit: int = None):
        """Buy item from player.
        
        Args:
            item_id: Item type to buy
            quantity: Quantity to buy
            price_per_unit: Price per unit (optional override)
        """
        # Find similar item or create new stack
        item = next((i for i in self.inventory if i.item_id == item_id), None)
        if item:
            item.quantity += quantity
        else:
            # Simplified - would need item type matching
            pass


class TradeTransaction:
    """Record of a trade transaction."""
    
    def __init__(self, transaction_type: str, items: List[Tuple[str, int, int]]):
        """Initialize transaction.
        
        Args:
            transaction_type: 'buy' or 'sell'
            items: List of (item_name, quantity, price)
        """
        self.transaction_type = transaction_type
        self.items = items
        self.total_price = sum(price for _, _, price in items)
    
    def get_summary(self) -> str:
        """Get transaction summary.
        
        Returns:
            Summary text
        """
        if self.transaction_type == 'buy':
            return f"Purchased {len(self.items)} items for ${self.total_price}"
        else:
            return f"Sold {len(self.items)} items for ${self.total_price}"


class TradingScreen:
    """Visual trading screen."""
    
    def __init__(self, trading_post: TradingPost):
        """Initialize trading screen.
        
        Args:
            trading_post: Trading post instance
        """
        self.trading_post = trading_post
        self.player_money = 1600
        self.player_inventory = {
            'food': 800,
            'ammunition': 100,
            'medicine': 20,
            'spare_parts': 10,
        }
        
        self.selected_tab = 'buy'  # buy or sell
        self.selected_item_index = 0
        self.transaction_history = []
    
    def buy_item(self, item_id: str, quantity: int) -> bool:
        """Buy item from post.
        
        Args:
            item_id: Item to buy
            quantity: Quantity
            
        Returns:
            True if successful
        """
        item = next((i for i in self.trading_post.inventory if i.item_id == item_id), None)
        if not item:
            return False
        
        total_cost = item.price * quantity
        if self.player_money < total_cost:
            return False
        
        success, cost = self.trading_post.sell_item(item_id, quantity)
        if success:
            self.player_money -= cost
            # Add to player inventory
            if item.item_type == ItemType.FOOD:
                self.player_inventory['food'] += quantity
            elif item.item_type == ItemType.AMMUNITION:
                self.player_inventory['ammunition'] += quantity
            elif item.item_type == ItemType.MEDICINE:
                self.player_inventory['medicine'] += quantity
            elif item.item_type == ItemType.SPARE_PARTS:
                self.player_inventory['spare_parts'] += quantity
            
            self.transaction_history.append(
                TradeTransaction('buy', [(item.name, quantity, cost)])
            )
            return True
        
        return False
    
    def sell_item(self, item_type: str, quantity: int) -> bool:
        """Sell item to post.
        
        Args:
            item_type: Type of item to sell
            quantity: Quantity to sell
            
        Returns:
            True if successful
        """
        if item_type not in self.player_inventory:
            return False
        
        if self.player_inventory[item_type] < quantity:
            return False
        
        # Get price (simplified - half of buy price)
        item = next((i for i in self.trading_post.inventory 
                    if i.item_type.value == item_type), None)
        
        if not item:
            return False
        
        sell_price = int(item.price * 0.5)
        total_money = sell_price * quantity
        
        self.player_inventory[item_type] -= quantity
        self.player_money += total_money
        
        self.transaction_history.append(
            TradeTransaction('sell', [(item.name, quantity, total_money)])
        )
        
        return True
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw trading screen.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        surface.fill(COLORS['black'])
        
        # Draw post name
        renderer.draw_text(f"{self.trading_post.name} - {self.trading_post.location}",
                         20, 10, COLORS['light_green'], 'large')
        
        # Draw player money
        renderer.draw_text(f"Your Money: ${self.player_money}",
                         20, 40, COLORS['yellow'], 'small')
        
        # Draw tabs
        buy_color = COLORS['light_cyan'] if self.selected_tab == 'buy' else COLORS['white']
        sell_color = COLORS['light_cyan'] if self.selected_tab == 'sell' else COLORS['white']
        
        renderer.draw_text("BUY", 50, 80, buy_color, 'small')
        renderer.draw_text("SELL", 150, 80, sell_color, 'small')
        
        # Draw inventory section
        if self.selected_tab == 'buy':
            self._draw_buy_section(surface, renderer)
        else:
            self._draw_sell_section(surface, renderer)
    
    def _draw_buy_section(self, surface: pygame.Surface, renderer):
        """Draw buy section."""
        inventory = self.trading_post.get_inventory()
        
        y = 120
        for i, item in enumerate(inventory):
            # Highlight selected
            if i == self.selected_item_index:
                pygame.draw.rect(surface, COLORS['gray'], 
                               (20, y - 5, WINDOW_WIDTH - 40, 25))
            
            renderer.draw_text(f"{item.name}", 30, y, COLORS['white'], 'small')
            renderer.draw_text(f"${item.price}", WINDOW_WIDTH - 200, y, 
                             COLORS['yellow'], 'small')
            renderer.draw_text(f"Qty: {item.quantity}", WINDOW_WIDTH - 100, y,
                             COLORS['light_green'], 'small')
            
            y += 30
    
    def _draw_sell_section(self, surface: pygame.Surface, renderer):
        """Draw sell section."""
        y = 120
        
        items_to_sell = [
            ('Food', self.player_inventory['food']),
            ('Ammunition', self.player_inventory['ammunition']),
            ('Medicine', self.player_inventory['medicine']),
            ('Spare Parts', self.player_inventory['spare_parts']),
        ]
        
        for i, (name, quantity) in enumerate(items_to_sell):
            if i == self.selected_item_index:
                pygame.draw.rect(surface, COLORS['gray'],
                               (20, y - 5, WINDOW_WIDTH - 40, 25))
            
            renderer.draw_text(f"{name}", 30, y, COLORS['white'], 'small')
            renderer.draw_text(f"You have: {quantity}", WINDOW_WIDTH - 200, y,
                             COLORS['light_green'], 'small')
            
            y += 30


class TradeUI:
    """Interactive trade UI."""
    
    def __init__(self, trading_post: TradingPost):
        """Initialize trade UI.
        
        Args:
            trading_post: Trading post
        """
        self.screen = TradingScreen(trading_post)
        self.on_complete = None
    
    def handle_input(self, event: pygame.event.EventType):
        """Handle input.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.screen.selected_item_index = max(0, 
                    self.screen.selected_item_index - 1)
            
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                max_items = 10 if self.screen.selected_tab == 'buy' else 4
                self.screen.selected_item_index = min(max_items - 1,
                    self.screen.selected_item_index + 1)
            
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.screen.selected_tab = 'sell'
            
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.screen.selected_tab = 'buy'
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._confirm_selection()
            
            elif event.key == pygame.K_ESCAPE:
                if self.on_complete:
                    self.on_complete()
    
    def _confirm_selection(self):
        """Confirm selection action."""
        # Would implement quantity selection dialog
        pass
    
    def draw(self, surface: pygame.Surface, renderer):
        """Draw UI.
        
        Args:
            surface: Surface to draw on
            renderer: Renderer for text
        """
        self.screen.draw(surface, renderer)


class LocationTradeSystem:
    """Trading system for trail locations."""
    
    LOCATIONS = {
        'Fort Laramie': TradingPost('Fort Laramie Trading Post', 'Fort Laramie'),
        'Fort Bridger': TradingPost('Fort Bridger Trading Post', 'Fort Bridger'),
        'Fort Hall': TradingPost('Fort Hall Trading Post', 'Fort Hall'),
    }
    
    @classmethod
    def get_trading_post(cls, location_name: str) -> Optional[TradingPost]:
        """Get trading post for location.
        
        Args:
            location_name: Location name
            
        Returns:
            TradingPost or None
        """
        return cls.LOCATIONS.get(location_name)
    
    @classmethod
    def has_trading_post(cls, location_name: str) -> bool:
        """Check if location has trading post.
        
        Args:
            location_name: Location name
            
        Returns:
            True if has trading post
        """
        return location_name in cls.LOCATIONS
