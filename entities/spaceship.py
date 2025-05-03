import pygame
from entities.bullet import Bullet
import math

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, image, initial_position, shoot_sound, scale=1.0):
        super().__init__()
        
        if scale != 1.0:
            w = int(image.get_width() * scale)
            h = int(image.get_height() * scale)
            image = pygame.transform.smoothscale(image, (w, h))
        
        self.image = image
        self.rect = self.image.get_rect(center=initial_position)
        self.speed = 5
        self.time_from_last_shoot = 0
        self.shoot_gap = 250  # ms

        self.shoot_sound = shoot_sound
        self.shoot_sound.set_volume(0.7)

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if pressed_keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if pressed_keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            
        # Garantir que o foguete não ultrapasse os limites da tela
        self.rect.x = max(0, min(self.rect.x, pygame.display.get_surface().get_width() - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, pygame.display.get_surface().get_height() - self.rect.height))

    def shoot(self, bullet_group, bullet_image):
        now = pygame.time.get_ticks()
        if now - self.time_from_last_shoot > self.shoot_gap:
            self.shoot_sound.play()
            
            bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top, 0.1)
            bullet_group.add(bullet)
            self.time_from_last_shoot = now

    def update_to_center(self, target_x, target_y, speed, dt):
        # Calcular direção para o centro da tela
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            direction_x = dx / distance  # Vetor unitário na direção X
            direction_y = dy / distance  # Vetor unitário na direção Y
        else:
            direction_x, direction_y = 0, 0  # Já está no centro

        # Mover o foguete em direção ao centro
        self.rect.x += int(direction_x * speed * dt)
        self.rect.y += int(direction_y * speed * dt)

        # Verificar se o foguete chegou ao centro (tolerância de 5 pixels)
        if abs(self.rect.centerx - target_x) < 5 and abs(self.rect.centery - target_y) < 5:
            self.rect.centerx = target_x  # Forçar alinhamento horizontal
            self.rect.centery = target_y  # Forçar alinhamento vertical
            return True  # Chegou ao centro
        return False  # Ainda não chegou ao centro