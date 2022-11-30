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
class Bishop(Enemy):
    is_summoning = False
    def __init__(self, assets_path):
        super().__init__(assets_path)
        self.move_frame = 0
        self.summon_frame = 0
        self.bishop_idle_R = [pygame.image.load(os.path.join(assets_path, "1.png")),
                            pygame.image.load(os.path.join(assets_path, "2.png")),
                            pygame.image.load(os.path.join(assets_path, "2.png")),
                            pygame.image.load(os.path.join(assets_path, "3.png")),
                            pygame.image.load(os.path.join(assets_path, "3.png")),
                            pygame.image.load(os.path.join(assets_path, "4.png")),
                            pygame.image.load(os.path.join(assets_path, "4.png")),
                            pygame.image.load(os.path.join(assets_path, "5.png")),
                            pygame.image.load(os.path.join(assets_path, "5.png")),
                            pygame.image.load(os.path.join(assets_path, "6.png")),
                            pygame.image.load(os.path.join(assets_path, "6.png")),
                            pygame.image.load(os.path.join(assets_path, "1.png"))]

        self.bishop_idle_L = [pygame.image.load(os.path.join(assets_path, "1L.png")),
                            pygame.image.load(os.path.join(assets_path, "2L.png")),
                            pygame.image.load(os.path.join(assets_path, "2L.png")),
                            pygame.image.load(os.path.join(assets_path, "3L.png")),
                            pygame.image.load(os.path.join(assets_path, "3L.png")),
                            pygame.image.load(os.path.join(assets_path, "4L.png")),
                            pygame.image.load(os.path.join(assets_path, "4L.png")),
                            pygame.image.load(os.path.join(assets_path, "5L.png")),
                            pygame.image.load(os.path.join(assets_path, "5L.png")),
                            pygame.image.load(os.path.join(assets_path, "6L.png")),
                            pygame.image.load(os.path.join(assets_path, "6L.png")),
                            pygame.image.load(os.path.join(assets_path, "1L.png"))]

        self.bishop_summon = [pygame.image.load(os.path.join(assets_path, "00.png")),
                            pygame.image.load(os.path.join(assets_path, "00.png")),
                            pygame.image.load(os.path.join(assets_path, "00.png")),
                            pygame.image.load(os.path.join(assets_path, "00.png")),
                            pygame.image.load(os.path.join(assets_path, "10.png")),
                            pygame.image.load(os.path.join(assets_path, "10.png")),
                            pygame.image.load(os.path.join(assets_path, "10.png")),
                            pygame.image.load(os.path.join(assets_path, "10.png")),
                            pygame.image.load(os.path.join(assets_path, "20.png")),
                            pygame.image.load(os.path.join(assets_path, "20.png")),
                            pygame.image.load(os.path.join(assets_path, "20.png")),
                            pygame.image.load(os.path.join(assets_path, "20.png")),
                            pygame.image.load(os.path.join(assets_path, "30.png")),
                            pygame.image.load(os.path.join(assets_path, "30.png")),
                            pygame.image.load(os.path.join(assets_path, "30.png")),
                            pygame.image.load(os.path.join(assets_path, "30.png")),
                            pygame.image.load(os.path.join(assets_path, "40.png")),
                            pygame.image.load(os.path.join(assets_path, "40.png")),
                            pygame.image.load(os.path.join(assets_path, "40.png")),
                            pygame.image.load(os.path.join(assets_path, "40.png")),
                            pygame.image.load(os.path.join(assets_path, "50.png")),
                            pygame.image.load(os.path.join(assets_path, "50.png")),
                            pygame.image.load(os.path.join(assets_path, "50.png")),
                            pygame.image.load(os.path.join(assets_path, "50.png")),
                            pygame.image.load(os.path.join(assets_path, "60.png")),
                            pygame.image.load(os.path.join(assets_path, "60.png")),
                            pygame.image.load(os.path.join(assets_path, "60.png")),
                            pygame.image.load(os.path.join(assets_path, "60.png")),
                            pygame.image.load(os.path.join(assets_path, "70.png")),
                            pygame.image.load(os.path.join(assets_path, "70.png")),
                            pygame.image.load(os.path.join(assets_path, "70.png")),
                            pygame.image.load(os.path.join(assets_path, "70.png"))]

        self.image = pygame.image.load(os.path.join(assets_path, "1.png"))
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.hp = 100
        self.direction = random.randint(0, 1) #0 for right, 1 for left
        self.vel.x = random.randint(2, 6) / 2 #randomizing velocity of enemy

        if self.direction == 0:
            self.pos.x = 50
            self.pos.y = 100
        if self.direction == 1:
            self.pos.x = WIDTH - 50
            self.pos.y = 100

    def teleport(self, assests_path):
        self.pos = vec(random.randint(20, WIDTH-20), random.randint(100, 200))

    def move(self, player=None):
        self.vel = vec(0,0)
        self.rect.center = self.pos

    def summon(self, assests_path):
        if self.summon_frame > 31:
            self.is_summoning = False
            self.summon_frame = 0
            return
        self.rect.bottom = self.pos.y
        self.image = self.bishop_summon[self.summon_frame]
        self.summon_frame += 1

        

    def updateRight(self, assets_path):
        if self.move_frame > 11:
            self.move_frame = 0
            return
        self.image = self.bishop_idle_R[self.move_frame]
        self.move_frame += 1

    def updateLeft(self, assets_path):
        if self.move_frame > 11:
            self.move_frame = 0
            return
        self.image = self.bishop_idle_L[self.move_frame]
        self.move_frame += 1

        
    def render(self, sur):
            #displayed the enemy on screen
            sur.blit(self.image, self.rect)