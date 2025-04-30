import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, largura_tela, altura_tela):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.largura = largura_tela
        self.altura = altura_tela
        self.reset_position()
    
    def reset_position(self):
        max_x = max(0, self.largura - self.rect.width)  # Garante que o valor não seja negativo
        self.rect.x = random.randint(0, max_x)
        self.rect.y = random.randint(-600, -64)

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > self.altura:
            self.reset_position()

