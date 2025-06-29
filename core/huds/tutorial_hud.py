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

        # CONTAGEM REGRESSIVA
        self.countdown_active = False
        self.countdown_start = 0  # timestamp em ms
        self.countdown_duration = 3000  # 3 segundos
        self.countdown_font = pygame.font.Font(settings.FONT_ALT_PATH, 528)

        self.countdown_sound = pygame.mixer.Sound('assets/audio/countdown.mp3')
        self.launch_sound = pygame.mixer.Sound('assets/audio/launch.mp3')

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
            planet_name="MERCÚRIO"
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

        # Variáveis para a animação
        self.animation_active = False
        self.animation_progress = 0.0
        self.animation_speed = 1.5
        self.animation_offset = 300

        self.hint_text = "PRESSIONE ESPAÇO PARA LANÇAR"
        self.highlight = "ESPAÇO"
        self.hint_padding = 6

    def start_countdown(self):
        if not self.countdown_active and not self.is_scrolling:
            self.countdown_active = True
            self.countdown_start = pygame.time.get_ticks()

            self.countdown_sound.play()

    def update(self, speed, altitude, is_scrolling):
        self.speed = speed
        self.altitude = altitude

        # Verifica se o scrolling acabou de começar (seja por input externo ou pelo countdown)
        scrolling_just_started = is_scrolling and not self.is_scrolling

        # gerencia transição do countdown → scroll
        if self.countdown_active:
            elapsed = pygame.time.get_ticks() - self.countdown_start
            if elapsed >= self.countdown_duration:
                self.countdown_active = False
                self.is_scrolling = True
                # Marca que o scrolling está começando agora
                scrolling_just_started = True

                self.launch_sound.play()
        else:
            # só sincroniza is_scrolling se o countdown não estiver ativo
            self.is_scrolling = is_scrolling

        # Inicia a animação dos gauges quando o scrolling começa
        if scrolling_just_started:
            self.animation_active = True
            self.animation_progress = 0.0

        # atualiza gauges
        self.stats_gauge.set_altitude(altitude)
        self.stats_gauge.set_speed(speed)

        # Atualiza a animação se estiver ativa
        if self.animation_active and self.animation_progress < 1.0:
            self.animation_progress += self.animation_speed * (1 / 60)
            if self.animation_progress >= 1.0:
                self.animation_progress = 1.0
                self.animation_active = False

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

        # Apenas desenha o contador quando estiver ativo
        if self.countdown_active:
            now = pygame.time.get_ticks()
            rem = self.countdown_duration - (now - self.countdown_start)
            sec = max(1, int(rem // 1000) + 1)

            # Texto da sombra
            shadow_txt = self.countdown_font.render(str(sec), True, (0, 0, 0)).convert_alpha()
            shadow_txt.set_alpha(120)
            shadow_rect = shadow_txt.get_rect(center=(width // 2 + 3, height // 2 + 3))
            screen.blit(shadow_txt, shadow_rect)

            # Texto principal
            txt = self.countdown_font.render(str(sec), True, (255, 255, 255)).convert_alpha()
            rect = txt.get_rect(center=(width // 2, height // 2))
            screen.blit(txt, rect)

        # Aviso sobre escalas proporcionais
        notice = self.notice_font.render("As distâncias, velocidades e proporções apresentadas são ilustrativas", True,
                                         (94, 169, 197))
        notice_rect = notice.get_rect(topleft=(30, 30))

        notice_s = self.notice_font.render(
            "e não correspondem a escalas reais.",
            True, (94, 169, 197))
        notice_rect_s = notice_s.get_rect(topleft=(30, 48))

        if self.is_scrolling:
            screen.blit(notice, notice_rect)
            screen.blit(notice_s, notice_rect_s)

            # Sempre que o scrolling estiver ativo, desenha os gauges com animação
            if self.animation_active or self.animation_progress > 0:
                animation_offset = (1 - self.animation_progress) * self.animation_offset

                target_w, target_h = self.target_gauge.bg_image.get_size()
                stats_w, stats_h = self.stats_gauge.bg_image.get_size()

                self.target_gauge.set_position(
                    40,
                    height - target_h - 40 + animation_offset
                )

                self.stats_gauge.set_position(
                    width - stats_w - 40,
                    height - stats_h - 40 + animation_offset
                )

                self.target_gauge.draw(screen, use_preset_position=True)
                self.stats_gauge.draw(screen, use_preset_position=True)

        # Mostra dica apenas quando não estiver scrolling e não estiver em countdown
        if not self.is_scrolling and not self.countdown_active:
            self._draw_hint(screen, width, height)