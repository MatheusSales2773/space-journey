# core/journey_progress_bar.py

import pygame

from config import settings

class JourneyProgress:
    def __init__(
        self,
        position,       # (x, y) topo-esquerdo do retângulo total (inclui ícones)
        size,           # (width, height) altura do bar = height
        start_icon,     # Surface da bandeira
        end_icon,       # Surface do planeta
        font,           
        traveled_color=(19,124,255),   
        remaining_color=(26,26,26)    
    ):
        self.x, self.y            = position
        self.width, self.height   = size
        self.start_icon           = end_icon          # Mudei de lado, faz mais sentido porque a distância é calculada da Terra até os Planetas
        self.end_icon             = start_icon        # Mudei de lado, essa bandeira significa a conclusão de um percurso
        self.font                 = pygame.font.Font(
            settings.FONT_ALT_EXPANDED_PATH, settings.FONT_SIZE_SMALL
        )
        self.alt_font                 = pygame.font.Font(
            settings.FONT_ALT_EXPANDED_PATH, settings.FONT_SIZE_GAME)
        self.traveled_color       = traveled_color
        self.remaining_color      = remaining_color

        self.percent              = 0.0
        self.distance_label       = ""
        
        self.arrow_img = pygame.image.load("assets/images/spaceship_small_right.png").convert_alpha()

    def set_progress(self, percent: float, distance_label: str):
        self.percent = max(0.0, min(percent, 100.0))
        self.distance_label = distance_label

    def draw(self, surface: pygame.Surface):
        leading_icon = self.start_icon
        trailing_icon = self.end_icon
        
        y_offset = (self.height - leading_icon.get_height()) / 2
        surface.blit(leading_icon, (self.x, self.y + y_offset))
        
        surface.blit(trailing_icon, (self.x + self.width - trailing_icon.get_width(),
                        self.y + (self.height - trailing_icon.get_height()) / 2))

        # Configurar a barra de progresso
        bar_x = self.x + leading_icon.get_width() + 5
        bar_w = self.width - leading_icon.get_width() - trailing_icon.get_width() - 10
        bar_y = self.y
        bar_h = self.height

        trav_w = int(bar_w * (self.percent / 100.0))
        pygame.draw.rect(surface, self.traveled_color, (bar_x, bar_y, trav_w, bar_h))

        # Desenha a parte restante
        pygame.draw.rect(surface, self.remaining_color, (bar_x + trav_w, bar_y, bar_w - trav_w, bar_h))

        # Cria uma surface temporária com alpha (transparência)
        border_surface = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)

        semi_transparent_white = (255, 255, 255, 64)

        pygame.draw.rect(border_surface, semi_transparent_white, (0, 0, bar_w, bar_h), width=2)

        surface.blit(border_surface, (bar_x, bar_y))
        
        trav_w = int(bar_w * (self.percent / 100))

        arrow_w, arrow_h = self.arrow_img.get_size()
        ax = bar_x + trav_w - arrow_w / 2
        ay = bar_y + (bar_h - arrow_h) / 2
        surface.blit(self.arrow_img, (ax, ay))

        perc_surf = self.font.render(f"{self.percent:.0f}%", True, (255,255,255))
        offset = 10  
        pr = perc_surf.get_rect(center=(bar_x + trav_w, bar_y + bar_h + offset + perc_surf.get_height()/2))
        surface.blit(perc_surf, pr)

        dist_surf = self.alt_font.render(self.distance_label, True, (255,255,255))
        dx = bar_x + bar_w // 2  
        dr = dist_surf.get_rect(midbottom=(dx, bar_y - 5))
        surface.blit(dist_surf, dr)
