import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale):
        super().__init__()

        if scale != 1.0:
            w = int(image.get_width() * scale)
            h = int(image.get_height() * scale)
            image = pygame.transform.smoothscale(image, (w, h))

        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10  

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()  