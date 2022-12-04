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

class StageDisplay(pygame.sprite.Sprite):
    def __init__(self, level, displaysurface):
        super().__init__()
        self.font = pygame.font.SysFont('Courier', 100)
        self.posx = -100
        self.posy = 100
        self.display = False
    def move_display(self):
        self.text_surface = self.font.render('Stage: ' + str(level), False, (0, 0, 0))   
        if self.posx < 700:
            self.posx += 5
            