import pygame
from config import settings

class JourneyProgress:
    def __init__(
        self,
        start_icon,
        end_icon,
        traveled_color=(95,254,255),
        remaining_color=(40,40,40)
    ):
        self.x = 0
        self.y = 0

        self.width = 1000
        self.height = 100

        self.start_icon = start_icon
        self.end_icon = end_icon
        self.font = pygame.font.Font(settings.FONT_ALT_EXPANDED_PATH, settings.FONT_SIZE_SMALL)
        self.alt_font = pygame.font.Font(settings.FONT_ALT_EXPANDED_PATH, settings.FONT_SIZE_GAME)
        self.traveled_color = traveled_color
        self.remaining_color = remaining_color

        self.percent = 0.0
        self.distance_label = ""

        self.indicator_img = pygame.image.load(
            "assets/images/spaceship_small_right.png"
        ).convert_alpha()
        self.hud_bg = pygame.image.load(
            "assets/images/hud/hud_progress_bg.png"
        ).convert_alpha()

    def set_progress(self, percent: float, distance_label: str):
        self.percent = max(0.0, min(percent, 100.0))
        self.distance_label = distance_label

    def draw(self, surface: pygame.Surface):
        # Padding interno e margens
        padding = 2  # margem superior
        icon_margin = 170  # espaço antes e depois dos ícones
        bar_margin = 15   # margem entre ícone e início/barra

        margin_text_bar = 20   # espaço entre texto de distância e barra
        margin_bar_text = 10   # espaço entre barra e texto de porcentagem

        # Alturas de texto e barra
        text_above = self.alt_font.get_height()
        bar_h = 10
        text_below = self.font.get_height()

        # Cálculo de altura total (fundo)
        full_height = padding + text_above + margin_text_bar + bar_h + margin_bar_text + text_below + padding

        # Desenha fundo do HUD
        bg_scaled = pygame.transform.smoothscale(
            self.hud_bg, (self.width, full_height)
        )
        surface.blit(bg_scaled, (self.x, self.y))

        # Área útil interna (x horizontal, y do topo da barra)
        x0 = self.x + padding + icon_margin
        y0 = self.y + padding + text_above + margin_text_bar
        inner_width = self.width - 2 * (padding + icon_margin)

        # Ícones laterais com margem extra
        icon_y = y0 + (bar_h - self.start_icon.get_height()) / 2
        surface.blit(self.start_icon, (x0, icon_y))
        surface.blit(
            self.end_icon,
            (x0 + inner_width - self.end_icon.get_width(), icon_y)
        )

        # Área da barra
        bar_x = x0 + self.start_icon.get_width() + bar_margin
        bar_w = inner_width - self.start_icon.get_width() - self.end_icon.get_width() - 2 * bar_margin
        bar_y = y0

        # Desenha progresso
        skew = 2
        trav_w = int(bar_w * (self.percent / 100.0))
        traveled_points = [
            (bar_x + skew, bar_y),
            (bar_x + trav_w + skew, bar_y),
            (bar_x + trav_w - skew, bar_y + bar_h),
            (bar_x - skew, bar_y + bar_h)
        ]
        pygame.draw.polygon(surface, self.traveled_color, traveled_points)

        remaining_points = [
            (bar_x + trav_w + skew, bar_y),
            (bar_x + bar_w + skew, bar_y),
            (bar_x + bar_w - skew, bar_y + bar_h),
            (bar_x + trav_w - skew, bar_y + bar_h)
        ]
        pygame.draw.polygon(surface, self.remaining_color, remaining_points)

        indicator_w, indicator_h = self.indicator_img.get_size()
        ax = bar_x + trav_w - indicator_w / 2
        ay = bar_y + (bar_h - indicator_h) / 2
        surface.blit(self.indicator_img, (ax, ay))

        # Texto de porcentagem 
        perc_surf = self.font.render(f"{self.percent:.0f}%", True, (95,254,255))
        pr = perc_surf.get_rect(
            center=(bar_x + trav_w, bar_y + bar_h + margin_bar_text + text_below / 2)
        )
        surface.blit(perc_surf, pr)

        # Texto de distância 
        dist_surf = self.font.render(self.distance_label, True, (240,240,240))
        dx = bar_x + bar_w // 2
        dr = dist_surf.get_rect(midbottom=(dx, bar_y - margin_text_bar / 2))
        surface.blit(dist_surf, dr)