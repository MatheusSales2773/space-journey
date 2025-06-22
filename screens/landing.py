import pygame
from config import settings
from screens.menu import MenuState

class PlanetTransitionState:
    def __init__(self, manager, planet_name, planet_surface, curiosity):
        super().__init__()
        self.manager = manager
        self.planet_name = planet_name
        self.original_planet_surface = planet_surface
        self.curiosity = curiosity

        screen_w, screen_h = pygame.display.get_surface().get_size()
        self.screen_h = screen_h
        self.screen_w = screen_w    

        original_w, original_h = self.original_planet_surface.get_size()
        scale_ratio = self.screen_w / original_w  # Calcula a proporção baseada na largura
        scaled_h = int(original_h * scale_ratio) # Calcula a nova altura proporcional
        
        # Usa smoothscale para um redimensionamento de melhor qualidade
        self.scaled_planet_img = pygame.transform.smoothscale(
            self.original_planet_surface, (self.screen_w, scaled_h)
        )

        # --- CONFIGURAÇÃO DA ANIMAÇÃO DE POUSO ---
        # A distância da rolagem será a altura da imagem redimensionada
        self.scroll_distance = self.scaled_planet_img.get_height()
        self.y_offset = 0  # Progresso da rolagem, de 0 até a distância total
        self.is_scrolling = True
        self.current_speed = 0.0
        # A velocidade é calculada para que a animação dure cerca de 8 segundos
        self.target_speed = self.scroll_distance / 8.0
        self.acceleration = self.target_speed / 4.0

        # --- CONFIGURAÇÃO DA ESPAÇONAVE ---
        self.spaceship_img = pygame.image.load('assets/images/spaceship.png').convert_alpha()
        
        self.start_scale = 0.05
        self.end_scale = 0.4
        self.start_pos_y = -100
        self.end_pos_y = self.screen_h // 2 + 50

        self.current_scale = self.start_scale
        w = int(self.spaceship_img.get_width() * self.current_scale)
        h = int(self.spaceship_img.get_height() * self.current_scale)
        self.scaled_spaceship_img = pygame.transform.smoothscale(self.spaceship_img, (w,h))
        self.spaceship_rect = self.scaled_spaceship_img.get_rect(
            center=(self.screen_w // 2, self.start_pos_y)
        )

        # --- CONFIGURAÇÃO DA CAIXA DE MENSAGEM ---
        self.show_message_box = False
        self.message_box_opacity = 0
        self.end_timer = 0
        self.message_box_rect = pygame.Rect(
            50, self.screen_h - 170,
            self.screen_w - 100, 150
        )
        self.font = pygame.font.Font("assets/fonts/Rajdhani-Bold.ttf", 24)

        self.font_title = pygame.font.Font("assets/fonts/Rajdhani-Bold.ttf", 96)

    def update(self, dt):
        """Atualiza a lógica da animação a cada quadro."""
        if self.is_scrolling:
            if self.current_speed < self.target_speed:
                self.current_speed = min(
                    self.target_speed,
                    self.current_speed + self.acceleration * dt
                )

            self.y_offset += self.current_speed * dt

            progress = self.y_offset / self.scroll_distance if self.scroll_distance > 0 else 1
            progress = min(1, progress)

            self.current_scale = self.start_scale + (self.end_scale - self.start_scale) * progress
            current_pos_y = self.start_pos_y + (self.end_pos_y - self.start_pos_y) * progress

            w = int(self.spaceship_img.get_width() * self.current_scale)
            h = int(self.spaceship_img.get_height() * self.current_scale)
            self.scaled_spaceship_img = pygame.transform.smoothscale(self.spaceship_img, (w, h))
            self.spaceship_rect = self.scaled_spaceship_img.get_rect(center=(self.screen_w // 2, int(current_pos_y)))

            if self.y_offset >= self.scroll_distance:
                self.y_offset = self.scroll_distance
                self.is_scrolling = False
                self.current_speed = 0
        else:
            self.end_timer += dt
            if self.end_timer > 1:
                self.show_message_box = True
                self.message_box_opacity = min(255, self.message_box_opacity + 200 * dt)

    def draw(self, screen):
        screen.fill((0, 0, 0)) # Fundo preto representando o espaço

        # --- DESENHO DA SUPERFÍCIE DO PLANETA ---
        # A posição Y da imagem é calculada para que ela surja de baixo para cima
        draw_y_pos = self.screen_h - self.y_offset
        screen.blit(self.scaled_planet_img, (0, draw_y_pos))
        
        screen.blit(self.scaled_spaceship_img, self.spaceship_rect)

        if self.show_message_box:
            message_box_surface = pygame.Surface(self.message_box_rect.size, pygame.SRCALPHA)
            message_box_surface.fill((0, 0, 0, min(200, int(self.message_box_opacity))))
            
            pygame.draw.rect(message_box_surface, (255, 255, 255, int(self.message_box_opacity)), message_box_surface.get_rect(), 2, border_radius=5)
            screen.blit(message_box_surface, self.message_box_rect.topleft)

            title_text = self.font_title.render(self.planet_name, True, (255, 255, 255))
            title_rect = title_text.get_rect(topleft=(30, 30))
            screen.blit(title_text, title_rect)

            lines = self.wrap_text(f"{self.curiosity}", self.font, self.message_box_rect.width - 30)
            for i, line in enumerate(lines):
                text_surface = self.font.render(line, True, (255, 255, 255))
                text_surface.set_alpha(int(self.message_box_opacity))
                text_pos = (
                    self.message_box_rect.x + 15,
                    self.message_box_rect.y + 15 + i * (self.font.get_height() + 5)
                )
                screen.blit(text_surface, text_pos)

            if self.message_box_opacity >= 255:
                hint_font = pygame.font.Font("assets/fonts/Rajdhani-Semibold.ttf", 22)
                hint_text = hint_font.render("Pressione ENTER para voltar ao Menu", True, (220, 220, 220))
                hint_rect = hint_text.get_rect(centerx=self.message_box_rect.centerx, bottom=self.message_box_rect.bottom - 10)
                screen.blit(hint_text, hint_rect)

    def handle_events(self, events):
        """Processa os eventos de entrada do jogador."""
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if not self.is_scrolling:
                    self.manager.set_state(MenuState(self.manager))

    def wrap_text(self, text, font, max_width):
        """Quebra o texto em várias linhas para caber na largura máxima."""
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        
        lines.append(current_line.strip())
        return lines
