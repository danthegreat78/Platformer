import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player = pygame.image.load("player.png").convert_alpha()

player = pygame.transform.scale(player, (1000, 1000))

player_pos = pygame.Vector2(640, 100)

velocity_y = 0

gravity = 1800
ground_y = pygame.Rect(0, 680, 1000, 40)
wall_x = 1240
on_ground = False

while running:
    jump_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    velocity_y += gravity * dt
    player_pos.y += velocity_y * dt

    on_ground = False

    player_hitbox = pygame.Rect(0,0,90,250) # Hitbox adjustment
    player_hitbox.center = player_pos

    if player_hitbox.colliderect(ground_y):

        left = player_hitbox.right - ground_y.left
        right = ground_y.right - player_hitbox.left
        bottom = player_hitbox.bottom - ground_y.top
        top = ground_y.bottom - player_hitbox.top

        if min(left, right, bottom, top) == bottom:
            player_hitbox.bottom = ground_y.top
            player_pos.y = player_hitbox.centery
            velocity_y = 0
            on_ground = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_SPACE]:
        if on_ground:
            velocity_y = -1000



 #   if player_pos.y > ground_y:
  #      player_pos.y = ground_y
   #     velocity_y = 0

    #if(player_pos.x > wall_x):
     #   player_pos.x = wall_x

    screen.fill("purple")

    pygame.draw.rect(screen, "green", ground_y)

    screen.blit(player, (player_pos.x - player.get_width() / 2 -50,
                         player_pos.y - player.get_height() / 2 + 185)) #ADJUST THIS
    pygame.draw.rect(screen, "red", player_hitbox, 2) # Shows player hitbox




    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        player_pos.y += 1000 * dt

    if keys[pygame.K_a]:
        player_pos.x -= 1000 * dt

    if keys[pygame.K_d]:
        player_pos.x += 1000 * dt

    pygame.display.flip()
    pygame.display.set_caption("Platformer")

    dt = clock.tick(60) / 1000

pygame.quit()