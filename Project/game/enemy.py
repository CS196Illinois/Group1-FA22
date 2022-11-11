import pygame
import os
from pygame.locals import *
import sys
import random
from tkinter import filedialog #from the GUI library Tkinter
from tkinter import * #Tkinter is used to generate additional windows
from constants import *

pygame.init()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, assets_path):
        super().__init__()
        #loads image, gets rect object 
        self.image = pygame.image.load(os.path.join(assets_path, "Enemy1.png"))
        
        self.rect = self.image.get_rect()
        #creates two vectors for pos and velocity with two componenets each
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.hp = 100
        #randomizing
        #self.direction takes a random integer betwee 0 and 1
        #self.vel.x will take a value between 2 and 6 (and divide by 2 to make sure its not too fast)
        self.direction = random.randint(0, 1) #0 for right, 1 for left
        self.vel.x = random.randint(2, 6) / 2 #randomizing velocity of enemy

        #sets starting position 
        #sets the initial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235
    def move(self):
        # causes the enemy to change directions upon reaching the end of screen
        if self.pos.x >= (WIDTH-20): # makes sure there is a little margin between the enemy and the screen
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0
        
        #enemy is only assigned magnitude of the velocity (not direction) and therefore only has speed
        #code will either subtract the velocity or add it into position x based on direction
        #updates position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
        
        self.rect.center = self.pos #Updates rect 
    def render(self,sur):
        #displayed the enemy on screen
        sur.blit(self.image, (self.pos.x, self.pos.y))
    def update(self, assets_path):
        if self.hp < 30:
            self.image = pygame.image.load(os.path.join(assets_path, "Enemy2.png"))
        if self.hp < 0:
            self.kill()