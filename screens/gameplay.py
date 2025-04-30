import pygame, os

from config import settings
from core.state_manager import State

from screens.menu import MenuState
from screens.gameover import GameOverState

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
        self.heart_image = pygame.image.load("assets/images/heart.png").convert_alpha()
        self.collision_overlay = pygame.image.load("assets/images/collision_overlay.png").convert_alpha()

        self.bg_orig  = pygame.image.load("assets/images/in_game_background.png").convert()

        self.background = None
        
        heart_size = 64
        shoot_sound = pygame.mixer.Sound(settings.SHOOT_SOUND)

        self.hit_effect = None      
        self.hit_duration = 200     
        self.hit_timer    = 0
        self.overlay_blink_interval = 500  
        self.blink_period = 1000  
        self.blink_max_alpha = 200

        self.score = 0
        self.lives = 3

        self.spaceship = Spaceship(self.spaceship_image, (400, 500), shoot_sound, 0.2)
        self.heart_image = pygame.transform.smoothscale(
            self.heart_image,
            (heart_size, heart_size)
        )
        
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

        spaceship_hits = pygame.sprite.spritecollide(self.spaceship, self.asteroids, True)
        if spaceship_hits:
            for _ in spaceship_hits:
                self.lives -= 1
                self.hit_timer = self.hit_duration
                exp = Explosion(self.explosion_frames, self.spaceship.rect.center)
                self.explosions.add(exp)

        if self.lives <= 0:
            self.manager.set_state(GameOverState(self.manager))

        if self.hit_timer > 0:
            self.hit_timer -= dt * 1000
            if self.hit_timer < 0:
                self.hit_timer = 0



    def draw(self, screen):
        width, height = screen.get_size()
        
        if self.background is None:
            self.background = pygame.transform.scale(self.bg_orig, (width, height))

        if self.hit_effect is None:
            self.hit_effect = pygame.transform.smoothscale(
                self.collision_overlay, (width, height)
            )

        screen.blit(self.background, (0, 0))

        self.asteroids.draw(screen)
        self.bullets.draw(screen)
        screen.blit(self.spaceship.image, self.spaceship.rect)

        self.explosions.draw(screen)

        score_hud = self.font.render("Pontuação: " + str(self.score), True, (0, 255, 0))

        if self.lives == 1:
            t = pygame.time.get_ticks() % self.blink_period
            half = self.blink_period / 2

            if t <= half:
                alpha = int((t / half) * self.blink_max_alpha)
            else:
                alpha = int(((self.blink_period - t) / half) * self.blink_max_alpha)

            overlay = self.hit_effect.copy()
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))

        elif self.hit_timer > 0:
            alpha = int(self.hit_timer / self.hit_duration * 255)
            overlay = self.hit_effect.copy()
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))
        
        padding = 10          # espaço entre corações
        x = 10                # margem esquerda
        y = 50                # margem topo
        for i in range(self.lives):
            screen.blit(self.heart_image, (x + i * (64 + padding), y))
            screen.blit(score_hud, (100, 20))
