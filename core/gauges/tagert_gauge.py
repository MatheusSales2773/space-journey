import pygame

class TargetGauge:
    def __init__(self, bg_image_path, font_path, font_size, planet_name):
        self.bg_image = pygame.image.load(bg_image_path).convert_alpha()
        self.font = pygame.font.Font(font_path, font_size)
        self.planet_name = planet_name

        self.x = 0
        self.y = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface, padding=42):
        screen_w, screen_h = surface.get_size()
        hud_w, hud_h = self.bg_image.get_size()

        self.x = screen_w - hud_w - padding
        self.y = screen_h - hud_h - padding

        # Fundo
        surface.blit(self.bg_image, (self.x, self.y))

        # Texto
        label = self.font.render("MISSÃO", True, (201, 201, 201))
        label_rect = label.get_rect(center=(self.x + hud_w // 2, self.y + 20))
        surface.blit(label, label_rect)

        label = self.font.render(self.planet_name, True, (201, 201, 201))
        label_rect = label.get_rect(center=(self.x + hud_w // 2, self.y + 50))
        surface.blit(label, label_rect)