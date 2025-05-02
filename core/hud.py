import pygame

from config import settings
from core.gauges.integrity_gauge import ShipIntegrityGauge

class HUD:
    def __init__(self, progress_bar, font, screen_size):
        self.progress = progress_bar
        self.font = font
        self.hit_timer = 0
        self.hit_duration = 200
        self.blink_period = 1000
        self.blink_max_alpha = 200

        overlay_raw = pygame.image.load("assets/images/collision_overlay.png").convert_alpha()
        self.hit_overlay = pygame.transform.smoothscale(overlay_raw, screen_size)

        self.heart_image = pygame.image.load("assets/images/heart.png").convert_alpha()
        self.traling_bg = pygame.image.load("assets/images/hud/hud_trailing_bg.png").convert_alpha()

        heart_size = 96
        self.heart_image = pygame.transform.smoothscale(
            self.heart_image, (heart_size, heart_size)
        )

        self.integrity_gauge = ShipIntegrityGauge(
            bg_image_path="assets/images/hud/hud_trailing_bg.png",
            heart_image_path="assets/images/heart.png",
            font_path=settings.FONT_ALT_PATH,
            font_size=20,
            max_lives=3
        )

        self.integrity_gauge.set_position(20, 20)


    def update_hit_effect(self, dt, lives):
        if lives <= 0:
            return
        if self.hit_timer > 0:
            self.hit_timer -= dt * 1000
            if self.hit_timer < 0:
                self.hit_timer = 0

    def draw(self, screen, lives, width, height):
        # Overlay de dano
        if lives == 1 or self.hit_timer > 0:
            alpha = 0
            if lives == 1:
                t = pygame.time.get_ticks() % self.blink_period
                half = self.blink_period / 2
                alpha = int((t / half) * self.blink_max_alpha) if t <= half else int(((self.blink_period - t) / half) * self.blink_max_alpha)
            elif self.hit_timer > 0:
                alpha = int(self.hit_timer / self.hit_duration * 255)

            if alpha > 0:
                overlay = self.hit_overlay.copy()
                overlay.set_alpha(alpha)
                screen.blit(overlay, (0, 0))

        self.integrity_gauge.update_lives(lives)
        self.integrity_gauge.draw(screen)

        # Barra de progresso
        self.progress.x = (width - self.progress.width) // 2
        self.progress.y = 0
        self.progress.draw(screen)

    def start_hit(self):
        self.hit_timer = self.hit_duration
