import pygame
from core.state_manager import State

from entities.spaceship import Spaceship

class GameplayState(State):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont(None, 48)
        self.spaceship_image = pygame.image.load("assets/images/spaceship.png").convert_alpha()
        self.bullet_image = pygame.image.load("assets/images/bullet.png").convert_alpha()

        self.spaceship = Spaceship(self.spaceship_image, (400, 500))
        self.bullets = pygame.sprite.Group()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Voltando ao menu...")
                if event.key == pygame.K_SPACE:
                    self.spaceship.shoot(self.bullets, self.bullet_image)

    def update(self, dt):
        pressed_keys = pygame.key.get_pressed()
        self.spaceship.update(pressed_keys)
        self.bullets.update()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.bullets.draw(screen)
        screen.blit(self.spaceship.image, self.spaceship.rect)
        text = self.font.render("Gameplay em andamento!", True, (0, 255, 0))
        screen.blit(text, (100, 20))
