import pygame
from Player import Player
from Platform import Platform
from Sign import Sign
from Slime import Slime
import json

def save_level(platforms):
    data = []
    print("saved")
    for p in platforms:

        data.append([p.rect.x, p.rect.y, p.rect.width, p.rect.height])

    with open("level.json", "w") as f:
            json.dump(data, f)

def load_level():
    with open("level.json", "r") as f:
        data = json.load(f)

    return [Platform(x,y,w,h) for x,y,w,h in data]

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
show_hitboxes = False

editing= False

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
            elif event.key == pygame.K_h:
                show_hitboxes = not show_hitboxes

            elif event.key == pygame.K_s:
                save_level(platforms)
            elif event.key == pygame.K_l:
                platforms = load_level()

            elif event.key == pygame.K_e:
                editing = not editing

        if event.type == pygame.MOUSEBUTTONDOWN and editing:
            print("building")
            mx,my = pygame.mouse.get_pos()

            world_x = mx + camera_x
            world_y = my + camera_y

            platforms.append(Platform(world_x, world_y, 100, 40))




    keys = pygame.key.get_pressed()



    player.update(dt, keys, platforms)

    if not player.alive:
        print("GAME OVER")
        player.alive = True





    camera_x = player.hitbox.centerx - screen.get_width() // 2
    camera_y = player.hitbox.centery - screen.get_height() // 2

    screen.fill("purple")

    for platform in platforms:

        platform.draw(screen, "green", camera_x, camera_y)

    for sign in signs:
        sign.draw(screen, camera_x, camera_y)

    for slime in slimes:
        slime.draw(screen, camera_x, camera_y, show_hitboxes)
        slime.update(dt, keys, platforms)

        if player.hitbox.colliderect(slime.hitbox):
            left = player.hitbox.right - slime.hitbox.left
            right = slime.hitbox.right - player.hitbox.left
            bottom = player.hitbox.bottom - slime.hitbox.top
            top = slime.hitbox.bottom - player.hitbox.top

            side = min(left,right,top,bottom)

            if side == bottom and player.velocity_y > 0:
                slimes.remove(slime)
                player.velocity_y = -500

            else:
                player.die()



    player.draw(screen, camera_x, camera_y, show_hitboxes)


    pygame.display.flip()
    pygame.display.set_caption("Platformer")

    dt = clock.tick(60) / 1000

pygame.quit()




