import pygame

class ShipIntegrityGauge:
    def __init__(self, bg_image_path, heart_image_path, font_path, font_size, max_lives):
        self.bg_image = pygame.image.load(bg_image_path).convert_alpha()
        self.heart_image = pygame.image.load(heart_image_path).convert_alpha()
        self.font = pygame.font.Font(font_path, font_size)
        self.max_lives = max_lives
        self.lives = max_lives

        self.x = 0
        self.y = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def update_lives(self, lives):
        self.lives = max(0, min(self.max_lives, lives))

    def draw(self, surface, padding=42):
        screen_w, screen_h = surface.get_size()
        hud_w, hud_h = self.bg_image.get_size()

        self.x = screen_w - hud_w - padding
        self.y = screen_h - hud_h - padding

        # Fundo
        surface.blit(self.bg_image, (self.x, self.y))

        # Texto
        label = self.font.render("INTEGRIDADE DA NAVE", True, (201, 201, 201))
        label_rect = label.get_rect(center=(self.x + hud_w // 2, self.y + 20))
        surface.blit(label, label_rect)

        # Corações
        heart_w, heart_h = self.heart_image.get_size()
        total_width = self.lives * heart_w + (self.lives - 1) * 5
        start_x = self.x + (hud_w - total_width) // 2
        heart_y = self.y + hud_h - heart_h - 25

        for i in range(self.lives):
            surface.blit(self.heart_image, (start_x + i * (heart_w + 5), heart_y))