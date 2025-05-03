import pygame
from config import settings
from core.state_manager import State
from screens.gameplay import GameplayState

class TutorialState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager      = manager
        self.scroll_speed = 150

        # Carrega e escala a imagem para preencher horizontalmente
        screen_w, screen_h = pygame.display.get_surface().get_size()
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

        # Fonte e mensagem
        self.font = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE_GAME)
        self.msg  = "Pressione ENTER para começar"

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                # Avança para o jogo sem reiniciar estado
                self.manager.set_state(GameplayState(self.manager))

    def update(self, dt):
        # Move a imagem para cima até y_offset = 0
        if self.y_offset > 0:
            self.y_offset -= self.scroll_speed * dt
            if self.y_offset < 0:
                self.y_offset = 0

    def draw(self, screen):
        # Desenha a parte correta da imagem
        screen.blit(self.tutorial_img, (0, -int(self.y_offset)))

        # Quando chegar ao topo, exibe o prompt
        if self.y_offset == 0:
            text_surf = self.font.render(self.msg, True, (255, 255, 255))
            text_rect = text_surf.get_rect(
                midbottom=(screen.get_width() // 2, self.screen_h - 20)
            )
            screen.blit(text_surf, text_rect)
