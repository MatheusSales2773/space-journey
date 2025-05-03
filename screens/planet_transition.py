import pygame
from config import settings
from screens.menu import MenuState

class PlanetTransitionState:
    def __init__(self, manager, planet_name, planet_surface, curiosity):
        super().__init__()
        self.manager = manager
        self.planet_name = planet_name
        self.planet_surface = planet_surface
        print("Imagem da superfície recebida:", self.planet_surface)  # Depuração
        self.curiosity = curiosity
        self.alpha = 0
        self.fade_speed = 2
        self.vignette_radius = max(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        self.vignette_closing = True
        self.timer = 0
        self.show_message_box = False
        self.message_box_opacity = 0

        # Configurações da caixa de mensagem
        self.message_box_rect = pygame.Rect(
            50,  # Margem esquerda
            settings.WINDOW_HEIGHT - 150,  # Margem superior
            settings.WINDOW_WIDTH - 100,  # Largura total menos margens
            100  # Altura da caixa
        )
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)

    def update(self, dt):
        # Animação da vinheta fechando
        if self.vignette_closing:
            self.vignette_radius -= 800 * dt  # Velocidade de fechamento
            if self.vignette_radius <= 0:
                self.vignette_closing = False
                self.timer = 0
        else:
            # Após a vinheta fechar, iniciar o temporizador
            self.timer += dt
            self.alpha += self.fade_speed
            if self.alpha > 255:
                self.alpha = 255
            if self.timer > 5:  # Após 5 segundos, abrir a vinheta
                self.show_message_box = True
                self.message_box_opacity += 200 * dt
                if self.message_box_opacity > 255:
                    self.message_box_opacity = 255

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Preenche a tela com preto

        # Desenha a imagem do planeta com o efeito de fade-in
        if self.planet_surface:
            print("Desenhando imagem da superfície...")  # Depuração
            print("Alpha atual:", self.alpha)
            self.planet_surface.set_alpha(self.alpha)  # Aplica o alpha à superfície
            screen.blit(self.planet_surface, (0, 0))  # Desenha a imagem
        else:
            print("Erro: Imagem da superfície não está definida.")

        # Desenhar a vinheta
        vignette_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(
            vignette_surface,
            (0, 0, 0, 255),
            (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2),
            max(0, int(self.vignette_radius))
        )
        screen.blit(vignette_surface, (0, 0))

        # Mostrar a caixa de mensagem
        if self.show_message_box:
            message_box = pygame.Surface(self.message_box_rect.size, pygame.SRCALPHA)
            message_box.fill((0, 0, 0, int(self.message_box_opacity * 0.8)))  # Fundo preto com opacidade
            screen.blit(message_box, self.message_box_rect.topleft)

            # Quebrar o texto em várias linhas
            lines = self.wrap_text(self.curiosity, self.font, self.message_box_rect.width - 20)
            for i, line in enumerate(lines):
                text_surface = self.font.render(line, True, (255, 255, 255))
                screen.blit(
                    text_surface,
                    (self.message_box_rect.x + 10, self.message_box_rect.y + 10 + i * text_surface.get_height())
                )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Voltar ao menu ou próximo estado
                self.manager.set_state(MenuState(self.manager))

    def wrap_text(self, text, font, max_width):
        """Quebra o texto em várias linhas para caber na largura máxima."""
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_width = font.size(word)[0]
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width + font.size(' ')[0]
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width + font.size(' ')[0]

        lines.append(' '.join(current_line))
        return lines