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

        self.font = pygame.font.Font(settings.FONT_ALT_PATH, settings.FONT_SIZE_SMALL)
        self.notice_font = pygame.font.Font(settings.FONT_ALT_PATH, 18)

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

        self.hint_text = "PRESSIONE ESPAÇO PARA LANÇAR"
        self.highlight = "ESPAÇO"
        self.hint_padding = 6

    def update(self, speed, altitude, is_scrolling):
        self.speed = speed
        self.altitude = altitude
        self.is_scrolling = is_scrolling

        self.stats_gauge.set_altitude(altitude)
        self.stats_gauge.set_speed(speed)

    def _draw_hint(self, surface, w, h):
        before, after = self.hint_text.split(self.highlight)
        font = self.font

        before_surf = font.render(before, True, (255, 255, 255))
        highlight_surf = font.render(self.highlight, True, (0, 0, 0))
        after_surf = font.render(after, True, (255, 255, 255))

        pad = self.hint_padding
        gap = 12

        total_w = (
                before_surf.get_width()
                + gap
                + highlight_surf.get_width()
                + 2 * pad
                + gap
                + after_surf.get_width()
        )
        x = (w - total_w) // 2
        y = h - 100

        surface.blit(before_surf, (x, y))
        x += before_surf.get_width()

        x += gap

        rect = pygame.Rect(
            x - pad - 3,
            y - pad // 2,
            highlight_surf.get_width() + 2 * pad,
            highlight_surf.get_height() + pad
        )

        slant = rect.height // 6

        points = [
            (rect.left + slant, rect.top),
            (rect.right + slant, rect.top),
            (rect.right, rect.bottom),
            (rect.left, rect.bottom),
        ]

        pygame.draw.polygon(surface, (255, 255, 255), points)

        surface.blit(highlight_surf, (x, y))
        x += highlight_surf.get_width()

        x += gap

        surface.blit(after_surf, (x, y))

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

        notice = self.notice_font.render("As distâncias, velocidades e proporções apresentadas são ilustrativas", True, (94, 169, 197))
        notice_rect = notice.get_rect(topleft=(30, 30))

        notice_s = self.notice_font.render(
            "e não correspondem a escalas reais.",
            True, (94, 169, 197))
        notice_rect_s = notice_s.get_rect(topleft=(30, 48))

        if self.is_scrolling:
            screen.blit(notice, notice_rect)
            screen.blit(notice_s, notice_rect_s)

        if not self.is_scrolling:
            self._draw_hint(screen, width, height)