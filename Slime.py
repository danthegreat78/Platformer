import pygame

class Slime:

    def __init__(self, x, y):

        self.image = pygame.image.load("slime.png")
        self.image = pygame.transform.scale(self.image, (500,500))
        self.hitbox = pygame.Rect(x,y,130,95)

        self.offset = pygame.Vector2(-135,-145)

        self.velocity_y = 0
        self.gravity = 3000 # Original: 1800


    def update(self, dt, keys, platforms):

        self.velocity_y += self.gravity * dt
        self.hitbox.y += self.velocity_y * dt

        for platform in platforms:

            if self.hitbox.colliderect(platform.rect):

                left = self.hitbox.right - platform.rect.left
                right = self.hitbox.right - platform.rect.left
                bottom = self.hitbox.bottom - platform.rect.bottom
                top = platform.rect.bottom - self.hitbox.top

                side = min(left,right,bottom,top)

                if side == bottom:
                    self.hitbox.bottom = platform.rect.top
                    self.velocity_y = 0


    def draw(self, screen, camera_x, camera_y, show_hitboxes):

        draw_x = self.hitbox.x - camera_x
        draw_y = self.hitbox.y - camera_y

        screen.blit(self.image, (draw_x + self.offset.x, draw_y + self.offset.y))

        if show_hitboxes:

            pygame.draw.rect(screen, "red", pygame.Rect(draw_x, draw_y, self.hitbox.width, self.hitbox.height), 2)