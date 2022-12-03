import math
import pygame
import os
from pygame.locals import *
import sys
import random
from tkinter import filedialog #from the GUI library Tkinter
from tkinter import * #Tkinter is used to generate additional windows
from constants import *
from enemy import *

pygame.init()    
class Cannon(Enemy):
    death = False
    def __init__(self, assets_path):
        super().__init__(assets_path)
        self.image = pygame.image.load(os.path.join(assets_path, "Cannon_test.png"))
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/5), int(self.size[1]/5)))
        self.rect = self.image.get_rect()
        self.bullet_list = []
        self.hit = False
        self.image_num = 0
        self.image_index = 0
        self.pos.y += 25
        self.flag = True
        if self.direction == 0:
            self.image = pygame.transform.flip(self.image, True, False)
        
    
    def display(self):
        self.bullet_list.append(Bullet())
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():
                self.bullet_list.remove(bullet)
    def check(self):
        if self.pos.x == 0:
            return True
        else:
            return False
    def render(self, sur):
        sur.blit(self.image, self.rect)
    
    def update(self, assets_path):
        if self.hp <= 0:
            self.kill()
            self.flag = False

class Bullet(pygame.sprite.Sprite):
    def __init__(self, assets_path, cannon):
        super().__init__()
        self.image = pygame.image.load(os.path.join(assets_path, "Bomb_test.png"))
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/3), int(self.size[1]/3)))
        self.x = cannon.pos.x 
        self.y = 250  
        self.direction = cannon.direction
    def move(self):
        if (self.x < 700 and self.x > 0 and self.direction == 0):
            self.x += 5
        elif (self.x < 700 and self.x > 0 and self.direction == 1):
            self.x -= 5
        elif (self.x >= 700 or self.x <= 0):
            self.kill()
    def render(self, sur):
        sur.blit(self.image, (self.x, self.y))
            