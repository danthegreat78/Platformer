import pygame
import json

from Platform import Platform
from Sign import Sign
from Slime import Slime


class Level:
    def __init__(self):
        self.platforms = []
        self.slimes = []
        self.slime_spawns = []
        self.signs = []

        self.powerups = []
        self.powerup_spawns = []

        self.player_start = (640,100)

    def update(self, dt, player, keys):

        player.update(dt, keys, self.platforms)
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

    def draw(self, screen, camera_x, camera_y, show_hitboxes):

        for platform in self.platforms:
            platform.draw(screen, "green", camera_x, camera_y)
        for sign in self.signs:
            sign.draw(screen, camera_x, camera_y)
        for slime in self.slimes:
            slime.draw(screen, camera_x, camera_y, show_hitboxes)

    def save(self, filename = "level.json"):
        data = {
            "platforms": [[p.rect.x, p.rect.y, p.rect.width, p.rect.height] for p in self.platforms],
            "slimes": [[s.hitbox.x, s.hitbox.y] for s in self.slimes],
            "signs": [[sg.x, sg.y, sg.text] for sg in self.signs]

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
    def reset(self):
        self.slimes = [Slime(*s) for s in self.slime_spawns]



