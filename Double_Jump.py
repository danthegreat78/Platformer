import pygame
class Double_Jump:

    def __init__(self, x, y):

        self.pos = pygame.Vector2(x,y)

        self.image = pygame.image.load("DoubleJump.png")
        self.image = pygame.transform.scale(self.image, (700,700))

        self.hitbox = pygame.Rect(x+250, y+216, 95,129)

        self.visible = False

        self.collected = False

    def draw(self, screen, camera_x, camera_y, show_hitboxes, player):

        if not self.visible:
            return

        if self.collected:
            return

        screen.blit(self.image, (self.pos.x - camera_x, self.pos.y - camera_y))

        if show_hitboxes:
            pygame.draw.rect(screen, "red", pygame.Rect(self.hitbox.x - camera_x, self.hitbox.y -camera_y, self.hitbox.width, self.hitbox.height), 2)

    def draw_no_power(self, screen, camera_x, camera_y, show_hitboxes):

        screen.blit(self.image, (self.pos.x - camera_x, self.pos.y - camera_y))

        if show_hitboxes:
            pygame.draw.rect(screen, "red", pygame.Rect(self.hitbox.x - camera_x, self.hitbox.y -camera_y, self.hitbox.width, self.hitbox.height), 2)