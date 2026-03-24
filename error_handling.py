"""
Edge case handling and error management
"""

import logging
from enum import Enum
from typing import Callable, Optional, Any
from functools import wraps


class ErrorLevel(Enum):
    """Error severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class GameException(Exception):
    """Base game exception."""
    
    def __init__(self, message: str, error_level: ErrorLevel = ErrorLevel.ERROR):
        """Initialize exception.
        
        Args:
            message: Error message
            error_level: Severity level
        """
        super().__init__(message)
        self.message = message
        self.error_level = error_level


class ResourceException(GameException):
    """Exception for resource-related errors."""
    pass


class PartyException(GameException):
    """Exception for party-related errors."""
    pass


class GameStateException(GameException):
    """Exception for game state errors."""
    pass


class ErrorHandler:
    """Centralized error handling."""
    
    def __init__(self):
        """Initialize error handler."""
        self.errors = []
        self.warnings = []
        self.recovery_actions = {}
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('game.log'),
                logging.StreamHandler(),
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error: Exception, error_level: ErrorLevel = ErrorLevel.ERROR,
                    recovery_action: Optional[Callable] = None):
        """Handle error.
        
        Args:
            error: Exception to handle
            error_level: Error level
            recovery_action: Optional recovery action
        """
        error_info = {
            'type': type(error).__name__,
            'message': str(error),
            'level': error_level.value,
        }
        
        self.errors.append(error_info)
        
        # Log error
        if error_level == ErrorLevel.CRITICAL:
            self.logger.critical(str(error))
        elif error_level == ErrorLevel.ERROR:
            self.logger.error(str(error))
        elif error_level == ErrorLevel.WARNING:
            self.logger.warning(str(error))
        else:
            self.logger.info(str(error))
        
        # Execute recovery action if provided
        if recovery_action:
            try:
                recovery_action()
            except Exception as recovery_error:
                self.logger.error(f"Recovery action failed: {recovery_error}")
    
    def handle_warning(self, message: str):
        """Handle warning.
        
        Args:
            message: Warning message
        """
        self.warnings.append(message)
        self.logger.warning(message)
    
    def register_recovery_action(self, error_type: type, action: Callable):
        """Register recovery action for error type.
        
        Args:
            error_type: Error type
            action: Recovery action callable
        """
        self.recovery_actions[error_type] = action
    
    def get_error_report(self) -> dict:
        """Get error report.
        
        Returns:
            Dictionary with error report
        """
        return {
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'errors': self.errors,
            'warnings': self.warnings,
        }


class EdgeCaseValidator:
    """Validates and handles edge cases."""
    
    @staticmethod
    def validate_party_members(party: list) -> bool:
        """Validate party members.
        
        Args:
            party: List of party members
            
        Returns:
            True if valid
        """
        if not party:
            raise PartyException("Party cannot be empty")
        
        if len(party) > 5:
            raise PartyException("Party size exceeds maximum")
        
        for member in party:
            if not hasattr(member, 'health') or member.health < 0:
                raise PartyException(f"Invalid member health: {member}")
        
        return True
    
    @staticmethod
    def validate_resources(resources: dict) -> bool:
        """Validate resources.
        
        Args:
            resources: Resource dictionary
            
        Returns:
            True if valid
        """
        required_keys = ['food', 'ammunition', 'medicine', 'spare_parts', 'money']
        
        for key in required_keys:
            if key not in resources:
                raise ResourceException(f"Missing resource: {key}")
            
            if resources[key] < 0:
                raise ResourceException(f"Negative resource value: {key}={resources[key]}")
        
        return True
    
    @staticmethod
    def validate_game_state(game_state) -> bool:
        """Validate game state.
        
        Args:
            game_state: Game state object
            
        Returns:
            True if valid
        """
        if not hasattr(game_state, 'party'):
            raise GameStateException("Missing party in game state")
        
        if not hasattr(game_state, 'resources'):
            raise GameStateException("Missing resources in game state")
        
        if game_state.current_day < 1 or game_state.current_day > 30:
            raise GameStateException(f"Invalid day: {game_state.current_day}")
        
        if game_state.distance_traveled < 0:
            raise GameStateException(f"Invalid distance: {game_state.distance_traveled}")
        
        return True


def handle_errors(error_handler: ErrorHandler):
    """Decorator for error handling.
    
    Args:
        error_handler: ErrorHandler instance
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except GameException as e:
                error_handler.handle_error(e, e.error_level)
                return None
            except Exception as e:
                error_handler.handle_error(e, ErrorLevel.ERROR)
                return None
        return wrapper
    return decorator


class SafeOperation:
    """Wrapper for safe operations with fallback."""
    
    def __init__(self, operation: Callable, fallback: Callable = None,
                 error_handler: Optional[ErrorHandler] = None):
        """Initialize safe operation.
        
        Args:
            operation: Operation to perform
            fallback: Fallback operation
            error_handler: Error handler
        """
        self.operation = operation
        self.fallback = fallback
        self.error_handler = error_handler or ErrorHandler()
    
    def execute(self, *args, **kwargs) -> Any:
        """Execute operation safely.
        
        Args:
            *args: Operation arguments
            **kwargs: Operation keyword arguments
            
        Returns:
            Operation result or fallback result
        """
        try:
            return self.operation(*args, **kwargs)
        except Exception as e:
            self.error_handler.handle_error(e)
            
            if self.fallback:
                try:
                    return self.fallback(*args, **kwargs)
                except Exception as fallback_error:
                    self.error_handler.handle_error(fallback_error, ErrorLevel.CRITICAL)
                    return None
            return None


class StateGuard:
    """Guards against invalid state transitions."""
    
    def __init__(self):
        """Initialize state guard."""
        self.valid_transitions = {}
        self.current_state = None
    
    def add_transition(self, from_state: str, to_state: str):
        """Add valid transition.
        
        Args:
            from_state: Starting state
            to_state: Ending state
        """
        if from_state not in self.valid_transitions:
            self.valid_transitions[from_state] = []
        self.valid_transitions[from_state].append(to_state)
    
    def can_transition(self, to_state: str) -> bool:
        """Check if transition is valid.
        
        Args:
            to_state: Target state
            
        Returns:
            True if transition is valid
        """
        if self.current_state is None:
            return True
        
        return to_state in self.valid_transitions.get(self.current_state, [])
    
    def transition(self, to_state: str) -> bool:
        """Transition to state.
        
        Args:
            to_state: Target state
            
        Returns:
            True if successful
        """
        if self.can_transition(to_state):
            self.current_state = to_state
            return True
        return False


class BoundaryChecker:
    """Checks for boundary violations."""
    
    @staticmethod
    def clamp_value(value: float, min_val: float, max_val: float) -> float:
        """Clamp value to range.
        
        Args:
            value: Value to clamp
            min_val: Minimum value
            max_val: Maximum value
            
        Returns:
            Clamped value
        """
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def check_boundary(value: float, boundary: float, 
                      on_exceeded: Optional[Callable] = None) -> bool:
        """Check if value exceeds boundary.
        
        Args:
            value: Value to check
            boundary: Boundary value
            on_exceeded: Callback if exceeded
            
        Returns:
            True if exceeded
        """
        exceeded = value > boundary
        if exceeded and on_exceeded:
            on_exceeded(value, boundary)
        return exceeded


class NullSafetyChecker:
    """Checks for null/None values safely."""
    
    @staticmethod
    def safe_get(obj: dict, key: str, default: Any = None) -> Any:
        """Safely get dictionary value.
        
        Args:
            obj: Dictionary object
            key: Key to get
            default: Default value
            
        Returns:
            Value or default
        """
        return obj.get(key, default) if obj else default
    
    @staticmethod
    def safe_access(obj: Any, attr: str, default: Any = None) -> Any:
        """Safely access object attribute.
        
        Args:
            obj: Object to access
            attr: Attribute name
            default: Default value
            
        Returns:
            Attribute value or default
        """
        return getattr(obj, attr, default) if obj else default
    
    @staticmethod
    def ensure_not_none(value: Any, name: str = "value") -> Any:
        """Ensure value is not None.
        
        Args:
            value: Value to check
            name: Value name for error message
            
        Returns:
            The value if not None
            
        Raises:
            GameException if None
        """
        if value is None:
            raise GameException(f"{name} cannot be None")
        return value


class RecoverySystem:
    """System for automatic recovery from errors."""
    
    def __init__(self):
        """Initialize recovery system."""
        self.recovery_points = {}
        self.auto_recovery_enabled = True
    
    def create_recovery_point(self, name: str, state: Any):
        """Create recovery point.
        
        Args:
            name: Point name
            state: State to save
        """
        self.recovery_points[name] = state
    
    def recover_from_point(self, name: str) -> Optional[Any]:
        """Recover from point.
        
        Args:
            name: Point name
            
        Returns:
            Recovered state or None
        """
        return self.recovery_points.get(name)
    
    def list_recovery_points(self) -> list:
        """List available recovery points.
        
        Returns:
            List of point names
        """
        return list(self.recovery_points.keys())
