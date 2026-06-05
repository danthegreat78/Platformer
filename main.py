import pygame
from Player import Player
from Platform import Platform
from Sign import Sign
from Slime import Slime

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

camera_x = 0
camera_y = 0

player = Player(640, 100)

platforms = [
    Platform(0,680,1000,40),
    Platform(400,500,300,40),
    Platform(1800,680,200,40)
]

slimes = [
    Slime(300, 300),
    Slime(100,100)
]

font = pygame.font.SysFont("arial", 30)

signs = [
    Sign(350, 100, "Welcome to Platformer!", font)
]



while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                player.jumper_buffer = 0.1




    keys = pygame.key.get_pressed()



    player.update(dt, keys, platforms)




    camera_x = player.hitbox.centerx - screen.get_width() // 2
    camera_y = player.hitbox.centery - screen.get_height() // 2

    screen.fill("purple")

    for platform in platforms:

        platform.draw(screen, "green", camera_x, camera_y)

    for sign in signs:
        sign.draw(screen, camera_x, camera_y)

    for slime in slimes:
        slime.draw(screen, camera_x, camera_y)

    player.draw(screen, camera_x, camera_y)


    pygame.display.flip()
    pygame.display.set_caption("Platformer")

    dt = clock.tick(60) / 1000

pygame.quit()