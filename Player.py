import pygame

class Player:

    def __init__(self, x, y):
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (1000,1000))

        self.hitbox = pygame.Rect(x,y,90,250)

        self.velocity_y = 0

        self.gravity = 1800

        self.on_ground = False

        self.jumper_buffer = 0

        self.draw_offset = pygame.Vector2(-500, -190)



    def update(self, dt, keys, ground_rect):

        if(self.jumper_buffer > 0):
            self.jumper_buffer -= dt


        self.velocity_y += self.gravity * dt
        self.hitbox.y += self.velocity_y * dt



        # Horizontal Movements
        speed = 1000
        if keys[pygame.K_a]:
            self.hitbox.x -= speed * dt
        if keys[pygame.K_d]:
            self.hitbox.x += speed * dt

        self.on_ground = False

        if self.hitbox.colliderect(ground_rect):
            left = self.hitbox.right - ground_rect.left
            right = ground_rect.right - self.hitbox.left
            bottom = self.hitbox.bottom - ground_rect.top
            top = ground_rect.bottom - self.hitbox.top

            if min(left, right, bottom, top) == bottom:
                self.hitbox.bottom = ground_rect.top
                self.velocity_y = 0
                self.on_ground = True

            elif min(left, right, bottom, top) == right:
                self.hitbox.left = ground_rect.right

        if self.jumper_buffer > 0:
            if self.on_ground:
                self.velocity_y = -1000
                self.on_ground = False
                self.jump_request = False






    def draw(self, screen):
        screen.blit(self.image, (self.hitbox.x + self.draw_offset.x, self.hitbox.y + self.draw_offset.y))
        pygame.draw.rect(screen, "red", self.hitbox, 2)