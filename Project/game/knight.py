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
class Knight(Enemy):
    jmpcooldown = False
    death = False
    def __init__(self, assets_path):
        super().__init__(assets_path)
        self.facing = 0
        self.move_frame = 0
        self.attack_frame = 0
        self.crush_frame = 0
        self.is_jumping = False
        self.set_jmpvel = False
        self.crush = False
        self.knight_L =     [pygame.image.load(os.path.join(assets_path, "k0L-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k1L-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k2L-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k3L-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k4L-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k5L-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k6L-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k7L-modified.png"))]

        self.knight_R =     [pygame.image.load(os.path.join(assets_path, "k0-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k1-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k2-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k3-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k4-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k5-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k6-modified.png")),
                            pygame.image.load(os.path.join(assets_path, "k7-modified.png"))]

        self.knight_AFA =   [pygame.image.load(os.path.join(assets_path, "AFA0.png")),
                            pygame.image.load(os.path.join(assets_path, "AFA1.png")),
                            pygame.image.load(os.path.join(assets_path, "AFA2.png"))]

        self.image = pygame.image.load(os.path.join(assets_path, "k0-modified.png"))
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH, 230)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.hp = 50
    
    def move(self, player):
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        

        if self.facing == 0:
            self.acc.x = 0.15
            if self.vel.x > 3:
                self.vel.x = 3
        else:
            self.acc.x = -0.15
            if self.vel.x < -3:
                self.vel.x = -3

    def update(self, assests_path, player):
        if self.pos.x < player:
            self.facing = 0
        else:
            self.facing = 1
        if self.hp > 0 and self.is_jumping == False:
            self.tmp = 3
            self.crush = False
            if self.facing == 0:
                self.image = self.knight_R[int(self.move_frame)]
                self.move_frame += 0.1
                if self.move_frame > 7:
                    self.move_frame = 0
                    return
            else:
                self.image = self.knight_L[int(self.move_frame)]
                self.move_frame += 0.1
                if self.move_frame > 7:
                    self.move_frame = 0
                    return
        if self.hp <= 0:
            self.death = True
            self.kill()
    def jump(self, player, enemy):
        #print('rect center: ' + str(self.rect.center) + 'rect bottom ' + str(self.rect.bottom) +'player bottom ' + str(player.rect.bottom))
        if enemy.death == True:
            if abs((player.pos.x - 50) - self.pos.x) <= 230 and self.jmpcooldown == False:
                self.is_jumping = True
            if self.is_jumping == True and self.crush == False:
                if self.set_jmpvel == False:
                    self.vel.y = -5
                    self.set_jmpvel = True
                self.acc.y = 0.05
                if int(abs((player.pos.x) - self.pos.x)) <= 3:
                    self.crush = True
            if self.crush == True:
                if abs(self.rect.centerx - player.rect.centerx) < 25 and abs(self.rect.bottom - player.rect.top) < 10:
                    print('crushed')
                self.image = self.knight_AFA[int(self.crush_frame)]
                self.crush_frame += 0.1
                if self.crush_frame > 2:
                    self.crush_frame = 0
                self.vel.y = 10
                self.vel.x = 0
                if abs(int(self.pos.y) - 230) <= 5:
                    self.is_jumping = False
                    self.crush = False
                    self.set_jmpvel = False
                    self.jmpcooldown = True
                    self.pos.y = 230
                    self.vel.y = 0
                    self.acc.y = 0
                    pygame.time.set_timer(JMPCOOLDOWN, 3000)
            if self.jmpcooldown == True:
                self.vel.x = 0
                self.acc.x = 0
    def render(self, sur, enemy):
            #displayed the enemy on screen
        if enemy.death == True:
            sur.blit(self.image, self.rect)

        