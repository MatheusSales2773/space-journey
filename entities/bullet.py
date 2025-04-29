import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10  # sobe na tela

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()  # remove se sair da tela