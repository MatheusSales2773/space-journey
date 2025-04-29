import pygame
from core.state_manager import StateManager
from screens.menu import MenuState

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Jornada Espacial")
    clock = pygame.time.Clock()
    running = True

    state_manager = StateManager()
    state_manager.set_state(MenuState(state_manager))

    while running:
        dt = clock.tick(60) / 1000  # delta time
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        state_manager.handle_events(events)
        state_manager.update(dt)
        state_manager.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
