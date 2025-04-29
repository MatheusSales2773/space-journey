import pygame
from core.state_manager import State

class GameplayState(State):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont(None, 48)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("Voltando para o menu... (aqui você pode trocar de volta com self.manager.set_state)")

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        text = self.font.render("Gameplay em andamento!", True, (0, 255, 0))
        screen.blit(text, (100, 200))
