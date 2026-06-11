import pygame
import json

from Platform import Platform
from Powerup import Powerup
from Sign import Sign
from Slime import Slime
from Double_Jump import Double_Jump


class Level:
    def __init__(self):
        self.platforms = []
        self.slimes = []
        self.slime_spawns = []
        self.signs = []

        self.powerups = []
        self.powerup_spawns = []

        self.double_jumps = []
        self.double_spawns = []

        self.player_start = (640,100)

        self.wait_till_onground = False

    def update(self, dt, player, keys):

        player.update(dt, keys, self.platforms, self.powerups)

        for p in self.powerups:
            p.update(player)


        if player.hitbox.y > 2000:
            player.die()

        for slime in self.slimes[:]:
            slime.update(dt, keys, self.platforms)
            if player.hitbox.colliderect(slime.hitbox):
                left = player.hitbox.right - slime.hitbox.left
                right = slime.hitbox.right - player.hitbox.left
                bottom = player.hitbox.bottom - slime.hitbox.top
                top = slime.hitbox.bottom - player.hitbox.top

                side = min(left,right,top,bottom)

                if side == bottom and player.velocity_y > 0:
                    self.slimes.remove(slime)
                    player.velocity_y = -500
                else:
                    player.die()
        for dj in self.double_jumps:
            if player.hitbox.colliderect(dj.hitbox):
                if not dj.collected:
                    player.double_jump_used = False
                    dj.collected = True
               # self.wait_till_onground = True

       # if self.wait_till_onground and player.on_ground:
        #    self.wait_till_onground = False
         #   player.double_jump_used = False

    def draw(self, screen, camera_x, camera_y, show_hitboxes, player):

        for platform in self.platforms:
            platform.draw(screen, "green", camera_x, camera_y)
        for sign in self.signs:
            sign.draw(screen, camera_x, camera_y)
        for slime in self.slimes:
            slime.draw(screen, camera_x, camera_y, show_hitboxes)

        for powerup in self.powerups:
            powerup.draw(screen, camera_x, camera_y, show_hitboxes)

        for dj in self.double_jumps:
            dj.draw(screen, camera_x, camera_y, show_hitboxes, player)

    def save(self, filename = "level.json"):
        data = {
            "platforms": [[p.rect.x, p.rect.y, p.rect.width, p.rect.height] for p in self.platforms],
            "slimes": [[s.hitbox.x, s.hitbox.y] for s in self.slimes],
            "signs": [[sg.x, sg.y, sg.text] for sg in self.signs],
            "powerups": [[p.pos.x, p.pos.y] for p in self.powerups],
            "double_jumps": [[dj.pos.x, dj.pos.y] for dj in self.double_jumps]

        }
        with open(filename, "w") as f:
            json.dump(data, f)

    def load(self, font, filename = "level.json"):
        with open(filename, "r") as f:
            data = json.load(f)
        self.player_start = data.get("player_start", [640,100])
        self.platforms = [
            Platform(p["x"], p["y"], p["w"], p["h"], p.get("image"))
            for p in data["platforms"]
        ]
        self.slime_spawns  = data["slimes"]
        self.slimes = [Slime(*s) for s in data["slimes"]]
        self.signs = [Sign(*sg, font) for sg in data["signs"]]
        self.powerup_spawns = data.get("powerups", [])
        self.powerups = [Powerup(*p) for p in self.powerup_spawns]

        self.double_spawns = data.get("double_jumps", [])
        self.double_jumps = [Double_Jump(*dj) for dj in self.double_spawns]

        for powerup, dj in zip(self.powerups, self.double_jumps):
            powerup.reward = dj

    def reset(self):
        self.slimes = [Slime(*s) for s in self.slime_spawns]
        self.powerups = [Powerup(*p) for p in self.powerup_spawns]



