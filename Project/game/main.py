import pygame
import os
from pygame.locals import *
import sys
import random
from tkinter import filedialog #from the GUI library Tkinter
from tkinter import * #Tkinter is used to generate additional windows
from constants import *
from background import *
from ground import *
from player import *
from enemy import *

#initializing variables and settings

pygame.init() #begin pygame

#create absolute path
base_path = os.path.dirname(__file__)
print(base_path)

assets_path = os.path.join(base_path, "Assets")
print(assets_path)

#loading animations
#creates display for pygame video, and changes title of window to "game"
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


#creates an event called hit_cooldown by adding 1 into the current index of pygame events
#makes surue that pygame won't record 60 collisions (how many it checks for in one second)


#initializing classes
#creating barebones of main classes



#put all sprite groups in the global space 
background = Background(pygame.image.load(os.path.join(assets_path, "Background.png")))
ground = Ground(pygame.image.load(os.path.join(assets_path, "Ground.png")))
#the collision detection functions that detect collisions requires a sprite group as a paramter
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player(assets_path)
Playergroup = pygame.sprite.Group()
Playergroup.add(player)
enemy = Enemy(assets_path)
enemygroup = pygame.sprite.Group()
enemygroup.add(enemy)



#Creating game and event loop
#everything in game loop is meant to be code that needs to be refreshed/updated every frame
#an event is created every time something happens 
while True:
    player.gravity_check(player, ground_group)
    for event in pygame.event.get():
        #Will run when the close window button is clicked 
        if event.type == QUIT:
            pygame.quit()
            sys.exit

        #For events that occur upon clicking the mouse (left)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.attacking == False: # checking to make sure that we only attack after the first is over 
                    player.attack(enemy)
                    player.attacking = True
        #event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_RETURN: # enter key 
                if player.attacking == False: # checking to make sure that we only attack after the first is over 
                    player.attack(enemy)
                    player.attacking = True
        #automatically disables cooldown once something is hit 
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)
    
    player.update()
    if player.attacking == True:
        player.attack(enemy)
    player.move()
    # Render functions ----
    #order matters, we must draw the background before drawing the ground
    
    #display and background related functions
    background.render(displaysurface)
    ground.render(displaysurface)
    #rendering sprites
    player.render(displaysurface, player)
    for i in enemygroup:
        i.update(assets_path)
        i.move()
        i.render(displaysurface)

    pygame.display.update()
    FPS_CLOCK.tick(FPS)

