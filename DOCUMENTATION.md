# Oregon Trail Graphical - Upgrade Documentation

## Overview

This is a complete graphical recreation of the 1985 Oregon Trail computer game using Python and Pygame. The game features authentic CGA/EGA 16-color pixel art graphics, complete with procedurally generated sprites, animations, weather effects, and full gameplay mechanics.

## Installation

### Requirements
- Python 3.8+
- Pygame 2.1+
- Windows/Mac/Linux

### Setup

1. **Clone or download the repository:**
```bash
git clone https://github.com/BeardedWorm/oregon_trail_graphics.git
cd oregon_trail_graphics
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the game:**
```bash
python main.py
```

## Project Structure

```
oregon_trail_graphics/
├── main.py                      # Game entry point
├── config.py                    # Central configuration
├── models.py                    # Game data structures
├── game_engine.py              # Core game engine
├── input_system.py             # Input handling
├── screens.py                  # Game screens
├── 
├── graphics/                   # Graphics system
│   ├── __init__.py
│   ├── renderer.py             # Rendering engine
│   ├── palette.py              # Color palette management
│   ├── sprites.py              # Sprite system
│   ├── animation.py            # Animation system
│   ├── ui.py                   # UI menus
│   ├── hud.py                  # Heads-up display
│   ├── ui_elements.py          # UI graphics (buttons, frames, icons)
│   ├── character_sprites.py    # Character sprite generation
│   ├── terrain_sprites.py      # Terrain and location sprites
│   ├── weather.py              # Weather effects and particles
│   └── screens/                # Screen displays
│       ├── main_menu_screen.py
│       ├── status_screens.py
│       ├── map_screen.py
│       └── events.py
│
├── hunting_game.py             # Hunting mini-game
├── event_animations.py         # Event visual sequences
├── resource_ui.py              # Resource management UI
├── party_tracking.py           # Party status tracking
├── trading_posts.py            # Trading system
├── fort_stops.py               # Fort mechanics
├── difficulty_settings.py      # Difficulty selection
├── persistence.py              # Save/load system
├── leaderboard.py              # High scores system
├── optimization.py             # Performance optimization
├── error_handling.py           # Error management
│
└── README.md                   # This file
```

## Key Features

### Graphics System
- **Color Palette**: 16-color CGA palette for authentic 1985 aesthetic
- **Procedural Sprites**: Dynamically generated character and terrain sprites
- **Animation System**: Keyframe-based animation with smooth transitions
- **Weather Effects**: Particle-based rain, snow, dust storms, lightning
- **UI Elements**: Procedurally generated buttons, frames, progress bars, icons

### Gameplay Systems
- **Game Engine**: State-based engine with game loop management
- **Input System**: Comprehensive keyboard and mouse handling
- **Party Management**: Track 5 party members with health, illness, and inventory
- **Resources**: Food, ammunition, medicine, spare parts, money
- **Trading Posts**: Buy/sell system at forts (Laramie, Bridger, Hall)
- **Fort Stops**: Rest, gather information, and resupply
- **Hunting Mini-Game**: Interactive hunting with targeting and scoring

### Game Mechanics
- **Difficulty Settings**: Easy, Normal, Hard with balanced gameplay
- **Event System**: Animated events (river crossing, illness, stampedes, etc.)
- **Travel System**: Distance-based progress with daily resource consumption
- **Save/Load**: JSON-based persistence with multiple save slots
- **Leaderboard**: Track high scores across difficulty levels

### Optimization
- **Sprite Caching**: Reduce recreation of frequently used sprites
- **Dirty Rect Optimization**: Efficient screen updates
- **Animation Frame Caching**: Cache animation frames to reduce computation
- **Batch Rendering**: Group sprites for efficient rendering
- **Memory Management**: Monitor and optimize memory usage

### Error Handling
- **Exception Hierarchy**: Organized exception types for different errors
- **Error Handler**: Centralized logging and recovery
- **State Guards**: Prevent invalid state transitions
- **Safe Operations**: Fallback mechanisms for critical operations
- **Boundary Checking**: Validate data within acceptable ranges

## Configuration

Edit `config.py` to customize:

```python
# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    # ... 16 CGA colors
}

# Gameplay
STARTING_PARTY_SIZE = 5
STARTING_FOOD = 800
STARTING_MONEY = 1600
```

## Game Controls

### Main Game
- **Arrow Keys / WASD**: Navigate menus, move selection
- **Enter / Space**: Confirm selection
- **Escape**: Cancel/Return to previous screen

### Hunting Mini-Game
- **Arrow Keys**: Select target
- **Space**: Fire at target

### Trading/Fort Screens
- **Up/Down**: Scroll through options
- **Left/Right**: Switch tabs
- **Enter**: Confirm selection

## Customization

### Adding Custom Sprites
Edit `graphics/character_sprites.py` and `graphics/terrain_sprites.py` to modify sprite generation.

### Adding Custom Events
Add to `event_animations.py`:
```python
class CustomAnimation(EventAnimation):
    def __init__(self):
        super().__init__(EventType.CUSTOM, duration=3.0)
    
    def draw(self, surface: pygame.Surface):
        # Draw custom animation
        pass
```

### Adding Custom Difficulty
Edit `difficulty_settings.py`:
```python
CUSTOM = DifficultySettings(
    name="Custom",
    description="Your custom difficulty",
    starting_money=2000,
    # ... other settings
)
```

### Changing Color Palette
Modify `config.py` to select different palette:
```python
PALETTE_NAME = 'EGA'  # or 'MONOCHROME', 'CGA'
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Performance Profiling
```python
from optimization import RenderStatistics

stats = RenderStatistics()
# ... run game ...
print(stats.get_summary())
```

### Debugging
Check `game.log` for error logs and debug information.

## Architecture Decisions

### Sprite Generation
Rather than storing pre-made image files, sprites are procedurally generated using Pygame drawing primitives. This reduces file size and enables dynamic sprite creation with different colors and styles.

### Color Palette
A 16-color CGA palette is used throughout to maintain authentic 1985 aesthetic while keeping memory usage minimal.

### State Machine
The game uses a state machine pattern for game states (MENU, TRAVEL, HUNT, REST, etc.) to manage transitions and keep logic organized.

### Modular Graphics
Graphics system is split into separate concerns:
- **Renderer**: Drawing primitives
- **Palette**: Color management
- **Sprites**: Game objects
- **Animation**: Keyframe sequences
- **UI**: Menus and widgets
- **Screens**: Full screen displays

## Performance Notes

### Memory Usage
- Typical memory: 50-150 MB
- Sprite cache limit: 100 surfaces
- Animation frame cache: Up to 1000 frames

### Frame Rate
- Target: 60 FPS
- Minimum: 30 FPS (with frame skipping)
- Dirty rect optimization reduces GPU load

### Save File Size
- Single save: ~5-15 KB
- 10 saves: ~50-150 KB

## Troubleshooting

### Game Won't Start
- Ensure Python 3.8+ is installed
- Check Pygame installation: `pip install pygame --upgrade`
- Verify all imports in `main.py`

### Poor Performance
- Enable optimization in `config.py`: `ENABLE_OPTIMIZATION = True`
- Reduce `FPS` value if needed
- Check `game.log` for errors

### Audio Issues
- Disable sound in settings if not working
- Check system audio is enabled

## Credits

- **Original Game**: The Oregon Trail (MECC, 1985)
- **Graphics System**: Pygame (pygame.org)
- **Development**: This graphical upgrade

## License

This is a fan recreation for educational purposes.

## Contributing

Bug reports and suggestions are welcome! Create an issue on GitHub.

## Version History

- **v1.0**: Initial graphical release
  - All 6 phases complete
  - Full gameplay implementation
  - Optimization and error handling
  - Save/load system
  - Leaderboard

---

**Enjoy playing the graphical Oregon Trail!**

For more information and to play online, visit: https://github.com/BeardedWorm/oregon_trail_graphics
