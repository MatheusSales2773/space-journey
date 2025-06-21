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
    def __init__(self, manager, planet_name, distance, speed, curiosity, surface_image_path, 
                 from_tutorial=False, initial_pos=None, initial_scale=None):
        super().__init__()
        self.manager = manager
        self.planet_name = planet_name
        self.distance = distance
        
        self.is_entry_animation = from_tutorial
        self.entry_animation_timer = 0.0
        self.entry_animation_duration = 1.5

        self.transition_stage = 0
        self.transition_timer = 0
        self.vignette_radius = max(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        self.curiosity = curiosity
        self.surface_image = pygame.image.load(surface_image_path).convert_alpha()
        
        self.rocket_animation_active = False
        self.rocket_animation_timer = 0
        
        self.rocket_target = (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)
        self.rocket_exit_speed = 700
        self.rocket_direction = None
        
        global_speed_multiplier = 6500.0
        self.speed = speed * global_speed_multiplier

        self.hit_duration = 1.0
        
        self.font = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE_GAME)
        self.font_alt = pygame.font.Font(settings.FONT_ALT_PATH, settings.FONT_SIZE_SMALL)
        self.shoot_sound = pygame.mixer.Sound(settings.SHOOT_SOUND)
        screen_size = pygame.display.get_surface().get_size()

        # --- MODIFICAÇÃO ---
        # A linha que carregava a imagem da nave foi removida daqui.
        # self.spaceship_image = pygame.image.load(...) << REMOVIDO
        
        self.bullet_image = pygame.image.load("assets/images/bullet.png").convert_alpha()
        self.asteroid_image = pygame.image.load("assets/images/asteroid.png").convert_alpha()
        self.bg_orig = pygame.image.load("assets/images/in_game_background.png").convert()
        self.flag_icon = pygame.image.load("assets/images/start_flag.png").convert_alpha()
        self.planet_icon = pygame.image.load("assets/images/earth_small.png").convert_alpha()

        self.hit_effect = None
        self.total_distance = self.distance * 1_000
        self.distance_remain = self.total_distance
        self.ship_speed = 8_500_000_00

        self.score = 0
        self.lives = 3

        self.gameplay_start_pos = (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 100)
        self.gameplay_target_scale = 0.2
        
        start_pos = initial_pos if from_tutorial else self.gameplay_start_pos
        start_scale = initial_scale if from_tutorial else self.gameplay_target_scale
        
        self.initial_anim_pos = initial_pos
        self.initial_anim_scale = initial_scale

        # --- MODIFICAÇÃO ---
        # A imagem não é mais passada para o construtor da Spaceship.
        self.spaceship = Spaceship(
            initial_position=start_pos,
            shoot_sound=self.shoot_sound,
            scale=start_scale
        )
        
        self.progress = JourneyProgress(start_icon=self.flag_icon, end_icon=self.planet_icon)
        self.hud = HUD(self.progress, self.font, screen_size, planet_name)

        width, height = pygame.display.get_surface().get_size()
        self.stars = []
        for _ in range(settings.NUM_STARS):
            self.stars.append({
                "x": random.uniform(0, width), "y": random.uniform(0, height),
                "speed": random.uniform(*settings.STAR_SPEED_RANGE), "r": random.randint(*settings.STAR_RADIUS_RANGE)
            })

        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.time_since_last_asteroid = 0.0
        self.asteroid_spawn_gap = 1.0

        folder = "assets/images/explosion"
        self.explosion_frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                self.explosion_frames.append(img)

    def handle_events(self, events):
        if self.is_entry_animation:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from screens.pause import PauseState
                    self.manager.set_state(PauseState(self.manager))
                if event.key == pygame.K_SPACE:
                    self.spaceship.shoot(self.bullets, self.bullet_image)

    def update(self, dt):
        if self.is_entry_animation:
            self.entry_animation_timer += dt
            progress = min(1.0, self.entry_animation_timer / self.entry_animation_duration)
            progress = 1 - (1 - progress)**3

            start_x, start_y = self.initial_anim_pos
            target_x, target_y = self.gameplay_start_pos
            current_x = start_x + (target_x - start_x) * progress
            current_y = start_y + (target_y - start_y) * progress
            self.spaceship.rect.center = (current_x, current_y)

            start_scale = self.initial_anim_scale
            target_scale = self.gameplay_target_scale
            current_scale = start_scale + (target_scale - start_scale) * progress
            self.spaceship.set_scale(current_scale)

            if progress >= 1.0:
                self.is_entry_animation = False
            
            self.update_stars(dt)
            self.hud.update_hit_effect(dt, self.lives)
            return

        if self.distance_remain <= 0 and not self.rocket_animation_active:
            self.rocket_animation_active = True
            self.transition_stage = 1
            self.rocket_direction = None
            return

        if self.transition_stage == 1:
            if self.rocket_direction is None:
                if self.spaceship.update_to_center(self.rocket_target[0], self.rocket_target[1], self.rocket_exit_speed, dt):
                    self.rocket_direction = (0, -1)
            if self.rocket_direction is not None:
                self.spaceship.rect.y += self.rocket_direction[1] * self.rocket_exit_speed * dt
            if self.spaceship.rect.bottom < 0:
                self.transition_stage = 2
            return
        elif self.transition_stage == 2:
            self.vignette_radius -= 800 * dt
            if self.vignette_radius <= 0:
                width, height = settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT
                scaled_surface = pygame.transform.scale(self.surface_image, (width, height))
                self.manager.set_state(PlanetTransitionState(
                    self.manager, self.planet_name, scaled_surface, self.curiosity
                ))
            return

        pressed_keys = pygame.key.get_pressed()
        self.spaceship.update(pressed_keys)
        self.bullets.update()
        self.asteroids.update(dt)
        self.hud.update_hit_effect(dt, self.lives)
        self.update_stars(dt)

        self.time_since_last_asteroid += dt
        if self.time_since_last_asteroid >= self.asteroid_spawn_gap:
            width, _ = pygame.display.get_surface().get_size()
            self.asteroids.add(Asteroid(self.asteroid_image, width))
            self.time_since_last_asteroid = 0

        travelled = self.ship_speed * dt
        self.distance_remain = max(0, self.distance_remain - travelled)
        percent = (1 - self.distance_remain / self.total_distance) * 100
        dist_km = self.distance_remain / 1_000
        dist_str = f"{dist_km / 1e6:.3f} milhões de km"
        self.progress.set_progress(percent, dist_str)

        collisions = pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True)
        if collisions:
            for asteroid_sprite in collisions.keys():
                self.explosions.add(Explosion(self.explosion_frames, asteroid_sprite.rect.center))
                self.score += 10
        self.explosions.update(dt)

        spaceship_hits = pygame.sprite.spritecollide(self.spaceship, self.asteroids, True)
        if spaceship_hits:
            for _ in spaceship_hits:
                self.lives -= 1
                self.hud.start_hit()
                self.explosions.add(Explosion(self.explosion_frames, self.spaceship.rect.center))
                if self.lives <= 0:
                    self.manager.set_state(GameOverState(self.manager))
                        
    def update_stars(self, dt):
        width, height = pygame.display.get_surface().get_size()
        for star in self.stars:
            star["y"] += star["speed"] * dt
            if star["y"] > height:
                star["y"] = 0
                star["x"] = random.uniform(0, width)

    def draw(self, screen):
        width, height = screen.get_size()
        screen.fill((0, 0, 0))

        if self.transition_stage == 1:
            screen.blit(self.spaceship.image, self.spaceship.rect)
            return

        if self.transition_stage == 2:
            vignette_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(
                vignette_surface, (0, 0, 0, 255),
                (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2),
                max(0, int(self.vignette_radius))
            )
            vignette_surface.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MIN)
            screen.blit(vignette_surface, (0, 0))
            return

        if self.transition_stage == 0:
            for star in self.stars:
                pygame.draw.circle(screen, (255, 255, 255), (int(star["x"]), int(star["y"])), star["r"])

            if not self.is_entry_animation:
                self.asteroids.draw(screen)
                self.bullets.draw(screen)
                self.explosions.draw(screen)

            screen.blit(self.spaceship.image, self.spaceship.rect)

        self.hud.draw(screen, self.lives, width, height)
