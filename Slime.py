import pygame

class Slime:

    def __init__(self, x, y):

        self.image = pygame.image.load("slime.png")
        self.image = pygame.transform.scale(self.image, (500,500))
        self.hitbox = pygame.Rect(x,y,130,95)

        self.hitbox_offset = pygame.Vector2(-164,-158)

    def draw(self, screen, camera_x, camera_y):

        draw_x = self.hitbox.x - camera_x + self.hitbox_offset.x
        draw_y = self.hitbox.y - camera_y + self.hitbox_offset.y

        screen.blit(self.image, (-camera_x, -camera_y))

        pygame.draw.rect(screen, "red", pygame.Rect(draw_x, draw_y, self.hitbox.width, self.hitbox.height), 2)