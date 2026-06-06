#running after first frame, shows title of platformer, seems to stop afterwards.
#try commenting things that utilize other classes


import asyncio
import pygame
from Player import Player
from Platform import Platform
from Sign import Sign
from Slime import Slime
import json
import traceback
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
state = "menu"

play_button = pygame.Rect(490,250,300,80)
editor_button = pygame.Rect(490,380,300,80)
menu_font = pygame.font.SysFont("arail", 50)

editing= False

dragging_platform = False
start_pos = None

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


async def main():
    global running, editing, dragging_platform, start_pos, platforms, dt, show_hitboxes, camera_x, camera_y, player
    while running:

        try:
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
                    mx,my = pygame.mouse.get_pos()

                    world_x = mx + camera_x
                    world_y = my + camera_y

                    dragging_platform = True
                    start_pos = (world_x,world_y)

                    #platforms.append(Platform(world_x, world_y, 100, 40))
                if event.type == pygame.MOUSEBUTTONUP and editing:
                    if dragging_platform:
                        mx, my = pygame.mouse.get_pos()

                        end_x = mx + camera_x
                        end_y = my + camera_y

                        x = min(start_pos[0], end_x)
                        y = min(start_pos[1], end_y)

                        width = abs(end_x - start_pos[0])
                        height = abs(end_y - start_pos[1])

                        if width > 5 and height > 5:
                            platforms.append(Platform(x,y,width,height))
                        dragging_platform = False




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

            for slime in slimes[:]:
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

            if dragging_platform:
                mx, my = pygame.mouse.get_pos()

                current_x = mx + camera_x
                current_y = my + camera_y

                x = min(start_pos[0], current_x)
                y = min(start_pos[1], current_y)

                width = abs(current_x - start_pos[0])
                height = abs(current_y - start_pos[1])

                pygame.draw.rect(screen, "yellow", pygame.Rect(x-camera_x, y-camera_y, width,height),2)


            pygame.display.flip()
            pygame.display.set_caption("Platformer")

            dt = clock.tick(60) / 1000

            await asyncio.sleep(0)

        except Exception:
            traceback.print_exc()

asyncio.run(main())






