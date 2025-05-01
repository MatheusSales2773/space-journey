import pygame

from config import settings
from core.state_manager import State

class PauseState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.text_font = pygame.font.Font(settings.FONT_ALT_EXPANDED_PATH, settings.FONT_SIZE_GAME)
        self.msg = "Jornada pausada"

        self.bg_orig  = pygame.image.load("assets/images/bg.png").convert()

        self.background = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("Voltando para o Gameplay...")
                from screens.menu import MenuState
                self.manager.set_state(MenuState(self.manager))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print("Voltando para o Menu...")
                from screens.gameplay import GameplayState
                self.manager.set_state(GameplayState(self.manager))
    
    def update(self, dt):
        pass

    def draw(self, screen):
        width, height = screen.get_size()

        if self.background is None:
            self.background = pygame.transform.scale(self.bg_orig, (width, height))

        screen.blit(self.background, (0, 0))

        text_surf = self.text_font.render(self.msg, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(width//2, height//2))
        screen.blit(text_surf, text_rect)