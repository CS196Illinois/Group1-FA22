import pygame
import os
from pygame.locals import *
import sys
import random
from tkinter import filedialog #from the GUI library Tkinter
from tkinter import * #Tkinter is used to generate additional windows
from constants import *

class Background(pygame.sprite.Sprite):
    def __init__(self, bg):
        super().__init__()
        #load image into var, load method takes in file path of image
        #if image is in same directory, only name and extension is needed
        self.bgimage = bg
        #\Users\helen\Downloads\Background.png
        #store x and y pos of background, good for scrolling backgrounds
        self.bgY = 0
        self.bgX = 0

    #render is used to display the background onto the window
    #blit will draw an image object with the input coordinate as the origin point 
    #origin is the top left corner of the pygame window

    def render(self, sur):
        sur.blit(self.bgimage, (self.bgX, self.bgY))