import pygame

class HUD:
    def __init__(self, heart_img, progress_bar, font, screen_size):
        self.heart_image = heart_img
        self.progress = progress_bar
        self.font = font
        self.hit_timer = 0
        self.hit_duration = 200
        self.blink_period = 1000
        self.blink_max_alpha = 200

        overlay_raw = pygame.image.load("assets/images/collision_overlay.png").convert_alpha()
        self.hit_overlay = pygame.transform.smoothscale(overlay_raw, screen_size)

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

        # Corações
        padding = 2
        heart_w, heart_h = self.heart_image.get_size()
        y = height - heart_h - padding
        for i in range(lives):
            x = padding + i * (heart_w + padding)
            screen.blit(self.heart_image, (x, y))

        # Barra de progresso
        self.progress.x = (width - self.progress.width) // 2
        self.progress.y = 50
        self.progress.draw(screen)

    def start_hit(self):
        self.hit_timer = self.hit_duration
