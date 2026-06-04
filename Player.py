import pygame

class Player:

    def __init__(self, x, y):
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (1000,1000))

        self.pos = pygame.Vector2(x, y)
        self.velocity_y = 0

        self.gravity = 1800
        self.on_ground = False

        self.hitbox = pygame.rect(0,0,90,250)

        def update(self, dt, keys, ground_rect):
            left = self.hitbox.right - ground_rect.left
            right = ground_rect.right - self.hitbox.left
            bottom = self.hitbox.bottom - ground_rect.top
            top = ground_rect.bottom - self.hitbox.top

            if min(left, right, bottom, top) == bottom:
                self.hitbox.bottom = ground_rect.top
                self.pos.y = self.hitbox.centery
                self.velocity_y = 0
                on_ground = True

            elif min(left, right, bottom, top) == right:
                self.hitbox.left = ground_rect.right
                self.hitbox.x = ground_rect.centerx
            speed = 1000

            # Horizontal Movements
            if keys[pygame.K_a]:
                self.pos.x -= speed * dt
            if keys[pygame.K_d]:
                self.pos.x += speed * dt

            if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
                self.velocity_y = -1000