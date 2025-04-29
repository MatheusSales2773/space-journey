import pygame
from entities.bullet import Bullet

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, image, initial_position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=initial_position)
        self.speed = 5
        self.time_from_last_shoot = 0
        self.shoot_gap = 250 #ms

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if pressed_keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if pressed_keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def shoot(self, bullet_group, bullet_image):
        now = pygame.time.get_ticks()
        if now - self.time_from_last_shoot > self.shoot_gap:
            bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.time_from_last_shoot = now