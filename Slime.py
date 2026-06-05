import pygame

class Slime:

    def __init__(self, x, y):

        self.image = pygame.image.load("slime.png")
        self.image = pygame.transform.scale(self.image, (500,500))
        self.hitbox = pygame.Rect(x,y,130,95)

        self.offset = pygame.Vector2(-135,-145)

    def draw(self, screen, camera_x, camera_y, show_hitboxes):

        draw_x = self.hitbox.x - camera_x
        draw_y = self.hitbox.y - camera_y

        screen.blit(self.image, (draw_x + self.offset.x, draw_y + self.offset.y))

        if show_hitboxes:

            pygame.draw.rect(screen, "red", pygame.Rect(draw_x, draw_y, self.hitbox.width, self.hitbox.height), 2)