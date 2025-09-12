import pygame
import math
import random

# A small cache for pre-rendered glow surfaces
_glow_cache = {}


def _create_glow_surface(radius, color=(255,255,255)):
    # create a surface twice the radius for smoother falloff
    size = int(radius * 4)
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = cy = size // 2
    # radial gradient: draw many circles outward with decreasing alpha
    for r in range(int(radius*2), 0, -1):
        # compute alpha falloff (quadratic)
        a = max(0, min(255, int(120 * (r / (radius*2))**2)))
        pygame.draw.circle(surf, (*color, a), (cx, cy), r)
    return surf


def get_glow(radius, color=(255,255,255)):
    """Return a pre-rendered glow surface for given radius and color."""
    key = (int(radius), color)
    if key not in _glow_cache:
        _glow_cache[key] = _create_glow_surface(radius, color)
    return _glow_cache[key]


class Particle:
    """Simple particle for hit effects."""
    def __init__(self, x, y, vx, vy, radius=2, color=(255,255,255), life=20):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.radius = radius
        self.color = color
        self.life = life
        self.max_life = life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.18  # gravity-like pull
        self.vx *= 0.995 # slight air resistance
        self.life -= 1

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = max(0, int(255 * (self.life / self.max_life)))
        s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.radius, self.radius), self.radius)
        surface.blit(s, (int(self.x - self.radius), int(self.y - self.radius)))

    def alive(self):
        return self.life > 0


def spawn_hit_particles(x, y, direction, count=12, speed=3, color=(255,255,255)):
    """Return a list of Particle objects emitted around (x,y).
    direction: -1 left, +1 right (used to bias particle velocities)
    """
    particles = []
    for i in range(count):
        # random angle slightly biased toward the direction the ball came from
        angle = random.uniform(-math.pi/2, math.pi/2)
        # bias angle horizontally
        angle += (0 if direction == 0 else (0.25 * -direction))
        sp = random.uniform(speed*0.5, speed*1.3)
        vx = math.cos(angle) * sp * (1 if direction == 0 else -direction) + random.uniform(-1,1)
        vy = math.sin(angle) * sp + random.uniform(-1.0,1.0)
        r = random.randint(1,3)
        life = random.randint(16, 32)
        particles.append(Particle(x, y, vx, vy, r, color, life))
    return particles
