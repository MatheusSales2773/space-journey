class State:
    def __init__(self):
        pass

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

class StateManager:
    def __init__(self, initial_state):
        self.current_state = None
        self.current_state = initial_state

    def set_state(self, state: State):
        self.current_state = state

    def handle_events(self, events):
        if self.current_state:
            self.current_state.handle_events(events)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)