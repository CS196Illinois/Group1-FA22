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
    def _init_(self, assets_path):
        pygame.sprite.Sprite._init_(self)
        self.img = pygame.image.load(os.path.join(assets_path, "Cannon_test.png"))
        self.img = pygame.transform.scale(self.img, (int(self.img.get_width() * scale)), (int(self.img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.bullet_List = []
        self.hit = False
        self.bomb_lists = []
        self.image_num = 0
        self.image_index = 0

    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))
    def display(self):
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():
                self.bullet_list.remove(bullet)
class Bullet(object):
    def _init_(self, screen_temp, assets_path, x, y):
        self.img = pygame.image.load(os.path.join(assets_path, "Bomb_test.png"))
        self.x = x+40  
        self.y = y-20  
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))   
    def move(self):
        self.x -= 10 
    def judge(self):
        if self.y < 0:
            return True
        else:
            return False
      
