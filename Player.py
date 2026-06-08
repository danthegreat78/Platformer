import pygame

class Player:

    def __init__(self, x, y):
        self.image = pygame.image.load("simple-player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (800,800))
        self.image_walking = pygame.image.load("Player_walking.png").convert_alpha()
        self.image_walking = pygame.transform.scale(self.image_walking, (800,800))

        self.hitbox = pygame.Rect(x,y,100,290)

        self.velocity_y = 0

        self.gravity = 1800

        self.on_ground = False

        self.jumper_buffer = 0

        self.draw_offset = pygame.Vector2(-332, -150)

        self.facing_right = False

        self.flip_offset = pygame.Vector2(-36.5,0)

        self.alive = True
        self.walking = False

        self.walking_frames = [self.image, self.image_walking]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_interval = 0.02



    def update(self, dt, keys, platforms):

        if(self.jumper_buffer > 0):
            self.jumper_buffer -= dt


        self.velocity_y += self.gravity * dt
        self.hitbox.y += self.velocity_y * dt



        # Horizontal Movements
        speed = 1000
        if keys[pygame.K_a]:
            self.hitbox.x -= speed * dt
            self.facing_right = True
            self.walking = True
            self.frame_timer += dt

        elif keys[pygame.K_d]:
            self.hitbox.x += speed * dt
            self.facing_right = False
            self.walking = True
            self.frame_timer += dt
        else:
            self.walking = False
            self.frame_timer = 0

        if self.walking and self.on_ground:
            self.frame_timer += dt

            if self.frame_timer > self.frame_interval:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames)

        elif not self.on_ground:
            self.current_frame = 1
            self.frame_timer = 0
        else:
            self.current_frame = 0
            self.frame_timer = 0

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
                    self.velocity_y = 500

        if self.jumper_buffer > 0:
            if self.on_ground:
                self.velocity_y = -1000
                self.on_ground = False
                self.jump_request = False



    def draw(self, screen, camera_x, camera_y, show_hitboxes):
        draw_x = self.hitbox.x - camera_x
        draw_y = self.hitbox.y - camera_y


        if self.walking:

            image = self.image_walking
        else:
            image = self.image
        image = self.walking_frames[self.current_frame] if self.walking else self.image

        if(self.facing_right):
            offset = self.draw_offset
        else:
            image = pygame.transform.flip(image, True, False)
            offset = self.draw_offset + self.flip_offset

        screen.blit(image,
                    (self.hitbox.x - camera_x + offset.x, self.hitbox.y - camera_y + offset.y))

        if(show_hitboxes):

            pygame.draw.rect(screen, "red", pygame.Rect(draw_x, draw_y, self.hitbox.width, self.hitbox.height), 2)

    def die(self):
        self.alive = False