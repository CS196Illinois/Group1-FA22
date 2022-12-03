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
class Grave(Enemy):
    def __init__(self, assets_path):
        super().__init__(assets_path)
        self.move_frame = 0
        self.summon_frame = 0
        self.death_frame = 0