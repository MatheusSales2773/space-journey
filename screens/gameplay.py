import pygame, os

from config import settings
from core.state_manager import State
from screens.menu import MenuState

from entities.spaceship import Spaceship
from entities.asteroid import Asteroid
from entities.explosion import Explosion

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

        folder = 'assets/images/explosion'
        self.explosion_frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith('.png'):
                img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                self.explosion_frames.append(img)

        self.explosions = pygame.sprite.Group()

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

        collisions = pygame.sprite.groupcollide(
            self.asteroids,    
            self.bullets,     
            True,              
            True               
        )

        if collisions:
            for asteroid_sprite in collisions.keys():
                exp = Explosion(self.explosion_frames, asteroid_sprite.rect.center)
                self.explosions.add(exp)
                self.score += 10

        self.explosions.update(dt)


    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.asteroids.draw(screen)
        self.bullets.draw(screen)
        screen.blit(self.spaceship.image, self.spaceship.rect)

        self.explosions.draw(screen)

        text = self.font.render("Pontuação: " + str(self.score), True, (0, 255, 0))
        screen.blit(text, (100, 20))
