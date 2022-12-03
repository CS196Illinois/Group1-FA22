import pygame
import os
from pygame.locals import *
import sys
import random
from tkinter import filedialog #from the GUI library Tkinter
from tkinter import * #Tkinter is used to generate additional windows

#declaring variables to be used through the program
pygame.init()
hit_cooldown = pygame.USEREVENT + 1
SUMMONLIGHTNING = pygame.USEREVENT + 2
TELEPORT = pygame.USEREVENT + 3
JMPCOOLDOWN = pygame.USEREVENT + 4
pygame.time.set_timer(SUMMONLIGHTNING, random.randint(3000, 5000))
pygame.time.set_timer(TELEPORT, random.randint(5000, 10000))
vec = pygame.math.Vector2 #creates a vector to record x and y pos of Player
#define height and width of screen
HEIGHT = 350 
WIDTH = 700
#acceleration, friction for physics 
ACC = 0.3
FRIC = -0.10
#frames per second 
FPS = 60
#clock object used to limit game loop to 60fps
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

