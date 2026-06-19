import pygame

class Cutscene:
    def __init__(self, font):
        self.font = font
        self.finished = False

        self.dialogue = [
            ("You", "Where am I?"),
            ("", "...")

        ]

        self.current_line = 0

        self.visible_chars = 0
        self.char_timer = 0
        self.type_speed = 0.03

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):

                speaker, text = self.dialogue[self.current_line]

                if self.visible_chars < len(text):
                    self.visible_chars = len(text)

                else:
                    self.current_line += 1
                    self.visible_chars = 0
                    self.char_timer = 0

                    if self.current_line >= len(self.dialogue):
                        self.finished = True

    def draw(self, screen):
        screen.fill("black")

        speaker, text = self.dialogue[self.current_line]

        shown_text = text[:int(self.visible_chars)]
        print(repr(shown_text))

        box = pygame.Rect(50,500,1180,180)

        pygame.draw.rect(screen, "white", box)
        pygame.draw.rect(screen, "black", box.inflate(-4,-4))

        speaker_text = self.font.render(speaker, True, "yellow")
        dialogue_text = self.font.render(shown_text, True, "white")

        screen.blit(speaker_text, (80,530))
        screen.blit(dialogue_text, (80, 580))

    def update(self, dt):
        if self.finished:
            return
        speaker, text = self.dialogue[self.current_line]

        if self.visible_chars < len(text):
            self.char_timer += dt

            if self.char_timer >= self.type_speed:
                self.char_timer -= self.type_speed
                self.visible_chars += 1
                #print(self.visible_chars)
