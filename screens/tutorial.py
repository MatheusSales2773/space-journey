import pygame
from config import settings

from core.huds.tutorial_hud import TutorialHUD
from core.state_manager import State
from screens.gameplay import GameplayState

target = {"name": "MERCÚRIO", "image": "assets/images/planets/mercury.png", "distance": 77_000_000, "speed": 300_000,
             "curiosity": "Mercúrio é o menor planeta do sistema solar e o mais próximo do Sol.",
             "surface_image": "assets/images/surfaces/mercury_surface.png"}

class TutorialState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        screen_w, screen_h = pygame.display.get_surface().get_size()

        # --- MODIFICAÇÃO INICIA ---
        # Carrega a mesma imagem de nave da gameplay ('spaceship.png')
        # A imagem 'spaceship_static.png' foi trocada para garantir consistência visual.
        self.spaceship_img = pygame.image.load('assets/images/spaceship.png').convert_alpha()
        
        # A nave do tutorial tem uma escala maior no início.
        self.tutorial_scale = 0.5
        
        # Redimensiona a imagem para a escala do tutorial
        w = int(self.spaceship_img.get_width() * self.tutorial_scale)
        h = int(self.spaceship_img.get_height() * self.tutorial_scale)
        self.scaled_spaceship_img = pygame.transform.smoothscale(self.spaceship_img, (w,h))
        
        self.spaceship_rect = self.scaled_spaceship_img.get_rect(
            center=(screen_w // 2, screen_h // 2 + 100)
        )
        # --- MODIFICAÇÃO TERMINA ---

        # Carrega e escala a imagem de fundo
        img = pygame.image.load(
            "assets/images/backgrounds/earth_lift_off_bg.png"
        ).convert()
        img_w, img_h = img.get_size()
        scale = screen_w / img_w
        self.tutorial_img = pygame.transform.smoothscale(
            img, (screen_w, int(img_h * scale))
        )

        self.screen_h = screen_h
        self.max_offset = max(0, self.tutorial_img.get_height() - screen_h)

        self.y_offset = self.max_offset
        self.is_scrolling = False
        self.current_speed = 0.0
        self.target_speed = self.max_offset / 15.0 # Um pouco mais rápido

        accel_time = 8.0 # Aceleração mais rápida
        self.acceleration = self.target_speed / accel_time

        self.font = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE_GAME)
        self.hud = TutorialHUD(speed=0, altitude=0, is_scrolling=False)

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and not self.is_scrolling:
                    self.hud.start_countdown()

    def update(self, dt):
        if self.hud.is_scrolling and self.y_offset > 0:
            self.is_scrolling = True

            if self.current_speed < self.target_speed:
                self.current_speed = min(
                    self.target_speed,
                    self.current_speed + self.acceleration * dt
                )
            self.y_offset -= self.current_speed * dt
            if self.y_offset < 0:
                self.y_offset = 0

        # --- MODIFICAÇÃO INICIA ---
        # Quando o scroll do fundo termina, inicia a transição para a gameplay
        if self.is_scrolling and self.y_offset == 0 and not self.hud.countdown_active:
            
            # Pega a posição final da nave no tutorial e sua escala
            final_pos = self.spaceship_rect.center
            
            # Chama o GameplayState com os parâmetros para a animação
            self.manager.set_state(GameplayState(
                self.manager,
                target["name"],
                target["distance"],
                target["speed"],
                target["curiosity"],
                target["surface_image"],
                from_tutorial=True,          # ATIVA a animação de entrada
                initial_pos=final_pos,       # Define a posição inicial da animação
                initial_scale=self.tutorial_scale  # Define a escala inicial
            ))
        # --- MODIFICAÇÃO TERMINA ---

        progresso = (self.max_offset - self.y_offset) / self.max_offset if self.max_offset else 1
        altitude_km = progresso * 100.0

        self.hud.update(
            speed=self.current_speed,
            altitude=altitude_km,
            is_scrolling=self.is_scrolling
        )

    def draw(self, screen):
        screen.blit(self.tutorial_img, (0, -int(self.y_offset)))
        
        # Usa a imagem da nave já redimensionada para o tutorial
        screen.blit(self.scaled_spaceship_img, self.spaceship_rect)
        self.hud.draw(screen)
