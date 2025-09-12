from collections import deque
import pygame
from config import *


class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width=PADDLE_WIDTH, height=PADDLE_HEIGHT):
        self.x = self.original_x = float(x)
        self.y = self.original_y = float(y)
        self.width = width
        self.height = height

    def draw(self, surface):
        pygame.draw.rect(surface, self.COLOR, (int(self.x), int(self.y), self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 7
    COLOR = WHITE

    def __init__(self, x, y, radius=BALL_RADIUS):
        self.x = self.original_x = float(x)
        self.y = self.original_y = float(y)
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        # trail buffer for Phase 1
        self.trail = deque(maxlen=TRAIL_LENGTH)

    def draw(self, surface):
        # draw trail first (fading circles)
        for i, (tx, ty) in enumerate(self.trail):
            alpha = max(8, 220 - i * 18)
            r = max(1, int(self.radius - i * 0.3))
            rs = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(rs, (255,255,255, alpha), (r, r), r)
            surface.blit(rs, (int(tx - r), int(ty - r)))

        # main ball
        pygame.draw.circle(surface, self.COLOR, (int(self.x), int(self.y)), self.radius)

    def move(self):
        # store position for trail then update
        self.trail.appendleft((self.x, self.y))
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
        self.trail.clear()
