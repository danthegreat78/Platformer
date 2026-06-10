#try setting dragging platform to false somewhere where editor is initalized to stop the drawing after exiting game state and then going into editor state issue.

import asyncio
import pygame
#import pygame.scrap
import platform
from Level import Level
from Player import Player
from Platform import Platform
from Sign import Sign
from Slime import Slime
import json
from Powerup import Powerup

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

def export_level(platforms, slimes, signs, powerups):
    data = {
        "player_start": [640,100],
        "platforms": [
            {"x": p.rect.x, "y": p.rect.y, "w": p.rect.width, "h": p.rect.height}
            for p in platforms
        ],
        "slimes": [
            [s.hitbox.x, s.hitbox.y]
            for s in slimes
        ],
        "signs": [
            [sg.pos.x, sg.pos.y, sg.text] for sg in signs
        ],
        "powerups": [
            [p.pos.x, p.pos.y]
            for p in powerups
        ]
    }
    return json.dumps(data, indent=2)

def mouse_over_ui(pos):
    return export_button.collidepoint(pos)

def reset_game():
    print("RESETTING")
    global player, camera_x ,camera_y, platforms, slimes

    player = Player(640,100)

    camera_x = 0
    camera_y = 0

    level1.reset()
    level1.load(font, "level1.json")

def get_clipboard_text():
    text = ""
    try:
        raw = pygame.scrap.get(pygame.SCRAP_TEXT)
        if raw:
            text = raw.decode("utf-8")
            text = text.replace("\0", "")
            text = text.strip()
    except Exception as e:
        print(e)
        pass
    return text


async def get_clipboard_text_web():
    try:

        return str(text)
    except Exception as e:
        print("Clipboard error", e)
        return str(e)

def reset_editor():
    global player, camera_x, camera_y

    player = Player(640,100)

    camera_x = 0
    camera_y = 0

    level1.platforms = platforms
    level1.slimes = [Slime(s.hitbox.x, s.hitbox.y) for s in editor_slimes]
    level1.signs = editor_signs
    level1.powerups = [Powerup(p.pos.x, p.pos.y) for p in editor_powerups]

pygame.init()
screen = pygame.display.set_mode((1280, 720))

try:
    pygame.scrap.init()
    pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
except Exception as e:
    print(e)

background = pygame.image.load("sky.png").convert_alpha()
background = pygame.transform.scale(background, (1280, 720))
background_tile_width = background.get_width()
background_tile_height = background.get_height()
clock = pygame.time.Clock()
brick = "Brick.png"
running = True
dt = 0
show_hitboxes = False
state = "menu"

play_button = pygame.Rect(490,250,300,80)
editor_button = pygame.Rect(490,380,300,80)
menu_font = pygame.font.SysFont("arial", 50)
export_button = pygame.Rect(10,10,150,80)

editing = False
editor_cam_x = 0
editor_cam_y = 0
camera_speed = 500

export_text = ""
show_export_box = False
x_rect = pygame.Rect(500, 505, 200, 50)


dragging_platform = False
start_pos = None
object_dropdown_open = False
object_types = ["Platform", "Slime", "Sign", "Powerup"]
selected_object = object_types[0]
dropdown_rect = pygame.Rect(170,10,120,30)
dropdown_font = pygame.font.SysFont("arial", 20)





camera_x = 0
camera_y = 0
font = pygame.font.SysFont("arial", 30)
level1 = Level()
level1.load(font, "level1.json")

player = Player(*level1.player_start)

editor_slimes = []
editor_signs = []
editor_powerups = []

platforms = [
    Platform(0,680,1100,40),
    Platform(400,500,300,40),
    Platform(1800,680,200,40)
]

slimes = [
    Slime(300, 300),
    Slime(100,100)
]


x_rect_text = font.render("OK", True, "black")

signs = [
    Sign(350, 100, "Welcome to Platformer!", font)
]

import_button = pygame.Rect(10,100,150,50)
import_text = font.render("IMPORT", True, "black")
show_import_box = False
import_text_box = ""
import_ok_button = pygame.Rect(import_button.x + 1079, import_button.y, 60, 50)
import_ok_text = font.render("X", True, "black")

playtest_button = pygame.Rect(10, 160, 150, 50)
playtest_text = font.render("PLAYTEST", True, "black")
play_test = False

powerup = Powerup(640,-100)




async def main():
    global running, editing, dragging_platform, start_pos, platforms, dt, show_hitboxes, camera_x, camera_y, player, state, editor_cam_x, editor_cam_y, camera_speed, export_text, show_export_box, x_rect, object_dropdown_open, object_types, selected_object, dropdown_rect, dropdown_font, import_button, import_text, show_import_box, import_text_box, import_ok_button, import_ok_text, playtest_button, playtest_text, play_test, powerup, editor_powerups
    while running:

        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
                    mx,my = pygame.mouse.get_pos()

                    if(play_button.collidepoint(mx,my)):
                        reset_game()
                        state = "game"
                    if editor_button.collidepoint(mx,my):
                        state = "editor"
                        editing = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        player.jumper_buffer = 0.1
                    elif event.key == pygame.K_h:
                        show_hitboxes = not show_hitboxes

                    elif event.key == pygame.K_s and keys[pygame.K_LCTRL]:
                        save_level(platforms)
                    elif event.key == pygame.K_l and keys[pygame.K_LCTRL]:
                            platforms = load_level()
                    if event.key == pygame.K_ESCAPE and not play_test:
                        editing = False
                        state = "menu"

                    elif event.key == pygame.K_ESCAPE and play_test:
                        play_test = False
                        editing = True
                        state = "editor"

                    if show_import_box:

                        if event.key == pygame.K_v and (pygame.key.get_mods() & pygame.KMOD_CTRL):

                            if hasattr(pygame, "scrap"):
                                import_text_box += get_clipboard_text()
                            #else:

                            #text = await get_clipboard_text_web()
                            #import_text_box += text
                            #import_text_box += "working"

                        if event.key == pygame.K_BACKSPACE:
                            import_text_box = import_text_box[:-1]
                        elif event.key == pygame.K_RETURN:
                            try:
                                clean_text = import_text_box.replace(("\0"), "").strip()
                                data = json.loads(clean_text)
                                platforms.clear()
                                editor_slimes.clear()
                                editor_signs.clear()
                                editor_powerups.clear()

                                for p in data.get("platforms", []):
                                    platforms.append(Platform(p["x"], p["y"], p["w"], p["h"]))
                                for s in data.get("slimes", []):
                                    editor_slimes.append(Slime(*s))
                                for sg in data.get("signs", []):
                                    editor_signs.append(Sign(sg[0], sg[1], sg[2], font))

                                for p in data.get("powerups", []):
                                    editor_powerups.append(Powerup(*p))

                                show_import_box = False
                                import_text_box = ""
                            except Exception as e:
                                print("Invalid JSON", e)
                        else:

                            if event.unicode and event.unicode.isprintable():
                                import_text_box += event.unicode


                if event.type == pygame.MOUSEBUTTONDOWN and editing:
                    mx,my = pygame.mouse.get_pos()

                    world_x = mx + camera_x
                    world_y = my + camera_y

                    if event.button == 3:
                        for platform in platforms[:]:
                            if platform.rect.collidepoint(world_x,world_y):
                                platforms.remove(platform)
                        for slime in editor_slimes[:]:
                            if slime.hitbox.collidepoint(world_x,world_y):
                                editor_slimes.remove(slime)
                        for powerup in editor_powerups:
                            if powerup.hitbox.collidepoint(world_x, world_y):
                                editor_powerups.remove(powerup)


                    if event.button == 1:

                        if import_button.collidepoint((mx,my)):
                            show_import_box = True

                        if selected_object == "Platform" and not mouse_over_ui((mx,my)):
                            dragging_platform = True
                            start_pos = (world_x,world_y)
                        else:
                            dragging_platform = False


                        if selected_object == "Slime"  and not mouse_over_ui((mx,my)):
                            editor_slimes.append(Slime(world_x,world_y))

                        if selected_object == "Powerup" and not mouse_over_ui((mx,my)):
                            editor_powerups.append(Powerup(world_x - 265,world_y - 167))

                        if show_import_box:
                            if import_ok_button.collidepoint((mx,my)):
                                show_import_box = False
                        if playtest_button.collidepoint((mx,my)):
                            play_test = True
                            editing = False
                            dragging_platform = False
                            reset_editor()
                            state = "game"


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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx,my = pygame.mouse.get_pos()

                    if(dropdown_rect.collidepoint(mx,my)):
                        object_dropdown_open = not object_dropdown_open
                    elif object_dropdown_open:
                        for i, obj in enumerate(object_types):
                            option_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.y + (i+1) * dropdown_rect.height, dropdown_rect.width, dropdown_rect.height)
                            if option_rect.collidepoint(mx,my):
                                selected_object = obj
                                object_dropdown_open = False
                                break
                    if export_button.collidepoint(mx,my):
                        export_text = export_level(platforms, editor_slimes, editor_signs, editor_powerups)
                        show_export_box = True
                        print(export_text)
                    elif x_rect.collidepoint(mx,my):
                        show_export_box = False




            keys = pygame.key.get_pressed()

            mx,my = pygame.mouse.get_pos()

            #if not hasattr(pygame, "scrap"):
                #asyncio.create_task(get_clipboard_text_web())

            if dragging_platform and mouse_over_ui((mx,my)):
                dragging_platform = False
                start_pos = None

            if(state == "editor"):
                if keys[pygame.K_a]:
                    editor_cam_x -= camera_speed * dt
                if keys[pygame.K_d]:
                    editor_cam_x += camera_speed * dt
                if keys[pygame.K_w] or keys[pygame.K_SPACE]:
                    editor_cam_y -= camera_speed * dt
                if keys[pygame.K_s]:
                    editor_cam_y += camera_speed * dt

           # if state == "game":

                #level1.update(dt,player,keys)
                #level1.draw(screen,camera_x,camera_y,show_hitboxes)
                #player.update(dt, keys, platforms)

            if not player.alive:
                state = "menu"
                #print("GAME OVER")
                player.alive = True






            if state == "game":
                camera_x = player.hitbox.centerx - screen.get_width() // 2
                camera_y = player.hitbox.centery - screen.get_height() // 2


                offset_x = -camera_x % background_tile_width

                for x in range(-background_tile_width,screen.get_width(), background_tile_width):
                    screen.blit(background, (x + offset_x,0))


                level1.update(dt, player, keys)
                level1.draw(screen, camera_x,camera_y, show_hitboxes)
                #powerup.draw(screen, camera_x, camera_y, show_hitboxes)
                #powerup.update(player)

                player.draw(screen, camera_x, camera_y, show_hitboxes)

            elif state == "menu":
                screen.fill("black")
                pygame.draw.rect(screen, "green", play_button)
                play_text = font.render("PLAY", True, "black")
                editor_text = font.render("EDITOR", True, "black")
                pygame.draw.rect(screen, "blue", editor_button)
                screen.blit(play_text,(play_button.x + 110, play_button.y + 20))
                screen.blit(editor_text, (editor_button.x + 95, editor_button.y + 20))

            elif state == "editor":
                screen.fill("darkgrey")
                camera_x = editor_cam_x
                camera_y = editor_cam_y

                camera_speed = 1500 if keys[pygame.K_LSHIFT] else 500

                for platform in platforms:
                    platform.draw(screen, "green", camera_x, camera_y)

                for slime in editor_slimes:
                    slime.draw(screen, camera_x, camera_y, show_hitboxes)
                for sign in editor_signs:
                    sign.draw(screen, camera_x, camera_y)

                for powerup in editor_powerups:
                    powerup.draw(screen, camera_x, camera_y, show_hitboxes)

                pygame.draw.rect(screen, "orange", export_button)
                export_label = font.render("EXPORT", True, "black")
                screen.blit(export_label, (22,30))

                pygame.draw.rect(screen, "yellow", import_button)
                screen.blit(import_text, (import_button.x + 10, import_button.y + 10))

                pygame.draw.rect(screen, "lightblue", playtest_button)
                screen.blit(playtest_text, (playtest_button.x, playtest_button.y + 10))

                if show_import_box:
                    box_rect = pygame.Rect(150,150,1000,400)
                    pygame.draw.rect(screen, "black", box_rect)
                    pygame.draw.rect(screen, "white", box_rect, 2)
                    pygame.draw.rect(screen, "red", import_ok_button)
                    screen.blit(import_ok_text, (import_ok_button.x+20, import_ok_button.y + 10))

                    y = box_rect.y + 10
                    x = box_rect.x + 10

                    line = ""

                    for char in import_text_box:
                        test = line + char

                        if font.size(test)[0] > box_rect.width - 20:
                            screen.blit(font.render(line, True, "white"), (x,y))
                            y += 30
                            line = char
                        else:
                            line = test
                    if line:
                        screen.blit(font.render(line, True, (255,255,255)), (x,y))

                if show_export_box:
                    box_rect = pygame.Rect(200,200,800,300)
                    pygame.draw.rect(screen, "black", box_rect)
                    pygame.draw.rect(screen, "white", box_rect, 2)
                    pygame.draw.rect(screen, "red", x_rect)
                    screen.blit(x_rect_text, (575,510))
                    x = box_rect.x + 10
                    y = box_rect.y + 10

                    line = ""

                    for char in export_text:
                        test = line + char

                        if font.size(test)[0] > box_rect.width - 20:
                            screen.blit(font.render(line, True, "white"), (x, y))
                            y += 30
                            line = char
                            if y > box_rect.bottom - 30:
                                break
                        else:
                            line = test

                    if line:
                        screen.blit(font.render(line, True, "white"), (x, y))

                pygame.draw.rect(screen, "lightgrey", dropdown_rect)
                text = dropdown_font.render(selected_object, True, "black")
                screen.blit(text, (dropdown_rect.x + 34, dropdown_rect.y + 5))

                if(object_dropdown_open):
                    for i, obj in enumerate(object_types):
                        option_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.y + (i+1) * dropdown_rect.height, dropdown_rect.width, dropdown_rect.height)
                        pygame.draw.rect(screen, "white", option_rect)
                        pygame.draw.rect(screen, "black", option_rect, 1)
                        option_text = dropdown_font.render(obj, True, "black")
                        screen.blit(option_text, (option_rect.x+34, option_rect.y+2))







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

        except Exception as e:
            print(e)

asyncio.run(main())






