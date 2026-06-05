import pygame

class Sign:

    def __init__(self, x, y, text, font):

        self.pos = pygame.Vector2(x,y)
        self.text = text
        self.font = font

        self.image = font.render(text, font, True, (255,255,255))

    def draw(self, screen, camera_x, camera_y):

        screen.blit(self.image, (self.pos.x - camera_x, self.pos.y - camera_y))
