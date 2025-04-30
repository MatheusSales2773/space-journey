# core/journey_progress_bar.py

import pygame

class JourneyProgress:
    def __init__(
        self,
        position,       # (x, y) topo-esquerdo do retângulo total (inclui ícones)
        size,           # (width, height) altura do bar = height
        start_icon,     # Surface da bandeira
        end_icon,       # Surface do planeta
        font,           
        traveled_color=(241,162,8),   
        remaining_color=(5,47,95)    
    ):
        self.x, self.y            = position
        self.width, self.height   = size
        self.start_icon           = start_icon
        self.end_icon             = end_icon
        self.font                 = font
        self.traveled_color       = traveled_color
        self.remaining_color      = remaining_color

        self.percent              = 0.0
        self.distance_label       = ""
        
        self.arrow_img = pygame.image.load("assets/images/spaceship_small_right.png").convert_alpha()

    def set_progress(self, percent: float, distance_label: str):
        self.percent = max(0.0, min(percent, 100.0))
        self.distance_label = distance_label

    def draw(self, surface: pygame.Surface):
        si = self.start_icon
        ei = self.end_icon

        y_offset = (self.height - si.get_height()) / 2
        surface.blit(si, (self.x, self.y + y_offset))
        surface.blit(ei, (self.x + self.width - ei.get_width(),
                        self.y + (self.height - ei.get_height()) / 2))

        bar_x = self.x + si.get_width() + 5
        bar_w = self.width - si.get_width() - ei.get_width() - 10
        bar_y = self.y
        bar_h = self.height

        trav_w = int(bar_w * (self.percent / 100.0))
        pygame.draw.rect(surface, self.traveled_color, (bar_x, bar_y, trav_w, bar_h))
        pygame.draw.rect(surface, self.remaining_color,
                        (bar_x + trav_w, bar_y, bar_w - trav_w, bar_h))
        
        trav_w = int(bar_w * (self.percent / 100))

        arrow_w, arrow_h = self.arrow_img.get_size()
        ax = bar_x + trav_w - arrow_w / 2
        ay = bar_y + (bar_h - arrow_h) / 2
        surface.blit(self.arrow_img, (ax, ay))

        perc_surf = self.font.render(f"{self.percent:.0f}%", True, (255,255,255))
        offset = 10  
        pr = perc_surf.get_rect(center=(bar_x + trav_w, bar_y + bar_h + offset + perc_surf.get_height()/2))
        surface.blit(perc_surf, pr)

        dist_surf = self.font.render(self.distance_label, True, (255,255,255))
        dx = bar_x + bar_w // 2  
        dr = dist_surf.get_rect(midbottom=(dx, bar_y - 5))
        surface.blit(dist_surf, dr)
