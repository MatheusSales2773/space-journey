import pygame, os, random

from config import settings
from core.state_manager import State
from core.journey_progress import JourneyProgress

from screens.menu import MenuState
from screens.gameover import GameOverState

from entities.spaceship import Spaceship
from entities.asteroid import Asteroid
from entities.explosion import Explosion

class GameplayState(State):
    def __init__(self, manager, planet_name, distance, speed):
        super().__init__()
        self.manager = manager
        self.planet_name = planet_name
        self.distance = distance
        self.speed = speed
        
        # Multiplicador global para aumentar a velocidade das fases
        global_speed_multiplier = 6500.0  # Aumente este valor para acelerar mais as fases, mudem aqui se necessário
        self.speed = speed * global_speed_multiplier

        # ─── 1. Font e sons ─────────────────────────────────────
        self.font = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE_GAME)
        self.font_alt = pygame.font.Font(settings.FONT_ALT_PATH, settings.FONT_SIZE_SMALL)
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
        self.flag_icon = pygame.image.load(
            "assets/images/start_flag.png"
        ).convert_alpha()
        self.planet_icon = pygame.image.load(
            "assets/images/earth_small.png"
        ).convert_alpha()

        # ─── 3. Preparar e escalar imagens derivadas ────────────
        # hearts
        heart_size = 96
        self.heart_image = pygame.transform.smoothscale(
            self.heart_image, (heart_size, heart_size)
        )

        self.hit_effect = None
        
        self.total_distance = self.distance * 1_000  # Converter para metros
        self.distance_remain = self.total_distance
        self.ship_speed = 500_000_00

        # ─── 4. Configuração de efeito de colisão ──────────────
        self.hit_duration = 200            # ms de fade-out
        self.hit_timer = 0
        self.blink_period = 1000           # ms de ciclo na última vida
        self.blink_max_alpha = 200

        # ─── 5. Estado do jogador ───────────────────────────────
        self.score = 0
        self.lives = 3

        # ─── 6. Instancias ──────────────────────────
        # escala embutida de 0.2 dentro do Spaceship
        self.spaceship = Spaceship(
            self.spaceship_image,
            (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 100),
            self.shoot_sound,
            scale=0.2
        )
        
        self.progress = JourneyProgress(
            position=(0, 0),         
            size=(800, 14),      
            start_icon=self.flag_icon,
            end_icon=self.planet_icon,
            font=self.font_alt
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
                    from screens.pause import PauseState
                    self.manager.set_state(PauseState(self.manager))
                if event.key == pygame.K_SPACE:
                    self.spaceship.shoot(self.bullets, self.bullet_image)
            elif event.type == pygame.KEYUP:
                # Exemplo: Lógica para soltar teclas, se necessário
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique esquerdo do mouse
                    print("Clique detectado (implementar lógica, se necessário)")

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
        
        travelled = self.speed * dt
        self.distance_remain = max(0, self.distance_remain - travelled)


        percent = (1 - self.distance_remain / self.total_distance) * 100

        dist_km = self.distance_remain / 1_000
        dist_str = f"{dist_km/1e6:.3f} milhões de km"
        self.progress.set_progress(percent, dist_str)
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
        
        travelled = self.ship_speed * dt
        self.distance_remain = max(0, self.distance_remain - travelled)
        
        # Verificar se a jornada foi concluída
        if self.distance_remain <= 0:
            self.manager.set_state(MenuState(self.manager))  # Voltar ao menu ou próximo estado

        percent = (1 - self.distance_remain / self.total_distance) * 100

        dist_km = self.distance_remain / 1_000
        dist_str = f"{dist_km/1e6:.3f} milhões de km"
        self.progress.set_progress(percent, dist_str)

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

        if self.hit_effect is None:
            self.hit_effect = pygame.transform.smoothscale(
                self.collision_overlay, (width, height)
            )

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

        padding = 2
        heart_w = self.heart_image.get_width()
        heart_h = self.heart_image.get_height()

        y = height - heart_h - padding

        for i in range(self.lives):
            x = padding + i * (heart_w + padding)
            screen.blit(self.heart_image, (x, y))


        bar_w, bar_h = self.progress.width, self.progress.height
        self.progress.x = (width - bar_w) // 2
        self.progress.y = 50
        self.progress.draw(screen)

