import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Centralized constants and configuration for the game
WIDTH = 700
HEIGHT = 500
FPS = 60


PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_RADIUS = 7


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (200, 200, 200)


WINNING_SCORE = 5


SCORE_FONT_NAME = "comicsans"
SCORE_FONT_SIZE = 50


# Toggle debug features (FPS display, draw hitboxes, etc.)
DEBUG = False

TRAIL_LENGTH = 12 # how many positions for the ball trail
GLOW_RADIUS_FACTOR = 2 # glow radius relative to ball radius
PARTICLE_COUNT_HIT = 14 # number of particles when ball hits paddle
PARTICLE_LIFETIME = 28 # frames
PARTICLE_GRAVITY = 0.18
CENTER_LINE_SEG_HEIGHT = HEIGHT // 20
CENTER_LINE_SPEED = 0.6 # pixels per frame (float for smooth motion)
SCORE_PULSE_MAG = 1.65 # initial scale when scoring
SCORE_PULSE_DECAY = 0.04 # how fast the pulse decays per frame
SCREEN_SHAKE_MAG = 6 # maximum shake pixels
SCREEN_SHAKE_DECAY = 0.85 # multiply per frame when active

# --- Audio ---
MASTER_VOLUME = 0.6
SFX_VOLUME = 0.8
MUSIC_VOLUME = 0.4

# Sound file names (placed in assets/sounds/)
SOUND_HIT_PADDLE = "hit_paddle.mp3"
SOUND_HIT_WALL = "hit_wall.mp3"
SOUND_SCORE = "score.mp3"
SOUND_WIN = "win.mp3"
MUSIC_BG = "bg_music.mp3"
