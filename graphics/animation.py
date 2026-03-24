"""
Animation system for sprite movement and transitions
"""

import pygame
from enum import Enum
from typing import List, Callable, Optional


class AnimationType(Enum):
    """Types of animations."""
    LOOP = "loop"
    ONCE = "once"
    BOUNCE = "bounce"
    REVERSE = "reverse"


class Keyframe:
    """Single keyframe in animation."""
    
    def __init__(self, frame_index: int, duration: float):
        """Initialize keyframe.
        
        Args:
            frame_index: Index of frame in sprite sheet
            duration: Duration in seconds
        """
        self.frame_index = frame_index
        self.duration = duration


class Animation:
    """Defines animation sequence."""
    
    def __init__(self, name: str, keyframes: List[Keyframe], 
                 animation_type: AnimationType = AnimationType.LOOP):
        """Initialize animation.
        
        Args:
            name: Animation identifier
            keyframes: List of keyframes
            animation_type: How animation loops
        """
        self.name = name
        self.keyframes = keyframes
        self.animation_type = animation_type
        self.total_duration = sum(kf.duration for kf in keyframes)
    
    def get_frame_at_time(self, time: float) -> int:
        """Get frame index at given time.
        
        Args:
            time: Time in seconds
            
        Returns:
            Frame index
        """
        if not self.keyframes:
            return 0
        
        # Handle animation type
        if self.animation_type == AnimationType.ONCE:
            if time >= self.total_duration:
                return self.keyframes[-1].frame_index
            current_time = time
        else:
            # Normalize time to animation duration
            current_time = time % self.total_duration
        
        # Find current frame
        elapsed = 0
        for keyframe in self.keyframes:
            elapsed += keyframe.duration
            if current_time <= elapsed:
                return keyframe.frame_index
        
        return self.keyframes[-1].frame_index
    
    def is_complete(self, time: float) -> bool:
        """Check if animation is complete."""
        if self.animation_type == AnimationType.ONCE:
            return time >= self.total_duration
        return False


class AnimationController:
    """Controls animation playback for sprites."""
    
    def __init__(self):
        """Initialize animation controller."""
        self.animations = {}
        self.current_animation = None
        self.animation_time = 0.0
        self.is_playing = False
        self.on_complete = None
    
    def add_animation(self, animation: Animation):
        """Add animation to controller.
        
        Args:
            animation: Animation to add
        """
        self.animations[animation.name] = animation
    
    def play(self, animation_name: str, restart: bool = True):
        """Start playing animation.
        
        Args:
            animation_name: Name of animation
            restart: Whether to restart if already playing
        """
        if animation_name not in self.animations:
            raise ValueError(f"Animation '{animation_name}' not found")
        
        if animation_name == self.current_animation and not restart:
            return
        
        self.current_animation = animation_name
        if restart:
            self.animation_time = 0.0
        self.is_playing = True
    
    def stop(self):
        """Stop animation."""
        self.is_playing = False
    
    def pause(self):
        """Pause animation."""
        self.is_playing = False
    
    def resume(self):
        """Resume animation."""
        if self.current_animation:
            self.is_playing = True
    
    def update(self, delta_time: float):
        """Update animation.
        
        Args:
            delta_time: Time since last frame in seconds
        """
        if not self.is_playing or not self.current_animation:
            return
        
        animation = self.animations[self.current_animation]
        self.animation_time += delta_time
        
        if animation.is_complete(self.animation_time):
            self.is_playing = False
            if self.on_complete:
                self.on_complete(self.current_animation)
    
    def get_current_frame(self) -> int:
        """Get current frame index.
        
        Returns:
            Current frame index or 0 if no animation
        """
        if not self.current_animation:
            return 0
        
        animation = self.animations[self.current_animation]
        return animation.get_frame_at_time(self.animation_time)
    
    def get_animation_progress(self) -> float:
        """Get animation progress 0-1.
        
        Returns:
            Progress value
        """
        if not self.current_animation:
            return 0.0
        
        animation = self.animations[self.current_animation]
        if animation.total_duration == 0:
            return 0.0
        
        progress = self.animation_time / animation.total_duration
        return min(progress, 1.0)


class AnimatedSprite(pygame.sprite.Sprite):
    """Sprite with animation support."""
    
    def __init__(self, x: float, y: float, width: int, height: int):
        """Initialize animated sprite.
        
        Args:
            x: X position
            y: Y position
            width: Sprite width
            height: Sprite height
        """
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.controller = AnimationController()
        self.frames = []
    
    def add_frame(self, frame: pygame.Surface):
        """Add animation frame.
        
        Args:
            frame: Frame surface
        """
        self.frames.append(frame)
    
    def add_animation(self, animation: Animation):
        """Add animation.
        
        Args:
            animation: Animation to add
        """
        self.controller.add_animation(animation)
    
    def play_animation(self, animation_name: str):
        """Play animation.
        
        Args:
            animation_name: Animation name
        """
        self.controller.play(animation_name)
    
    def update(self, delta_time: float):
        """Update sprite.
        
        Args:
            delta_time: Time since last frame
        """
        self.controller.update(delta_time)
        
        # Update image to current frame
        if self.frames and self.controller.current_animation:
            frame_index = self.controller.get_current_frame()
            if 0 <= frame_index < len(self.frames):
                self.image = self.frames[frame_index]
        
        self.rect.topleft = (self.x, self.y)


class TransitionAnimation:
    """Smooth transition between values."""
    
    def __init__(self, start_value: float, end_value: float, 
                 duration: float, easing_func: Optional[Callable] = None):
        """Initialize transition.
        
        Args:
            start_value: Starting value
            end_value: Ending value
            duration: Transition duration in seconds
            easing_func: Optional easing function
        """
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.elapsed = 0.0
        self.easing_func = easing_func or self._linear_easing
    
    def _linear_easing(self, progress: float) -> float:
        """Linear easing."""
        return progress
    
    def _ease_in_out_cubic(self, progress: float) -> float:
        """Ease in-out cubic."""
        if progress < 0.5:
            return 4 * progress * progress * progress
        return 1 - pow(-2 * progress + 2, 3) / 2
    
    def _ease_out_quad(self, progress: float) -> float:
        """Ease out quadratic."""
        return 1 - (1 - progress) * (1 - progress)
    
    def update(self, delta_time: float):
        """Update transition.
        
        Args:
            delta_time: Time since last frame
        """
        self.elapsed += delta_time
    
    def get_value(self) -> float:
        """Get current value.
        
        Returns:
            Current interpolated value
        """
        if self.duration == 0:
            return self.end_value
        
        progress = min(self.elapsed / self.duration, 1.0)
        eased_progress = self.easing_func(progress)
        
        return self.start_value + (self.end_value - self.start_value) * eased_progress
    
    def is_complete(self) -> bool:
        """Check if transition is complete."""
        return self.elapsed >= self.duration


class MovementAnimation:
    """Smooth movement animation."""
    
    def __init__(self, sprite: pygame.sprite.Sprite, 
                 target_x: float, target_y: float, 
                 duration: float):
        """Initialize movement animation.
        
        Args:
            sprite: Sprite to animate
            target_x: Target X position
            target_y: Target Y position
            duration: Duration in seconds
        """
        self.sprite = sprite
        self.start_x = sprite.rect.x
        self.start_y = sprite.rect.y
        self.target_x = target_x
        self.target_y = target_y
        self.x_transition = TransitionAnimation(self.start_x, target_x, duration)
        self.y_transition = TransitionAnimation(self.start_y, target_y, duration)
    
    def update(self, delta_time: float):
        """Update movement.
        
        Args:
            delta_time: Time since last frame
        """
        self.x_transition.update(delta_time)
        self.y_transition.update(delta_time)
        
        self.sprite.rect.x = int(self.x_transition.get_value())
        self.sprite.rect.y = int(self.y_transition.get_value())
    
    def is_complete(self) -> bool:
        """Check if movement is complete."""
        return self.x_transition.is_complete() and self.y_transition.is_complete()


class AnimationQueue:
    """Queue animations and play sequentially."""
    
    def __init__(self):
        """Initialize animation queue."""
        self.queue = []
        self.current_animation = None
    
    def enqueue(self, animation_name: str, controller: AnimationController):
        """Add animation to queue.
        
        Args:
            animation_name: Animation name
            controller: Animation controller
        """
        self.queue.append((animation_name, controller))
    
    def play_next(self):
        """Play next animation in queue."""
        if not self.queue:
            self.current_animation = None
            return
        
        animation_name, controller = self.queue.pop(0)
        controller.play(animation_name)
        self.current_animation = (animation_name, controller)
    
    def update(self):
        """Update queue."""
        if self.current_animation:
            animation_name, controller = self.current_animation
            if not controller.is_playing:
                self.play_next()
