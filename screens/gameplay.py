import pygame

from config import settings
from core.state_manager import State
from screens.menu import MenuState

from entities.spaceship import Spaceship
from entities.asteroid import Asteroid

class GameplayState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.font = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE_GAME)

        self.spaceship_image = pygame.image.load("assets/images/spaceship.png").convert_alpha()
        self.bullet_image = pygame.image.load("assets/images/bullet.png").convert_alpha()
        self.asteroid_image = pygame.image.load("assets/images/asteroid.png").convert_alpha()
        
        shoot_sound = pygame.mixer.Sound(settings.SHOOT_SOUND)

        self.score = 0
        self.spaceship = Spaceship(self.spaceship_image, (400, 500), shoot_sound, 0.2)
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

        self.time_since_last_asteroid = 0.0
        self.asteroid_spawn_gap = 1.0

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
        self.asteroids.update(dt)

        self.time_since_last_asteroid += dt
        if self.time_since_last_asteroid >= self.asteroid_spawn_gap:
            width, _ = pygame.display.get_surface().get_size()
            asteroid = Asteroid(self.asteroid_image, width)
            self.asteroids.add(asteroid)
            self.time_since_last_asteroid -= self.asteroid_spawn_gap
        
        if self.score < 1000:  # Limite máximo da barra
            self.score += dt * 100  # Incrementa a distância com base no tempo
            if self.score > 1000:
                 self.score = 1000  # Garante que a distância não ultrapasse o limite

        collisions = pygame.sprite.groupcollide(
            self.asteroids,    # primeiro grupo
            self.bullets,      # segundo grupo
            True,              # mata o asteroide
            True               # mata a bala
        )

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.asteroids.draw(screen)
        self.bullets.draw(screen)
        screen.blit(self.spaceship.image, self.spaceship.rect)
        progress_width = (self.score * (settings.WINDOW_WIDTH * 1.0)) / 1000  # Calcula a largura da barra com base no progresso
        pygame.draw.rect(screen, (255, 255, 255), (settings.WINDOW_WIDTH * 1.2, 20, progress_width, 17)) # A barra de progresso

        distance_text = self.font.render(f"Distância: {int(1000 - self.score)}", True, (255, 255, 255))
        screen.blit(distance_text, (20, 10))  