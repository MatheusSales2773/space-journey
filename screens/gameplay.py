import pygame, os, random

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

        # ─── 1. Font e sons ─────────────────────────────────────
        self.font = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE_GAME)
        self.shoot_sound = pygame.mixer.Sound(settings.SHOOT_SOUND)

        # ─── 2. Carregamento de imagens ─────────────────────────
        # Sprite principal
        self.spaceship_image = pygame.image.load(
            "assets/images/spaceship.png"
        ).convert_alpha()
        self.bullet_image = pygame.image.load(
            "assets/images/bullet.png"
        ).convert_alpha()
        self.asteroid_image = pygame.image.load(
            "assets/images/asteroid.png"
        ).convert_alpha()
        self.heart_image = pygame.image.load(
            "assets/images/heart.png"
        ).convert_alpha()
        self.collision_overlay = pygame.image.load(
            "assets/images/collision_overlay.png"
        ).convert_alpha()
        self.bg_orig = pygame.image.load(
            "assets/images/in_game_background.png"
        ).convert()

        # ─── 3. Preparar e escalar imagens derivadas ────────────
        # hearts
        heart_size = 64
        self.heart_image = pygame.transform.smoothscale(
            self.heart_image, (heart_size, heart_size)
        )

        self.background = None
        self.hit_effect = None

        # ─── 4. Configuração de efeito de colisão ──────────────
        self.hit_duration = 200            # ms de fade-out
        self.hit_timer = 0
        self.blink_period = 1000           # ms de ciclo na última vida
        self.blink_max_alpha = 200

        # ─── 5. Estado do jogador ───────────────────────────────
        self.score = 0
        self.lives = 3

        # ─── 6. Instanciar a Spaceship ──────────────────────────
        # escala embutida de 0.2 dentro do Spaceship
        self.spaceship = Spaceship(
            self.spaceship_image,
            (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 100),
            self.shoot_sound,
            shoot_gap=250,
            scale=0.2
        )

        # ─── 7. Estrelas ────────────────────────────
        width, height = pygame.display.get_surface().get_size()
        self.stars = []
        for _ in range(settings.NUM_STARS):
            self.stars.append({
                "x": random.uniform(0, width),
                "y": random.uniform(0, height),
                "speed": random.uniform(*settings.STAR_SPEED_RANGE),
                "r": random.randint(*settings.STAR_RADIUS_RANGE),
            })

        # ─── 8. Grupos de sprites e timers ──────────────────────
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.time_since_last_asteroid = 0.0
        self.asteroid_spawn_gap = 1.0     # segundos entre spawns

        # ─── 9. Frames de explosão ──────────────────────────────
        folder = "assets/images/explosion"
        self.explosion_frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                img = pygame.image.load(
                    os.path.join(folder, filename)
                ).convert_alpha()
                self.explosion_frames.append(img)

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

        width, height = pygame.display.get_surface().get_size()
        for star in self.stars:
            star["y"] += star["speed"] * dt
            if star["y"] > height:
                star["y"] = 0
                star["x"] = random.uniform(0, width)

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

        # if self.background is None:
        #     self.background = pygame.transform.scale(self.bg_orig, (width, height))
        if self.hit_effect is None:
            self.hit_effect = pygame.transform.smoothscale(
                self.collision_overlay, (width, height)
            )

        # screen.blit(self.background, (0, 0))

        screen.fill((0, 0, 0))

        for star in self.stars:
            pos = (int(star["x"]), int(star["y"]))
            pygame.draw.circle(screen, (255, 255, 255), pos, star["r"])

        self.asteroids.draw(screen)
        self.bullets.draw(screen)
        screen.blit(self.spaceship.image, self.spaceship.rect)
        self.explosions.draw(screen)

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

        padding = 10
        heart_w = self.heart_image.get_width()
        y = 50
        for i in range(self.lives):
            x = 10 + i * (heart_w + padding)
            screen.blit(self.heart_image, (x, y))

        score_hud = self.font.render(f"Pontuação: {self.score}", True, (0, 255, 0))
        screen.blit(score_hud, (100, 20))
