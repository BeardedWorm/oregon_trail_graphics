"""
Game configuration and constants
"""

# Display settings
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = "The Oregon Trail - A Computer Game"
FPS = 60

# Palette name (16-color retro - CGA/EGA style)
PALETTE_NAME = "CGA Mode 4"

# Color palette (16-color retro - IBM PC compatible)
COLORS = {
    # Standard 8 colors
    'black': (0, 0, 0),
    'blue': (0, 0, 170),
    'green': (0, 170, 0),
    'cyan': (0, 170, 170),
    'red': (170, 0, 0),
    'magenta': (170, 0, 170),
    'brown': (170, 85, 0),
    'white': (170, 170, 170),
    
    # Bright 8 colors (high intensity)
    'gray': (85, 85, 85),
    'light_blue': (85, 85, 255),
    'light_green': (85, 255, 85),
    'light_cyan': (85, 255, 255),
    'light_red': (255, 85, 85),
    'light_magenta': (255, 85, 255),
    'yellow': (255, 255, 85),
    'light_white': (255, 255, 255),
}

# Game settings
STARTING_FOOD = 800
STARTING_AMMUNITION = 100
STARTING_MEDICINE = 20
STARTING_SPARE_PARTS = 10
STARTING_MONEY = 1600

# Trail settings
TOTAL_DISTANCE = 1600
STARTING_YEAR = 1848
SEASONS = ['Spring', 'Summer', 'Fall', 'Winter']

# Gameplay mechanics
DAILY_FOOD_PER_PERSON = 2
HUNT_SUCCESS_RATE = 0.60
ILLNESS_CHANCE = 0.05
EVENT_BASE_CHANCE = 0.20

# UI settings
FONT_SIZE_LARGE = 32
FONT_SIZE_MEDIUM = 24
FONT_SIZE_SMALL = 16

# Animation settings
ANIMATION_FPS = 8  # Retro speed
TILE_SIZE = 32
SPRITE_SCALE = 2  # 2x upscaling for retro feel

# Asset paths
ASSET_DIR = 'graphics/assets'
SPRITE_DIR = f'{ASSET_DIR}/sprites'
FONT_DIR = f'{ASSET_DIR}/fonts'
TILE_DIR = f'{ASSET_DIR}/tiles'
UI_DIR = f'{ASSET_DIR}/ui'

# Debug settings
DEBUG_MODE = False
SHOW_PALETTE = True
SHOW_FPS = True
