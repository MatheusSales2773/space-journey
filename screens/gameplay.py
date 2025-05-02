import pygame, os, random

from config import settings
from core.state_manager import State
from core.journey_progress import JourneyProgress

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
        if self.transition_stage == 0:
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
            
            # Atualizar a distância percorrida
            travelled = self.speed * dt
            self.distance_remain = max(0, self.distance_remain - travelled)

            percent = (1 - self.distance_remain / self.total_distance) * 100
            dist_km = self.distance_remain / 1_000
            dist_str = f"{dist_km/1e6:.3f} milhões de km"
            self.progress.set_progress(percent, dist_str)
            
            # Verificar colisões entre asteroides e tiros
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
            
            # Verificar se a jornada foi concluída
            if self.distance_remain <= 0 and not self.rocket_animation_active:
                self.rocket_animation_active = True
                self.rocket_animation_timer = 0
                self.transition_stage = 1  # Iniciar a animação do foguete
            
        # Animação do foguete indo para o centro e saindo da tela
        elif self.transition_stage == 1:
            self.rocket_animation_timer += dt
            if self.spaceship.rect.centerx < settings.WINDOW_WIDTH // 2:
                self.spaceship.rect.x += 5  # Mover para o centro horizontalmente
            elif self.spaceship.rect.centery > 0:
                self.spaceship.rect.y -= 5  # Mover para cima
            else:  # Quando estiver no centro (ou próximo), mover para a direita
                self.spaceship.rect.x += 5  # Ajuste a velocidade conforme necessário
                if self.spaceship.rect.left > settings.WINDOW_WIDTH: #Esquerda do rect saiu da tela
                    self.transition_stage = 2
        elif self.rocket_animation_timer > 3:  # Delay de 3 segundos antes da vinheta
                self.transition_stage = 2  # Iniciar a vinheta fechando
                
        # Animação da vinheta fechando
        elif self.transition_stage == 2:
            self.vignette_radius -= 800 * dt  # Velocidade de fechamento
            if self.vignette_radius <= 0:
                # Redimensionar a imagem da superfície para o tamanho da tela
                width, height = pygame.display.get_surface().get_size()
                scaled_surface = pygame.transform.scale(self.surface_image, (width, height))

                # Transição para o próximo estado
                self.manager.set_state(PlanetTransitionState(
                    self.manager,
                    self.planet_name,
                    scaled_surface,  # Usar a imagem redimensionada
                    self.curiosity
        ))

        # Atualizar o progresso
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
                self.hit_timer = self.hit_duration
                exp = Explosion(self.explosion_frames, self.spaceship.rect.center)
                self.explosions.add(exp)

        # Verificar se o player perdeu todas as vidas
        if self.lives <= 0:
            self.manager.set_state(GameOverState(self.manager))
    
        # Atualizar o temporizador de impacto
        if self.hit_timer > 0:
            self.hit_timer -= dt * 1000
            if self.hit_timer < 0:
                self.hit_timer = 0

    def draw(self, screen):
        width, height = screen.get_size()

        # Inicializar o efeito de colisão, se necessário
        if self.hit_effect is None:
            self.hit_effect = pygame.transform.smoothscale(
                self.collision_overlay, (width, height)
            )

        screen.fill((0, 0, 0))
        
        
        # Desenhar o foguete durante a animação
        if self.transition_stage == 1:
            screen.fill((0, 0, 0))  # Limpar a tela
            screen.blit(self.spaceship.image, self.spaceship.rect)
            return  # Não desenhar mais nada durante a animação do foguete

        # Desenhar elementos do jogo apenas se não estiver em transição
        if self.transition_stage == 0:
            # estrelas
            for star in self.stars:
                pos = (int(star["x"]), int(star["y"]))
                pygame.draw.circle(screen, (255, 255, 255), pos, star["r"])

            # elementos do jogo
            self.asteroids.draw(screen)
            self.bullets.draw(screen)
            screen.blit(self.spaceship.image, self.spaceship.rect)
            self.explosions.draw(screen)

            # Efeito de piscar a tela, quando possui uma vida
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

            # corações
            padding = 2
            heart_w = self.heart_image.get_width()
            heart_h = self.heart_image.get_height()
            y = height - heart_h - padding
            for i in range(self.lives):
                x = padding + i * (heart_w + padding)
                screen.blit(self.heart_image, (x, y))

            # barra de progresso
            bar_w, bar_h = self.progress.width, self.progress.height
            self.progress.x = (width - bar_w) // 2
            self.progress.y = 50
            self.progress.draw(screen)
        
        # Desenhar a vinheta durante a transição
        if self.transition_stage == 2:
            vignette_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(
                vignette_surface,
                (0, 0, 0, 255),
                (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2),
                max(0, int(self.vignette_radius))
            )
            screen.blit(vignette_surface, (0, 0))

