import pygame
import sys
import os
import random
import traceback

from config import *  # expects ASSETS_DIR, MUSIC_BG, SOUND_HIT_PADDLE, etc.
from asset_loader import ensure_assets_folder, load_font, load_sound, play_sound
from entities import Paddle, Ball
import effects

# -----------------------------------------------------------------------------
# Globals for sounds
hit_paddle_snd = None
hit_wall_snd = None
score_snd = None
win_snd = None

# Game state
particles = []  # list of active particles

# -----------------------------------------------------------------------------
# Colors
GRAY = (180, 180, 180)
ACCENT = (100, 180, 255)  # light blue accent for modern look

# -----------------------------------------------------------------------------
# Helpers
def center_text(surface, text_surf, y=None):
    x = WIDTH // 2 - text_surf.get_width() // 2
    if y is None:
        y = HEIGHT // 2 - text_surf.get_height() // 2
    surface.blit(text_surf, (x, y))


def draw_button(surface, text, font, y, color=WHITE, hover_color=ACCENT):
    """Draws centered button text with hover effect."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    text_surf = font.render(text, True, color)
    rect = text_surf.get_rect(center=(WIDTH // 2, y))

    if rect.collidepoint(mouse_x, mouse_y):
        text_surf = font.render(text, True, hover_color)

    surface.blit(text_surf, rect)
    return rect


def draw_score_with_pulse(surface, score_font, score, center_x, pulse):
    base_surf = score_font.render(str(score), True, WHITE)
    if pulse > 1.01:
        w, h = base_surf.get_size()
        sw = max(1, int(w * pulse))
        sh = max(1, int(h * pulse))
        scaled = pygame.transform.smoothscale(base_surf, (sw, sh))
        surface.blit(scaled, (int(center_x - scaled.get_width()//2),
                              20 - int((scaled.get_height() - h)/2)))
    else:
        surface.blit(base_surf, (int(center_x - base_surf.get_width()//2), 20))


def draw_game(render_surf, paddles, ball, left_score, right_score, score_font,
              line_offset, left_pulse, right_pulse):
    render_surf.fill(BLACK)

    # scores
    draw_score_with_pulse(render_surf, score_font, left_score, WIDTH//4, left_pulse)
    draw_score_with_pulse(render_surf, score_font, right_score, WIDTH*3//4, right_pulse)

    for paddle in paddles:
        paddle.draw(render_surf)

    # dashed line
    seg_h = max(6, CENTER_LINE_SEG_HEIGHT)
    off = int(line_offset)
    for i in range(0, HEIGHT, seg_h + 6):
        y = (i + off) % HEIGHT
        pygame.draw.rect(render_surf, WHITE, (WIDTH//2 - 5, y, 10, seg_h))

    # glow
    try:
        glow = effects.get_glow(int(ball.radius * GLOW_RADIUS_FACTOR), (200, 240, 255))
        gw, gh = glow.get_size()
        render_surf.blit(glow, (int(ball.x - gw/2), int(ball.y - gh/2)), special_flags=pygame.BLEND_RGBA_ADD)
    except Exception:
        pass

    ball.draw(render_surf)

    for p in particles:
        p.draw(render_surf)


def handle_collisions(ball, left_paddle, right_paddle):
    global particles, hit_wall_snd, hit_paddle_snd

    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1
        play_sound(hit_wall_snd)
        edge_y = HEIGHT - 8 if ball.y > HEIGHT//2 else 8
        particles.extend(effects.spawn_hit_particles(ball.x, edge_y, 0, count=8, speed=2))

    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height/2
                diff = middle_y - ball.y
                ball.y_vel = -1 * (diff / ((left_paddle.height/2)/ball.MAX_VEL))
                particles.extend(effects.spawn_hit_particles(ball.x, ball.y, -1, count=PARTICLE_COUNT_HIT, speed=3))
                play_sound(hit_paddle_snd)
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height/2
                diff = middle_y - ball.y
                ball.y_vel = -1 * (diff / ((right_paddle.height/2)/ball.MAX_VEL))
                particles.extend(effects.spawn_hit_particles(ball.x, ball.y, 1, count=PARTICLE_COUNT_HIT, speed=3))
                play_sound(hit_paddle_snd)


# -----------------------------------------------------------------------------
def safe_mixer_init():
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        return True
    except Exception:
        try:
            pygame.mixer.init()
            return True
        except Exception as e2:
            print(f"[WARN] mixer init fail: {e2}")
            return False


def paddle_handle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w]:
        left_paddle.y = max(0, left_paddle.y - left_paddle.VEL)
    if keys[pygame.K_s]:
        left_paddle.y = min(HEIGHT-left_paddle.height, left_paddle.y + left_paddle.VEL)
    if keys[pygame.K_UP]:
        right_paddle.y = max(0, right_paddle.y - right_paddle.VEL)
    if keys[pygame.K_DOWN]:
        right_paddle.y = min(HEIGHT-right_paddle.height, right_paddle.y + right_paddle.VEL)


# -----------------------------------------------------------------------------
# Modern Start Screen
def start_screen(screen, clock):
    waiting = True
    while waiting:
        screen.fill(BLACK)

        title_font = pygame.font.Font(None, 100)
        subtitle_font = pygame.font.Font(None, 36)
        button_font = pygame.font.Font(None, 48)

        # Title
        title = title_font.render("PONG", True, ACCENT)
        center_text(screen, title, HEIGHT//3 - 60)

        # Subtitle
        sub = subtitle_font.render("Created by Afif", True, GRAY)
        center_text(screen, sub, HEIGHT//3 + 20)

        # Play button
        draw_button(screen, "Press ENTER to Play", button_font, HEIGHT//2 + 120)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


# Modern End Screen
def end_screen(screen, clock, message):
    pygame.mixer.music.stop()
    waiting = True
    while waiting:
        screen.fill(BLACK)

        title_font = pygame.font.Font(None, 80)
        button_font = pygame.font.Font(None, 42)

        title = title_font.render(message, True, ACCENT)
        center_text(screen, title, HEIGHT//3)

        draw_button(screen, "Press R to Replay | ESC to Quit", button_font, HEIGHT//2 + 120)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()


# -----------------------------------------------------------------------------
def main():
    global particles, hit_paddle_snd, hit_wall_snd, score_snd, win_snd
    pygame.init()
    ensure_assets_folder()
    audio_ok = safe_mixer_init()

    try:
        winning_score = int(WINNING_SCORE)
    except Exception:
        winning_score = 10

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Game")

    score_font = load_font(SCORE_FONT_NAME, SCORE_FONT_SIZE)

    if audio_ok:
        hit_paddle_snd = load_sound(SOUND_HIT_PADDLE, SFX_VOLUME)
        hit_wall_snd = load_sound(SOUND_HIT_WALL, SFX_VOLUME)
        score_snd = load_sound(SOUND_SCORE, SFX_VOLUME)
        win_snd = load_sound(SOUND_WIN, SFX_VOLUME)

    clock = pygame.time.Clock()
    start_screen(screen, clock)

    playing = True
    while playing:
        if audio_ok:
            try:
                music_path = os.path.join(ASSETS_DIR, "sounds", MUSIC_BG)
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(MUSIC_VOLUME*MASTER_VOLUME)
                    pygame.mixer.music.play(-1)
            except Exception as me:
                print(f"[WARN] music error: {me}")

        left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2)
        right_paddle = Paddle(WIDTH-10-PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
        ball = Ball(WIDTH//2, HEIGHT//2)
        left_score, right_score = 0, 0
        particles.clear()
        line_offset, left_pulse, right_pulse, shake_mag = 0, 1.0, 1.0, 0

        run = True
        while run:
            dt = clock.tick(FPS)
            line_offset = (line_offset + CENTER_LINE_SPEED) % HEIGHT

            if left_pulse > 1: left_pulse = max(1, left_pulse - SCORE_PULSE_DECAY)
            if right_pulse > 1: right_pulse = max(1, right_pulse - SCORE_PULSE_DECAY)
            shake_mag = shake_mag*SCREEN_SHAKE_DECAY if shake_mag > 0.01 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            keys = pygame.key.get_pressed()
            paddle_handle_movement(keys, left_paddle, right_paddle)

            ball.move(); handle_collisions(ball, left_paddle, right_paddle)

            if ball.x < 0:
                right_score += 1; play_sound(score_snd); ball.reset()
                right_pulse, shake_mag = SCORE_PULSE_MAG, SCREEN_SHAKE_MAG
            if ball.x > WIDTH:
                left_score += 1; play_sound(score_snd); ball.reset()
                left_pulse, shake_mag = SCORE_PULSE_MAG, SCREEN_SHAKE_MAG

            for p in particles: p.update()
            particles[:] = [p for p in particles if p.alive()]

            render_surf = pygame.Surface((WIDTH, HEIGHT))
            draw_game(render_surf, [left_paddle, right_paddle], ball,
                      left_score, right_score, score_font,
                      line_offset, left_pulse, right_pulse)

            if DEBUG:
                fps_surf = pygame.font.Font(None, 20).render(f"FPS: {int(clock.get_fps())}", True, WHITE)
                render_surf.blit(fps_surf, (8, 8))

            ox = int(random.uniform(-shake_mag, shake_mag)) if shake_mag>0 else 0
            oy = int(random.uniform(-shake_mag, shake_mag)) if shake_mag>0 else 0

            screen.fill(BLACK); screen.blit(render_surf, (ox, oy))
            pygame.display.update()

            won = None
            if left_score >= winning_score: won = "PLAYER 1 WINS!"
            elif right_score >= winning_score: won = "PLAYER 2 WINS!"

            if won:
                play_sound(win_snd)
                replay = end_screen(screen, clock, won)
                if replay: run = False
                else: playing, run = False, False

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        input("Press Enter to exit...")
