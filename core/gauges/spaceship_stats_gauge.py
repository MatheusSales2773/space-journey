import pygame

class SpaceshipStatsGauge:
    def __init__(self, bg_image_path, font_path, font_size, speed, altitude):
        self.font = pygame.font.Font(font_path, font_size)
        self.text = pygame.font.Font(font_path, 36)
        self.bg_image = pygame.image.load(bg_image_path).convert_alpha()
        self.speed = speed
        self.altitude = altitude

        self.x = 0
        self.y = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def update_lives(self, lives):
        pass

    def set_speed(self, speed):
        self.speed = speed

    def set_altitude(self, altitude):
        self.altitude = altitude

    def draw(self, surface, padding=42, use_preset_position=False):
        if not use_preset_position:
            screen_w, screen_h = surface.get_size()
            hud_w, hud_h = self.bg_image.get_size()

            self.x = screen_w - hud_w - padding
            self.y = screen_h - hud_h - padding

        surface.blit(self.bg_image, (self.x, self.y))

        # Altitude
        altitude_label = self.font.render("ALTITUDE", True, (201, 201, 201))
        altitude_label_rect = altitude_label.get_rect(midleft=(self.x + 50, self.y + 30))
        surface.blit(altitude_label, altitude_label_rect)

        altitude_int = int(self.altitude)

        speed_text = self.text.render(str(altitude_int) + " KM", True, (255, 255, 255))
        speed_text_rect = speed_text.get_rect(midright=(self.x + 240, self.y + 32))
        surface.blit(speed_text, speed_text_rect)

        # Speed
        speed_label = self.font.render("VELOCIDADE", True, (201, 201, 201))
        speed_label_rect = speed_label.get_rect(midleft=(self.x - 30, self.y + 74))
        surface.blit(speed_label, speed_label_rect)

        speed_int = int(self.speed)

        altitude_text = self.text.render(str(speed_int) + " KM/H", True, (255, 255, 255))
        altitude_text_rect = altitude_text.get_rect(midright=(self.x + 220, self.y + 74))
        surface.blit(altitude_text, altitude_text_rect)