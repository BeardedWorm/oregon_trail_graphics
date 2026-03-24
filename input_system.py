"""
Mouse and keyboard input system for menus and gameplay
"""

import pygame
from enum import Enum
from typing import Callable, Optional, List, Tuple
from graphics.ui import MenuItem


class InputMode(Enum):
    """Input mode types."""
    MENU_NAVIGATION = "menu"
    GAMEPLAY = "gameplay"
    TEXT_INPUT = "text_input"
    DIALOG = "dialog"


class KeyBinding:
    """Keyboard binding."""
    
    def __init__(self, key: int, callback: Callable, name: str = ""):
        """Initialize key binding.
        
        Args:
            key: Pygame key constant
            callback: Function to call
            name: Binding name for display
        """
        self.key = key
        self.callback = callback
        self.name = name or pygame.key.name(key)


class MouseButton:
    """Clickable button region."""
    
    def __init__(self, rect: pygame.Rect, callback: Callable, 
                 hover_callback: Optional[Callable] = None,
                 hover_exit_callback: Optional[Callable] = None):
        """Initialize mouse button.
        
        Args:
            rect: Clickable rectangle
            callback: Function to call on click
            hover_callback: Function to call on hover enter
            hover_exit_callback: Function to call on hover exit
        """
        self.rect = rect
        self.callback = callback
        self.hover_callback = hover_callback
        self.hover_exit_callback = hover_exit_callback
        self.is_hovered = False
    
    def check_collision(self, pos: Tuple[int, int]) -> bool:
        """Check if position collides with button.
        
        Args:
            pos: Mouse position
            
        Returns:
            True if collision
        """
        return self.rect.collidepoint(pos)
    
    def on_click(self, pos: Tuple[int, int]):
        """Handle click on button.
        
        Args:
            pos: Click position
        """
        if self.check_collision(pos):
            self.callback(pos)
    
    def on_hover(self, pos: Tuple[int, int]):
        """Handle hover on button.
        
        Args:
            pos: Mouse position
        """
        colliding = self.check_collision(pos)
        
        if colliding and not self.is_hovered:
            self.is_hovered = True
            if self.hover_callback:
                self.hover_callback()
        elif not colliding and self.is_hovered:
            self.is_hovered = False
            if self.hover_exit_callback:
                self.hover_exit_callback()


class MenuInputHandler:
    """Handles input for menu navigation."""
    
    def __init__(self, menu):
        """Initialize menu input handler.
        
        Args:
            menu: Menu instance to control
        """
        self.menu = menu
        self.key_bindings = {
            pygame.K_UP: self._handle_up,
            pygame.K_w: self._handle_up,
            pygame.K_DOWN: self._handle_down,
            pygame.K_s: self._handle_down,
            pygame.K_RETURN: self._handle_select,
            pygame.K_SPACE: self._handle_select,
            pygame.K_LEFT: self._handle_left,
            pygame.K_a: self._handle_left,
            pygame.K_RIGHT: self._handle_right,
            pygame.K_d: self._handle_right,
        }
    
    def _handle_up(self):
        """Move selection up."""
        if hasattr(self.menu, 'select_previous'):
            self.menu.select_previous()
    
    def _handle_down(self):
        """Move selection down."""
        if hasattr(self.menu, 'select_next'):
            self.menu.select_next()
    
    def _handle_left(self):
        """Move selection left."""
        if hasattr(self.menu, 'select_left'):
            self.menu.select_left()
    
    def _handle_right(self):
        """Move selection right."""
        if hasattr(self.menu, 'select_right'):
            self.menu.select_right()
    
    def _handle_select(self):
        """Select current menu item."""
        if hasattr(self.menu, 'activate_selection'):
            self.menu.activate_selection()
    
    def process_event(self, event: pygame.event.EventType):
        """Process input event.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_bindings:
                self.key_bindings[event.key]()


class GameplayInputHandler:
    """Handles input for gameplay."""
    
    def __init__(self):
        """Initialize gameplay input handler."""
        self.key_callbacks = {}
        self.mouse_buttons = []
        self.key_states = {}
    
    def register_key(self, key: int, callback: Callable, name: str = ""):
        """Register key callback.
        
        Args:
            key: Pygame key constant
            callback: Function to call
            name: Binding name
        """
        self.key_callbacks[key] = KeyBinding(key, callback, name)
    
    def register_mouse_button(self, rect: pygame.Rect, callback: Callable,
                             hover_callback: Optional[Callable] = None,
                             hover_exit_callback: Optional[Callable] = None):
        """Register mouse button.
        
        Args:
            rect: Button rectangle
            callback: Click callback
            hover_callback: Hover enter callback
            hover_exit_callback: Hover exit callback
        """
        button = MouseButton(rect, callback, hover_callback, hover_exit_callback)
        self.mouse_buttons.append(button)
        return button
    
    def process_event(self, event: pygame.event.EventType):
        """Process input event.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            self.key_states[event.key] = True
            if event.key in self.key_callbacks:
                self.key_callbacks[event.key].callback()
        
        elif event.type == pygame.KEYUP:
            self.key_states[event.key] = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.mouse_buttons:
                button.on_click(event.pos)
        
        elif event.type == pygame.MOUSEMOTION:
            for button in self.mouse_buttons:
                button.on_hover(event.pos)
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if key is pressed.
        
        Args:
            key: Pygame key constant
            
        Returns:
            True if pressed
        """
        return self.key_states.get(key, False)
    
    def get_hovered_buttons(self) -> List[MouseButton]:
        """Get currently hovered buttons.
        
        Returns:
            List of hovered buttons
        """
        return [btn for btn in self.mouse_buttons if btn.is_hovered]
    
    def clear(self):
        """Clear all inputs."""
        self.key_callbacks.clear()
        self.mouse_buttons.clear()
        self.key_states.clear()


class DialogInputHandler:
    """Handles input for dialog boxes."""
    
    def __init__(self, on_confirm: Callable, on_cancel: Optional[Callable] = None):
        """Initialize dialog input handler.
        
        Args:
            on_confirm: Callback for confirm/yes
            on_cancel: Callback for cancel/no
        """
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.selected_option = 0  # 0=yes/confirm, 1=no/cancel
    
    def process_event(self, event: pygame.event.EventType):
        """Process input event.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.selected_option = 0
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected_option = 1
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._confirm()
            elif event.key == pygame.K_ESCAPE:
                self._cancel()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse clicks on buttons
            pass
    
    def _confirm(self):
        """Confirm selection."""
        if self.selected_option == 0:
            self.on_confirm()
        else:
            if self.on_cancel:
                self.on_cancel()
    
    def _cancel(self):
        """Cancel dialog."""
        if self.on_cancel:
            self.on_cancel()


class TextInputHandler:
    """Handles text input for forms."""
    
    def __init__(self, max_length: int = 20, allowed_chars: str = None):
        """Initialize text input handler.
        
        Args:
            max_length: Maximum input length
            allowed_chars: Allowed characters (None = all alphanumeric)
        """
        self.text = ""
        self.max_length = max_length
        self.allowed_chars = allowed_chars
        self.cursor_pos = 0
    
    def process_event(self, event: pygame.event.EventType) -> str:
        """Process input event.
        
        Args:
            event: Pygame event
            
        Returns:
            Current text
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
            
            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
            
            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos - 1)
            
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
            
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
            
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
            
            elif event.unicode and event.unicode.isprintable():
                if len(self.text) < self.max_length:
                    if self.allowed_chars is None or event.unicode in self.allowed_chars:
                        self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                        self.cursor_pos += 1
        
        return self.text
    
    def get_text(self) -> str:
        """Get entered text.
        
        Returns:
            Current text
        """
        return self.text
    
    def set_text(self, text: str):
        """Set text.
        
        Args:
            text: New text
        """
        self.text = text[:self.max_length]
        self.cursor_pos = len(self.text)
    
    def clear(self):
        """Clear text."""
        self.text = ""
        self.cursor_pos = 0


class InputManager:
    """Centralized input manager."""
    
    def __init__(self):
        """Initialize input manager."""
        self.mode = InputMode.MENU_NAVIGATION
        self.handlers = {
            InputMode.MENU_NAVIGATION: None,
            InputMode.GAMEPLAY: GameplayInputHandler(),
            InputMode.TEXT_INPUT: TextInputHandler(),
            InputMode.DIALOG: None,
        }
    
    def set_mode(self, mode: InputMode, handler: Optional[object] = None):
        """Set input mode.
        
        Args:
            mode: New input mode
            handler: Optional handler for this mode
        """
        self.mode = mode
        if handler is not None:
            self.handlers[mode] = handler
    
    def process_event(self, event: pygame.event.EventType):
        """Process input event.
        
        Args:
            event: Pygame event
        """
        handler = self.handlers.get(self.mode)
        if handler and hasattr(handler, 'process_event'):
            handler.process_event(event)
    
    def get_current_handler(self):
        """Get current input handler.
        
        Returns:
            Current handler
        """
        return self.handlers.get(self.mode)
