import pygame
import os
from pygame.locals import *
import sys
import random
from tkinter import filedialog #from the GUI library Tkinter
from tkinter import * #Tkinter is used to generate additional windows
from constants import *
from enemy import *
from player import *

pygame.init()
hit = False
class Lightning(Enemy):
    def __init__(self, assets_path, posx, posy):
        super().__init__(assets_path)
        self.hit = False
        self.move_frame = 0
        self.lightning_effect_A =  [pygame.image.load(os.path.join(assets_path, "F01.png")),
                                    pygame.image.load(os.path.join(assets_path, "F01.png")),
                                    pygame.image.load(os.path.join(assets_path, "F02.png")),
                                    pygame.image.load(os.path.join(assets_path, "F02.png")),
                                    pygame.image.load(os.path.join(assets_path, "F03.png")),
                                    pygame.image.load(os.path.join(assets_path, "F03.png")),
                                    pygame.image.load(os.path.join(assets_path, "F04.png")),
                                    pygame.image.load(os.path.join(assets_path, "F04.png")),
                                    pygame.image.load(os.path.join(assets_path, "F05.png")),
                                    pygame.image.load(os.path.join(assets_path, "F05.png")),
                                    pygame.image.load(os.path.join(assets_path, "F06.png")),
                                    pygame.image.load(os.path.join(assets_path, "F06.png")),
                                    pygame.image.load(os.path.join(assets_path, "F07.png")),
                                    pygame.image.load(os.path.join(assets_path, "F07.png")),
                                    pygame.image.load(os.path.join(assets_path, "F08.png")),
                                    pygame.image.load(os.path.join(assets_path, "F08.png")),
                                    pygame.image.load(os.path.join(assets_path, "F09.png")),
                                    pygame.image.load(os.path.join(assets_path, "F09.png")),
                                    pygame.image.load(os.path.join(assets_path, "F10.png")),
                                    pygame.image.load(os.path.join(assets_path, "F10.png")),
                                    pygame.image.load(os.path.join(assets_path, "F11.png")),
                                    pygame.image.load(os.path.join(assets_path, "F11.png")),
                                    pygame.image.load(os.path.join(assets_path, "F12.png")),
                                    pygame.image.load(os.path.join(assets_path, "F12.png")),
                                    pygame.image.load(os.path.join(assets_path, "F13.png")),
                                    pygame.image.load(os.path.join(assets_path, "F13.png")),
                                    pygame.image.load(os.path.join(assets_path, "F14.png")),
                                    pygame.image.load(os.path.join(assets_path, "F14.png")),
                                    pygame.image.load(os.path.join(assets_path, "F15.png")),
                                    pygame.image.load(os.path.join(assets_path, "F15.png")),
                                    pygame.image.load(os.path.join(assets_path, "F16.png")),
                                    pygame.image.load(os.path.join(assets_path, "F16.png")),
                                    pygame.image.load(os.path.join(assets_path, "F17.png")),
                                    pygame.image.load(os.path.join(assets_path, "F17.png")),
                                    pygame.image.load(os.path.join(assets_path, "F18.png")),
                                    pygame.image.load(os.path.join(assets_path, "F18.png")),
                                    pygame.image.load(os.path.join(assets_path, "F19.png")),
                                    pygame.image.load(os.path.join(assets_path, "F19.png")),
                                    pygame.image.load(os.path.join(assets_path, "F20.png")),
                                    pygame.image.load(os.path.join(assets_path, "F20.png")),
                                    pygame.image.load(os.path.join(assets_path, "F21.png")),
                                    pygame.image.load(os.path.join(assets_path, "F21.png")),
                                    pygame.image.load(os.path.join(assets_path, "F22.png")),
                                    pygame.image.load(os.path.join(assets_path, "F22.png")),
                                    pygame.image.load(os.path.join(assets_path, "F23.png")),
                                    pygame.image.load(os.path.join(assets_path, "F23.png")),
                                    pygame.image.load(os.path.join(assets_path, "F24.png")),
                                    pygame.image.load(os.path.join(assets_path, "F24.png")),
                                    pygame.image.load(os.path.join(assets_path, "F25.png")),
                                    pygame.image.load(os.path.join(assets_path, "F25.png")),
                                    pygame.image.load(os.path.join(assets_path, "F26.png")),
                                    pygame.image.load(os.path.join(assets_path, "F26.png")),
                                    pygame.image.load(os.path.join(assets_path, "F27.png")),
                                    pygame.image.load(os.path.join(assets_path, "F27.png"))]

        self.image = pygame.image.load(os.path.join(assets_path, "F01.png"))
        self.rect = self.image.get_rect()
        self.pos = vec(posx - 100, 85)
        self.vel = vec(0, 0)
        self.hp = 100
        self.playerpos = 0

    
    
    def update(self, assets_path, player):
        self.rect.center = self.pos
        if abs(self.rect.centerx + 100 - player.rect.centerx) < 80:
            if self.hit == False:
                print("THUNDERSTRUCK!!!")
                player.current_health -= 20
            self.hit = True
        if self.move_frame >= 53:
            self.kill()
        self.image = self.lightning_effect_A[self.move_frame]
        self.move_frame += 1

    def render(self, sur):
            #displayed the enemy on screen
            sur.blit(self.image, (self.pos.x, self.pos.y))
