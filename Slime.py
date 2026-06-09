import pygame

class Slime:

    def __init__(self, x, y):

        self.image = pygame.image.load("slime.png")
        self.image = pygame.transform.scale(self.image, (500,500))
        self.hitbox = pygame.Rect(x,y,130,95)

        self.offset = pygame.Vector2(-135,-145)

        self.velocity_y = 0
        self.gravity = 3000 # Original: 1800
        self.direction = 1 # right = 1, left = -1
        self.speed = 120

        self.ground = None


    def update(self, dt, keys, platforms):

        self.velocity_y += self.gravity * dt
        self.hitbox.y += self.velocity_y * dt

        self.ground = None

        for platform in platforms:

            if self.hitbox.colliderect(platform.rect):

                left = self.hitbox.right - platform.rect.left
                right = platform.rect.right - self.hitbox.left
                bottom = self.hitbox.bottom - platform.rect.bottom
                top = platform.rect.bottom - self.hitbox.top

                side = min(left,right,bottom,top)

                if side == bottom:
                    self.hitbox.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.ground = platform
        if self.ground:
            next_x = self.hitbox.x + self.direction * self.speed * dt

            left_edge = self.ground.rect.left
            right_edge = self.ground.rect.right

            if next_x <= left_edge:
                self.hitbox.left = left_edge
                self.direction = 1

            elif next_x + self.hitbox.width >= right_edge:
                self.hitbox.right = right_edge
                self.direction = -1
            else:
                self.hitbox.x = next_x



    def draw(self, screen, camera_x, camera_y, show_hitboxes):

        draw_x = self.hitbox.x - camera_x
        draw_y = self.hitbox.y - camera_y

        screen.blit(self.image, (draw_x + self.offset.x, draw_y + self.offset.y))

        if show_hitboxes:

            pygame.draw.rect(screen, "red", pygame.Rect(draw_x, draw_y, self.hitbox.width, self.hitbox.height), 2)