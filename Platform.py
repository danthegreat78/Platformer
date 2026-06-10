import pygame

class Platform:
    def __init__(self, x, y, width, height, image=None):
        self.rect = pygame.Rect(x,y,width,height)

        if image:

            self.image = pygame.image.load(image).convert_alpha()

            #self.image = pygame.transform.scale(self.image, (10000, 10000))
        else:
            self.image = None

    def draw(self, screen, color, camera_x, camera_y):

        if self.image:

            tile_width, tile_height = self.image.get_size()

            tiles_x = (self.rect.width + tile_width - 1) // tile_width
            tiles_y = (self.rect.height + tile_height - 1) // tile_height

            for i in range(tiles_x):
                for j in range(tiles_y):
                    x = self.rect.x + i * tile_width
                    y = self.rect.y + j * tile_height

                    blit_width = min(tile_width, self.rect.right - x)
                    blit_height = min(tile_height, self.rect.bottom - y)

                    if blit_width != tile_width or blit_height != tile_height:
                        tile = pygame.transform.scale(self.image, (blit_width, blit_height))
                    else:
                        tile = self.image

                    screen.blit(tile, (x - camera_x, y - camera_y))
        else:

            pygame.draw.rect(screen, color, self.rect.move(-camera_x,-camera_y))