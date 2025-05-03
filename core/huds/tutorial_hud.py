import pygame

from core.gauges.spaceship_stats_gauge import SpaceshipStatsGauge
from core.gauges.tagert_gauge import TargetGauge
from config import settings

class TutorialHUD:
    def __init__(self, speed, altitude, is_scrolling):
        self.screen = pygame.display.get_surface()
        self.speed = speed
        self.altitude = altitude
        self.is_scrolling = is_scrolling

        # Overlay
        self.hud_background = pygame.image.load("assets/images/hud/bottom_gradient_overlay.png").convert_alpha()

        self.hud_overlay = None
        self.hud_overlay_rect = None

        # Gauges
        self.target_gauge = TargetGauge(
            bg_image_path="assets/images/hud/hud_gauge_leading.png",
            font_path=settings.FONT_ALT_PATH,
            font_size=20,
            planet_name="LUA"
        )

        self.stats_gauge = SpaceshipStatsGauge(
            bg_image_path="assets/images/hud/hud_trailing_bg.png",
            font_path=settings.FONT_ALT_PATH,
            font_size=20,
            altitude=self.altitude,
            speed=self.speed,
        )

        self.target_gauge.set_position(20, 0)
        self.stats_gauge.set_position(20, 20)

    def update(self, speed, altitude, is_scrolling):
        self.speed = speed
        self.altitude = altitude
        self.is_scrolling = is_scrolling

        self.stats_gauge.set_altitude(altitude)
        self.stats_gauge.set_speed(speed)

    def draw(self, screen):
        width, height = screen.get_size()

        if self.hud_overlay is None:
            orig_w, orig_h = self.hud_background.get_size()
            overlay_h = int(orig_h * (width / orig_w))
            overlay_w = width

            self.hud_overlay = pygame.transform.smoothscale(
                self.hud_background, (overlay_w, overlay_h)
            )

            self.hud_overlay_rect = self.hud_overlay.get_rect(
                bottomleft=(0, height)
            )

        screen.blit(self.hud_overlay, self.hud_overlay_rect)
        self.target_gauge.draw(screen)
        self.stats_gauge.draw(screen)