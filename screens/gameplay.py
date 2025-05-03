import pygame, os, random, math

from config import settings
from core.state_manager import State
from core.journey_progress import JourneyProgress
from core.hud import HUD

from screens.menu import MenuState
from screens.gameover import GameOverState
from screens.planet_transition import PlanetTransitionState

from entities.spaceship import Spaceship
from entities.asteroid import Asteroid
from entities.explosion import Explosion

class GameplayState(State):
    def __init__(self, manager, planet_name, distance, speed, curiosity, surface_image_path):
        super().__init__()
        self.manager = manager
        self.planet_name = planet_name
        self.distance = distance
        self.speed = speed
        
        self.transition_stage = 0  # 0: gameplay, 1: foguete animando, 2: vinheta fechando
        self.transition_timer = 0  # Temporizador para controlar os delays
        self.vignette_radius = max(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)  # Para a vinheta
        self.curiosity = curiosity
        self.surface_image = pygame.image.load(surface_image_path).convert_alpha()
        
        self.rocket_animation_active = False  # Controla se a animação está ativa
        self.rocket_animation_timer = 0  # Temporizador para a animação
        
        self.rocket_target = (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)  # Centro da tela
        self.rocket_exit_speed = 500  # Velocidade de saída do foguete
        self.rocket_direction = None  # Direção do movimento do foguete
        
        # Multiplicador global para aumentar a velocidade das fases
        global_speed_multiplier = 6500.0  # Aumente este valor para acelerar mais as fases, mudem aqui se necessário
        self.speed = speed * global_speed_multiplier

        # ─── 1. Font e sons ─────────────────────────────────────
        self.font = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE_GAME)
        self.font_alt = pygame.font.Font(settings.FONT_ALT_PATH, settings.FONT_SIZE_SMALL)
        self.shoot_sound = pygame.mixer.Sound(settings.SHOOT_SOUND)
        screen_size = pygame.display.get_surface().get_size()

        # ─── 2. Carregamento de imagens ───────────────────────────────
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
        self.bg_orig = pygame.image.load(
            "assets/images/in_game_background.png"
        ).convert()
        self.flag_icon = pygame.image.load(
            "assets/images/start_flag.png"
        ).convert_alpha()
        self.planet_icon = pygame.image.load(
            "assets/images/earth_small.png"
        ).convert_alpha()

        # ─── 3. Preparar e escalar imagens derivadas ─────────────────────────
        self.hit_effect = None
        
        self.total_distance = self.distance * 1_000  # Converter para metros
        self.distance_remain = self.total_distance
        self.ship_speed = 500_000_00

        # ─── 5. Estado do jogador ───────────────────────────────────
        self.score = 0
        self.lives = 3

        # ─── 6. Instancias ──────────────────────────
        self.spaceship = Spaceship(
            self.spaceship_image,
            (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 100),
            self.shoot_sound,
            scale=0.2
        )
        
        self.progress = JourneyProgress(
            start_icon=self.flag_icon,
            end_icon=self.planet_icon,
        )

        self.hud = HUD(self.progress, self.font, screen_size, planet_name)

        # ─── 7. Estrelas ─────────────────────────
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

        # ─── 9. Frames de explosão ───────────────────────────
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
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Clique detectado (implementar lógica, se necessário)")

    def update(self, dt):
        pressed_keys = pygame.key.get_pressed()
        self.spaceship.update(pressed_keys)
        self.bullets.update()
        self.asteroids.update(dt)
        self.hud.update_hit_effect(dt, self.lives)

        self.time_since_last_asteroid += dt
        if self.time_since_last_asteroid >= self.asteroid_spawn_gap:
            width, _ = pygame.display.get_surface().get_size()
            asteroid = Asteroid(self.asteroid_image, width)
            self.asteroids.add(asteroid)
            self.time_since_last_asteroid -= self.asteroid_spawn_gap
        
        travelled = self.ship_speed * dt
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

        percent = (1 - self.distance_remain / self.total_distance) * 100
        dist_km = self.distance_remain / 1_000
        dist_str = f"{dist_km / 1e6:.3f} milhões de km"
        self.progress.set_progress(percent, dist_str)

        # atualizar estelas
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
                self.hud.start_hit()
                exp = Explosion(self.explosion_frames, self.spaceship.rect.center)
                self.explosions.add(exp)

            if self.lives <= 0:
                self.manager.set_state(GameOverState(self.manager))

    def draw(self, screen):
        width, height = screen.get_size()
        
        screen.fill((10, 10, 10))
        
        for star in self.stars:
            pos = (int(star["x"]), int(star["y"]))
            pygame.draw.circle(screen, (255, 255, 255), pos, star["r"])

        self.asteroids.draw(screen)
        self.bullets.draw(screen)
        screen.blit(self.spaceship.image, self.spaceship.rect)
        self.explosions.draw(screen)

        self.hud.draw(screen, self.lives, width, height)
