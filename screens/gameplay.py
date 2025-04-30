import pygame

from config import settings
from core.state_manager import State
from entities.spaceship import Spaceship
from screens.menu import MenuState
from entities.enemies import Enemy

class GameplayState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.font = pygame.font.SysFont(None, 48)
        self.spaceship_image = pygame.image.load("assets/images/spaceship.png").convert_alpha()
        self.bullet_image = pygame.image.load("assets/images/bullet.png").convert_alpha()
        self.enemy_image = pygame.image.load("assets/images/enemy.png").convert_alpha()
        
        shoot_sound = pygame.mixer.Sound(settings.SHOOT_SOUND)

        self.spaceship = Spaceship(self.spaceship_image, (400, 500), shoot_sound)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        for _ in range(6):  # Ajuste o número de inimigos conforme necessário
            enemy = Enemy(self.enemy_image, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
            self.enemies.add(enemy)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.set_state(MenuState(self.manager))
                if event.key == pygame.K_SPACE:
                    self.spaceship.shoot(self.bullets, self.bullet_image)

    def update(self, dt):
        pressed_keys = pygame.key.get_pressed()
        self.spaceship.update(pressed_keys)
        self.bullets.update()
        self.enemies.update(3)
        
    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.bullets.draw(screen)
        self.enemies.draw(screen)
        screen.blit(self.spaceship.image, self.spaceship.rect)
        text = self.font.render("Gameplay em andamento!", True, (0, 255, 0))
        screen.blit(text, (100, 20))
