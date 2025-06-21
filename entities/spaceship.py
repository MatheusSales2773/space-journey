import pygame
from entities.bullet import Bullet
import math

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, initial_position, shoot_sound, scale=1.0):
        super().__init__()
        
        # --- MODIFICAÇÃO INICIA ---
        # Guarda a imagem original, sem escala, para referência.
        # Isto é crucial para que o redimensionamento seja sempre a partir do original.
        self.original_image = pygame.image.load("assets/images/spaceship.png").convert_alpha()
        
        # A posição inicial do rect será definida após o primeiro redimensionamento
        self.rect = self.original_image.get_rect(center=initial_position)
        
        # Aplica a escala inicial usando o novo método
        self.set_scale(scale)
        # --- MODIFICAÇÃO TERMINA ---

        self.speed = 5
        self.time_from_last_shoot = 0
        self.shoot_gap = 250  # ms

        self.shoot_sound = shoot_sound
        self.shoot_sound.set_volume(0.7)

    # --- NOVO MÉTODO ---
    def set_scale(self, scale):
        # Mantém o centro atual da nave para que ela não "salte" ao ser redimensionada.
        center = self.rect.center
        
        w = int(self.original_image.get_width() * scale)
        h = int(self.original_image.get_height() * scale)
        
        self.image = pygame.transform.smoothscale(self.original_image, (w, h))
        
        # Recria o rect com o novo tamanho, mas no mesmo centro.
        self.rect = self.image.get_rect(center=center)

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
        width, height = pygame.display.get_surface().get_size()
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(width, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(height, self.rect.bottom)

    def shoot(self, bullet_group, bullet_image):
        now = pygame.time.get_ticks()
        if now - self.time_from_last_shoot > self.shoot_gap:
            self.shoot_sound.play()
            
            bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top, 0.1)
            bullet_group.add(bullet)
            self.time_from_last_shoot = now

    def update_to_center(self, target_x, target_y, speed, dt):
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 1.0: # Adicionada uma pequena margem para evitar "tremer"
            direction_x = dx / distance
            direction_y = dy / distance
            self.rect.x += direction_x * speed * dt
            self.rect.y += direction_y * speed * dt
        else:
            self.rect.center = (target_x, target_y)
            return True # Chegou ao centro
        return False
