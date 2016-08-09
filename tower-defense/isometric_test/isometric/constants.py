import os

# Filesystem-related constants
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMG_DIR = os.path.join(BASE_DIR, *["static", "img"])
MAPS_DIR = os.path.join(BASE_DIR, *["static", "maps"])

# General game constants
FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
TILE_SIZE = 50  # pixels
MAP_WIDTH, MAP_HEIGHT = 20, 20
MAP_SIZE = (MAP_WIDTH, MAP_HEIGHT)