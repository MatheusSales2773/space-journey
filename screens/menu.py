import pygame
from core.state_manager import State
from screens.gameplay import GameplayState

class MenuState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.font = pygame.font.SysFont(None, 48)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print("Trocando para o Gameplay...")
                self.manager.set_state(GameplayState())

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((10, 10, 50))
        text = self.font.render("Pressione ENTER para começar", True, (255, 255, 255))
        screen.blit(text, (100, 200))
