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



    def update(self, dt, keys, platforms):

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

        for platform in platforms:

            if self.hitbox.colliderect(platform.rect):
                left = self.hitbox.right - platform.rect.left
                right = platform.rect.right - self.hitbox.left
                bottom = self.hitbox.bottom - platform.rect.top
                top = platform.rect.bottom - self.hitbox.top

                side = min(left, right, top, bottom)

                if side == bottom:
                    self.hitbox.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

                elif side == right:
                        self.hitbox.left = platform.rect.right

                elif min(left, right, bottom, top) == left:
                    self.hitbox.right = platform.rect.left

                elif min(left, right, bottom, top) == top:
                    self.hitbox.top = platform.rect.bottom

        if self.jumper_buffer > 0:
            if self.on_ground:
                self.velocity_y = -1000
                self.on_ground = False
                self.jump_request = False






    def draw(self, screen, camera_x, camera_y):

        draw_x = self.hitbox.x - camera_x
        draw_y = self.hitbox.y - camera_y

        screen.blit(self.image, (self.hitbox.x - camera_x + self.draw_offset.x, self.hitbox.y - camera_y+ self.draw_offset.y))
        pygame.draw.rect(screen, "red", pygame.Rect(draw_x, draw_y, self.hitbox.width, self.hitbox.height), 2)