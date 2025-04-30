import pygame

from config import settings
from core.state_manager import State

class GameOverState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.font = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE_MENU)
        self.font_desc = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE_GAME)

        self.bg_orig  = pygame.image.load("assets/images/bg.png").convert()
        self.game_over_orig = pygame.image.load("assets/images/game_over.png").convert_alpha()

        self.background = None
        self.game_over_logo = None
        self.game_over_rect = None

    def handle_events(self, events):
        for event in events:
            if event.type ==  pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from screens.menu import MenuState
                self.manager.set_state(MenuState(self.manager))
    
    def update(self, dt):
        pass

    def draw(self, screen):
        width, height = screen.get_size()

        if self.background is None:
            self.background = pygame.transform.scale(self.bg_orig, (width, height))

            logo_w = int(width * 0.3)
            logo_h = int(self.game_over_orig.get_height() * logo_w / self.game_over_orig.get_width())
            self.game_over_logo = pygame.transform.smoothscale(self.game_over_orig, (logo_w, logo_h))

            self.game_over_rect = self.game_over_logo.get_rect(midtop=(width // 2, int(height * 0.1)))

        screen.blit(self.background, (0,0))
        screen.blit(self.game_over_logo, self.game_over_rect)

        text_surf_title = self.font_desc.render("Jogar novamente?", True, (255, 255, 255))

        text_rect = text_surf_title.get_rect(center=(width // 2, height // 1.5))

        screen.blit(text_surf_title, text_rect)
