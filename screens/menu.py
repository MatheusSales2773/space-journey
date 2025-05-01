import pygame

from config import settings
from core.state_manager import State

class MenuState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.font = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE_GAME)
        self.msg = "Pressione ENTER para começar"

        # Efeito de Fade
        self.alpha = 0                 
        self.fade_direction = 1        
        self.fade_speed = 300    

        self.bg_orig  = pygame.image.load("assets/images/menu_background.png").convert()
        self.logo_orig = pygame.image.load("assets/images/logo.png").convert_alpha()

        self.background = None
        self.logo       = None
        self.logo_rect  = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Pressionar Enter para iniciar
                    from screens.level_selection import LevelSelectionState
                    self.manager.set_state(LevelSelectionState(self.manager))
                elif event.key == pygame.K_ESCAPE:  # Pressionar Esc para sair
                    pygame.quit()
                    exit()
                

    def update(self, dt):
        self.alpha += self.fade_speed * dt * self.fade_direction
        if self.alpha >= 255:
            self.alpha = 255
            self.fade_direction = -1
        elif self.alpha <= 10:
            self.alpha = 10
            self.fade_direction = 1

    def draw(self, screen):
        width, height = screen.get_size()

        if self.background is None:
            self.background = pygame.transform.scale(self.bg_orig, (width, height))

            logo_w = int(width * 0.3)
            logo_h = int(self.logo_orig.get_height() * logo_w / self.logo_orig.get_width())
            self.logo = pygame.transform.smoothscale(self.logo_orig, (logo_w, logo_h))

            self.logo_rect = self.logo.get_rect(midtop=(width // 2, int(height * 0.1)))

        screen.blit(self.background, (0, 0))
        screen.blit(self.logo, self.logo_rect)

        text_surf = self.font.render(self.msg, True, (255, 255, 255))
        text_surf.set_alpha(int(self.alpha))
        text_rect = text_surf.get_rect(midbottom=(width//2, int(height*0.9)))
        screen.blit(text_surf, text_rect)