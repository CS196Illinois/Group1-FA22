import pygame
import os
from pygame.locals import *
import sys
import random
from tkinter import filedialog #from the GUI library Tkinter
from tkinter import * #Tkinter is used to generate additional windows
from constants import *

class Ground(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img
        #rect around it allows for collision detection
        self.rect = self.image.get_rect(center = (350, 350))

    def render(self, sur):
        sur.blit(self.image, (self.rect.x, self.rect.y))