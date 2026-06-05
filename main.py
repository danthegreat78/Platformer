import pygame
from Player import Player

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player = Player(640, 100)




ground_y = pygame.Rect(0, 680, 1000, 40)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                player.jumper_buffer = 0.1




    keys = pygame.key.get_pressed()



    player.update(dt, keys, ground_y)

    screen.fill("purple")

    pygame.draw.rect(screen, "green", ground_y)

    player.draw(screen)

   # screen.blit(player, (player_pos.x - player.get_width() / 2 -50,
    #                     player_pos.y - player.get_height() / 2 + 185)) #ADJUST THIS
    #pygame.draw.rect(screen, "red", player_hitbox, 2) # Shows player hitbox


    pygame.display.flip()
    pygame.display.set_caption("Platformer")

    dt = clock.tick(60) / 1000

pygame.quit()