import pygame
import os
import config

# Directory to keep assets (images, sounds, fonts). Will be created if missing.
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def ensure_assets_folder():
    os.makedirs(ASSETS_DIR, exist_ok=True)

def load_font(name=None, size=20):
    try:
        if name:
         return pygame.font.SysFont(name, size)
        return pygame.font.Font(None, size)
    except Exception:
        return pygame.font.Font(None, size)
    
def load_sound(filename, volume = 1.0):
   path = os.path.join(ASSETS_DIR, "sounds", filename)
   if not os.path.exists(path):
       print(f"Warning: Sound file not found: {path}")
       return None
   sound = pygame.mixer.Sound(path)
   sound.set_volume(volume * config.MASTER_VOLUME)
   return sound

def play_sound(sound):
    """Play a given pygame Sound safely."""
    if sound:
        sound.play()
