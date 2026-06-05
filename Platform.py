import pygame

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x,y,width,height)

    def draw(self, screen, color, camera_x, camera_y):

        pygame.draw.rect(screen, color, self.rect.move(-camera_x,-camera_y))