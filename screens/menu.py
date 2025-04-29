import pygame
from core.state_manager import State

# from screens.gameplay import GameplayState
# from screens.menu import MenuState

class MenuState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.font = pygame.font.SysFont(None, 48)

        # 1) carregue os originais sem escalar
        self.bg_orig  = pygame.image.load("assets/images/menu_background.png").convert()
        self.logo_orig = pygame.image.load("assets/images/logo.png").convert_alpha()

        # 2) placeholders para as versões escaladas
        self.background = None
        self.logo       = None
        self.logo_rect  = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print("Trocando para o Gameplay...")
                from screens.gameplay import GameplayState
                self.manager.set_state(GameplayState(self.manager))
                

    def update(self, dt):
        pass

    def draw(self, screen):
        # Obtém a resolução atual
        width, height = screen.get_size()

        # Só escala na primeira vez (ou quando a janela mudar de tamanho)
        if self.background is None:
            # escala fundo para preencher toda a tela
            self.background = pygame.transform.scale(self.bg_orig, (width, height))

            # opcional: escalar logo para, digamos, 30% da largura da tela
            logo_w = int(width * 0.3)
            logo_h = int(self.logo_orig.get_height() * logo_w / self.logo_orig.get_width())
            self.logo = pygame.transform.smoothscale(self.logo_orig, (logo_w, logo_h))

            # posiciona o logo centralizado no topo (10% abaixo do topo)
            self.logo_rect = self.logo.get_rect(midtop=(width // 2, int(height * 0.1)))

        # 3) desenha tudo em ordem
        screen.blit(self.background, (0, 0))
        screen.blit(self.logo, self.logo_rect)

        # finalmente o texto, posicionado, por exemplo, centralizado um pouco abaixo
        msg = "Pressione ENTER para começar"
        text_surf = self.font.render(msg, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midbottom=(width // 2, int(height * 0.9)))
        screen.blit(text_surf, text_rect)