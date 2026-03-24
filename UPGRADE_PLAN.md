# Oregon Trail - 1985 Graphical Version - Development Plan

## Project Overview
Upgrade the terminal-based Oregon Trail game to a graphical version with authentic 1985 pixel art aesthetics, while refactoring and improving the underlying game systems.

**Technology Stack:**
- Python 3 with Pygame
- Resolution: 640x480 (period-accurate)
- Color palette: 16-color retro aesthetic
- Graphical interface with menus, map, status displays, character portraits

## Architecture Changes

### Module Structure (Enhanced)
```
oregon_trail_graphics/
├── main.py              # Entry point
├── game.py              # Core game logic (refactored)
├── models.py            # Game state (enhanced)
├── config.py            # Configuration and constants
├── graphics/
│   ├── renderer.py      # Main rendering engine
│   ├── ui.py            # UI components & menus
│   ├── sprites.py       # Sprite and animation handling
│   └── assets/
│       ├── sprites/     # Character/object sprites
│       ├── fonts/       # Retro bitmap fonts
│       ├── tiles/       # Terrain tiles
│       └── ui/          # UI elements
├── persistence.py       # Save/load system (enhanced)
├── assets.py            # Asset loading
├── requirements.txt
└── UPGRADE_PLAN.md
```

## Implementation Phases

### Phase 1: Graphics Foundation
**Tasks:** 5 | **Dependencies:** None
- [ ] Set up Pygame with 640x480 resolution and retro color palette
- [ ] Create color palette system (16-color retro)
- [ ] Implement sprite system for loading and rendering
- [ ] Build asset loading pipeline for sprites, fonts, configurations
- [ ] Create basic menu system with navigation

### Phase 2: UI System
**Tasks:** 5 | **Dependencies:** Phase 1
- [ ] Build main menu with New Game, Load, Leaderboard, Options, Exit
- [ ] Implement in-game HUD (status bar, resources, date, health)
- [ ] Create character status display screens
- [ ] Build trail map visualization showing progress
- [ ] Create event message display system

### Phase 3: Game Graphics
**Tasks:** 5 | **Dependencies:** Phase 1-2
- [ ] Create character sprites (party members with multiple states)
- [ ] Build terrain and location graphics (grass, mountains, water, forts)
- [ ] Implement animation engine (movement, hunting, transitions)
- [ ] Add seasonal weather visual effects (snow, rain, storms)
- [ ] Create UI element graphics (buttons, frames, icons, borders)

### Phase 4: Gameplay Integration
**Tasks:** 5 | **Dependencies:** Phase 1-3
- [ ] Refactor game loop to integrate with graphics rendering
- [ ] Implement mouse and keyboard input system
- [ ] Integrate all menus with game logic (Travel, Hunt, Rest, Check)
- [ ] Create visual hunting mini-game with animations
- [ ] Add animations and visual effects for random events

### Phase 5: Enhanced Mechanics
**Tasks:** 5 | **Dependencies:** Phase 3-4
- [ ] Improve resource management UI with visual bar displays
- [ ] Enhance party member tracking with visual health indicators
- [ ] Add trading post interactions (buy/sell at forts graphically)
- [ ] Implement fort stop mechanics (rest, resupply, information)
- [ ] Add difficulty selection screen (Easy, Normal, Hard)

### Phase 6: Polish & Optimization
**Tasks:** 5 | **Dependencies:** Phase 5
- [ ] Performance optimization (sprite batching, efficient rendering)
- [ ] Integrate save/load system (JSON compatibility)
- [ ] Display leaderboard graphically (top 10 scores)
- [ ] Handle edge cases and errors gracefully
- [ ] Create comprehensive upgrade documentation

## Key Design Decisions

### Visual Style
- **Resolution**: 640x480 (authentic 1985)
- **Palette**: 16-color retro (CGA/EGA style)
- **Sprites**: Pixel art with 16-32 pixel characters
- **Fonts**: Bitmap fonts (8x8 or similar)
- **Animation**: Frame-based, retro speed (8-16 FPS for smooth movement)

### Gameplay Integration
- **Input**: Mouse + keyboard support
- **Turn-based**: Keep turn-based gameplay with animated sequences
- **Performance**: Efficient sprite rendering with batching
- **Compatibility**: Maintain save file compatibility with terminal version

### Asset Management
- **Sprite sheets**: Combine multiple sprites per sheet for efficiency
- **Asset pipeline**: Preload all assets on startup
- **Configuration**: Sprite positions, animations, and layouts in JSON

## Feature Matrix

| Feature | Terminal | Graphics | Enhanced |
|---------|----------|----------|----------|
| Resource Management | ✓ | ✓ | ✓ Trading |
| Party Management | ✓ | ✓ Portraits | ✓ Visual |
| Illness System | ✓ | ✓ Visual | ✓ |
| Random Events | ✓ | ✓ Animated | ✓ |
| Hunting | ✓ | ✓ Animation | ✓ Enhanced |
| Travel | ✓ | ✓ Map | ✓ |
| Save/Load | ✓ | ✓ | ✓ Thumbnails |
| Leaderboard | ✓ | ✓ | ✓ Visual |
| Trading Posts | ✗ | ✓ | ✓ |
| Fort Stops | ✗ | ✓ | ✓ |
| Difficulty Settings | ✗ | ✓ | ✓ |

## Asset Requirements

### Sprites Needed
- Party member character sprites (idle, walking, sick, dead)
- Wagon and oxen graphics
- Wildlife (buffalo, snake, rabbit, deer)
- Terrain tiles (grass, dirt, mountains, water, snow)
- Building sprites (forts, trading posts, towns)
- UI elements (buttons, scroll bars, frames, icons, borders)
- Weather effects (snow particles, rain, dust)

### Fonts
- Main bitmap font (8x8 or 8x16)
- Optional: Title/menu font for variety

### Animation Frames
- Character walking (left, right, up, down)
- Hunting sequence
- Event animations
- Transition effects

## Technical Specifications

### Resolution & Timing
- Display: 640x480 pixels
- Frame Rate: 60 FPS (internal), scaled for retro feel
- Color Depth: 16-bit (5-6-5 RGB)

### Input Handling
- Mouse: Menu navigation, selection
- Keyboard: Shortcuts, menu navigation, game controls

### Performance Targets
- Load time: < 2 seconds
- Frame rate: Stable 60 FPS
- Memory: < 100 MB

## Deliverables

### Core Application
- Standalone Pygame executable/script
- Full game with all features
- Cross-platform support (Windows, Mac, Linux)

### Asset Package
- Sprite sheets and individual sprites
- Font files and configuration
- Configuration files for sprite/animation data

### Documentation
- Detailed installation and setup guide
- Asset creation and customization guide
- Developer documentation
- Graphics specification document

### Backwards Compatibility
- Save file conversion (if needed)
- Configuration migration from terminal version

## Milestone Timeline

1. **Milestone 1**: Graphics Foundation complete (Phase 1)
2. **Milestone 2**: UI System complete (Phase 1-2)
3. **Milestone 3**: Game Graphics complete (Phase 1-3)
4. **Milestone 4**: Gameplay Integration complete (Phase 1-4)
5. **Milestone 5**: Enhanced Mechanics complete (Phase 1-5)
6. **Milestone 6**: Polish & Release (Phase 1-6)

## Future Enhancements
- Sound effects and music
- Extended sprite sets and themes
- Mod support and asset packs
- Multiplayer/co-op mode
- Additional historical scenarios
- Custom difficulty/game modes
- Web version (via Pygame to JavaScript transpiler)
- Mobile version
