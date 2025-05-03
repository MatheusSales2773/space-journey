import pygame
from config import settings
from core.state_manager import State
from screens.gameplay import GameplayState

class TutorialState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager      = manager
        self.scroll_speed = 250
        self.is_scrolling = False

        screen_w, screen_h = pygame.display.get_surface().get_size()

        # Spaceship
        initial_position = (screen_w // 2 - 70, screen_h // 2 + 100)
        self.spaceship = pygame.image.load('assets/images/spaceship_static.png').convert_alpha()
        self.rect = self.spaceship.get_rect(center=initial_position)

        # Carrega e escala a imagem para preencher horizontalmente
        img = pygame.image.load(
            "assets/images/backgrounds/earth_lift_off_bg.png"
        ).convert()
        img_w, img_h = img.get_size()
        scale = screen_w / img_w
        self.tutorial_img = pygame.transform.smoothscale(
            img, (screen_w, int(img_h * scale))
        )

        # Guarda altura da tela e calcula offset máximo
        self.screen_h   = screen_h
        self.max_offset = max(0, self.tutorial_img.get_height() - screen_h)
        # Começa mostrando o final da imagem (offset máximo)
        self.y_offset   = self.max_offset

        self.font = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE_GAME)

        self.msg = "Pressione ESPAÇO para iniciar o scroll"
        self.start_msg = "Pressione ENTER para começar"


    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and not self.is_scrolling:
                    self.is_scrolling = True
                    self.msg = self.start_msg
                elif e.key in (pygame.K_RETURN, pygame.K_ESCAPE) and self.y_offset == 0:
                    self.manager.set_state(GameplayState(self.manager))

    def update(self, dt):
        if self.is_scrolling and self.y_offset > 0:
            self.y_offset -= self.scroll_speed * dt
            if self.y_offset < 0:
                self.y_offset = 0

    def draw(self, screen):
        screen.blit(self.tutorial_img, (0, -int(self.y_offset)))

        if self.y_offset == 0:
            text_surf = self.font.render(self.msg, True, (255, 255, 255))
            text_rect = text_surf.get_rect(
                midbottom=(screen.get_width() // 2, self.screen_h - 20)
            )
            screen.blit(text_surf, text_rect)

        screen.blit(self.spaceship, self.rect)