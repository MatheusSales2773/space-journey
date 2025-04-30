import pygame
import random

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, image, screen_width):
        super().__init__()
        scale = random.uniform(0.5, 1.5)

        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)

        self.image = pygame.transform.smoothscale(image, (width, height))

        x = random.randint(0, screen_width - width)
        self.rect = self.image.get_rect(topleft=(x, -height))

        self.speed = random.uniform(100, 300)

        def update(self, dt):
            self.rect.y += int(self.speed * dt)
            if self.rect.top > pygame.display.get_surface().get_height():
                self.kill()