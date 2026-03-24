# Oregon Trail - 1985 Graphical Version

A pixel-art graphical recreation of the classic 1985 Oregon Trail educational computer game using Python and Pygame.

## Project Status

🚀 **In Development** - Phase 1 Starting Soon

- Terminal version: ✅ Complete ([oregon_trail_python](https://github.com/BeardedWorm/oregon_trail_python))
- Graphical version: 🔨 In progress

## Overview

This is an upgraded graphical version of the Oregon Trail with:
- **640x480 retro pixel-art graphics** with 16-color palette
- **Authentic 1985 aesthetic** with period-accurate visuals
- **Enhanced game mechanics** including trading posts, fort stops, and difficulty settings
- **Full graphical UI** with menus, HUD, character portraits, and map display
- **Pygame-based engine** for smooth cross-platform gameplay

## Features (Planned)

### Gameplay
- 1,600+ mile journey across 11 trail locations
- Resource management (food, ammunition, medicine, spare parts, money)
- Party management with character portraits and health tracking
- Realistic illness system with 4 period diseases
- Random event engine with 10+ encounter types
- Visual hunting mini-game
- Trading post interactions at forts
- Day/season/year progression

### Graphics & UI
- Pixel-art character sprites and party portraits
- Terrain tiles and location graphics
- Weather effects (snow, rain, storms)
- Animated sequences (hunting, travel, events)
- Interactive menus with mouse/keyboard support
- Real-time HUD showing resources and status
- Character status screens with detailed information

## Project Structure

```
oregon_trail_graphics/
├── main.py                 # Entry point
├── game.py                 # Core game logic
├── models.py               # Game state and data structures
├── config.py               # Game configuration
├── graphics/
│   ├── renderer.py         # Main rendering engine
│   ├── ui.py               # UI components and menus
│   ├── sprites.py          # Sprite and animation handling
│   └── assets/
│       ├── sprites/        # Character and object sprites
│       ├── fonts/          # Bitmap fonts
│       ├── tiles/          # Terrain tiles
│       └── ui/             # UI elements
├── persistence.py          # Save/load system
├── assets.py               # Asset loading and management
├── requirements.txt        # Python dependencies
├── UPGRADE_PLAN.md         # Detailed implementation plan
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

## Development Phases

### Phase 1: Graphics Foundation (5 tasks)
- Pygame setup and initialization
- Color palette system
- Sprite system implementation
- Asset loading pipeline
- Basic menu system

### Phase 2: UI System (5 tasks)
- Main menu with options
- In-game HUD display
- Character status screens
- Trail map visualization
- Event message system

### Phase 3: Game Graphics (5 tasks)
- Character sprites and portraits
- Terrain and location graphics
- Animation engine
- Seasonal weather effects
- UI element graphics

### Phase 4: Gameplay Integration (5 tasks)
- Game loop refactoring for graphics
- Mouse/keyboard input system
- Menu integration with game logic
- Visual hunting mini-game
- Event animations

### Phase 5: Enhanced Mechanics (5 tasks)
- Improved resource management UI
- Enhanced party member tracking
- Trading post system
- Fort stop mechanics
- Difficulty settings

### Phase 6: Polish & Optimization (5 tasks)
- Performance optimization
- Save/load integration
- Leaderboard display
- Error handling
- Documentation

## Requirements

- Python 3.7+
- Pygame 2.0+
- See `requirements.txt` for full list

## Installation

```bash
git clone https://github.com/BeardedWorm/oregon_trail_graphics.git
cd oregon_trail_graphics
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature suggestions.

## Related Projects

- **Terminal Version**: [oregon_trail_python](https://github.com/BeardedWorm/oregon_trail_python)
  - Original terminal-based implementation
  - Full working game in green text
  - Reference implementation

## License

This is a fan recreation made for educational purposes.

## Credits

Original Game: The Learning Company (1985)  
Terminal Version: Earlier project  
Graphical Version: In development  

## Roadmap

- [ ] Phase 1: Graphics Foundation
- [ ] Phase 2: UI System  
- [ ] Phase 3: Game Graphics
- [ ] Phase 4: Gameplay Integration
- [ ] Phase 5: Enhanced Mechanics
- [ ] Phase 6: Polish & Optimization
- [ ] Beta release
- [ ] Sound effects (optional)
- [ ] Additional sprite sets
- [ ] Mod support

---

**Status**: Project initialized and planning complete. Development starting soon!
