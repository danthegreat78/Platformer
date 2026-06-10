import pygame


class Powerup:

    IMAGE = pygame.transform.scale(pygame.image.load("Block.png"),(700,700))

    def __init__(self, x, y):
        self.pos = pygame.Vector2(x,y)
        self.image = Powerup.IMAGE
        #self.image = pygame.transform.scale(self.image, (700,700))
        self.hitbox_offset = pygame.Vector2(265, 167)
        self.hitbox = pygame.Rect(self.pos.x + self.hitbox_offset.x,self.pos.y + self.hitbox_offset.y, 115,113)


    def update(self, player):

        if self.hitbox.colliderect(player.hitbox):

            bottom = self.hitbox.bottom - player.hitbox.top
            top = player.hitbox.bottom - self.hitbox.top
            left = player.hitbox.right - self.hitbox.left
            right = self.hitbox.right - player.hitbox.left

            side = min(bottom,top,left,right)


            #if side == left:
             #   player.hitbox.right = self.hitbox.left
            #if side == right:
             #   player.hitbox.left = self.hitbox.right
            #if side == top:
            #    player.hitbox.bottom = self.hitbox.top
                #player.velocity_y = 500
            #if side == bottom:
             #   player.hitbox.top = self.hitbox.bottom
                #player.velocity_y = 300

    def draw(self, screen, camera_x, camera_y, show_hitboxes):
        screen.blit(self.image, ( self.pos.x - camera_x, self.pos.y - camera_y))
        if show_hitboxes:
            pygame.draw.rect(screen, "red", pygame.Rect(self.hitbox.x - camera_x, self.hitbox.y - camera_y, self.hitbox.width, self.hitbox.height), 2)
