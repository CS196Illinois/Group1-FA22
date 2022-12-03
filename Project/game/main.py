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
from bishop import *
from lightning import *
from bishop import *
from lightning import *
from button import *

#initializing variables and settings

pygame.init() #begin pygame
pygame.font.init()

#create absolute path
base_path = os.path.dirname(__file__)
print(base_path)

assets_path = os.path.join(base_path, "Assets")
print("line 24: " + str(assets_path))

#loading animations
#creates display for pygame video, and changes title of window to "game"
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pawn's Game")

#creates an event called hit_cooldown by adding 1 into the current index of pygame events
#makes surue that pygame won't record 60 collisions (how many it checks for in one second)

#initializing classes

#creating barebones of main classes

#intro materials
backgroundimage = pygame.image.load(os.path.join(assets_path, "Background.png"))
background2 = Background(backgroundimage, 1, 1)
ground = Ground(pygame.image.load(os.path.join(assets_path, "Ground.png")))
start_img = pygame.image.load(os.path.join(assets_path, "start_btn.png"))
exit_img = pygame.image.load(os.path.join(assets_path, "exit_button.png"))
start_button = Button(100, 200, start_img, 0.8)
exit_button = Button(450, 200, exit_img, 0.8)
exitVictory = Button(500, 300, exit_img, 0.3)

#text
titleFont = pygame.font.SysFont('Courier', 100)
text_surface = titleFont.render('PAWN', False, (0, 0, 0))
#game start vars
start_run = True
game_run = False
while start_run:
    background2.render(displaysurface)
    ground.render(displaysurface)
    displaysurface.blit(text_surface, (250, 50))
    if (start_button.draw(displaysurface)):
        start_run = False
        game_run = True

    if (exit_button.draw(displaysurface)):
        start_run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()


#put all sprite groups in the global space

#victory screen
victory_image = pygame.image.load(os.path.join(assets_path, "victoryScreen.jpg"))
congrats = Background(victory_image, 0.7, 0.4)

#game over screen
game_over_image = pygame.image.load(os.path.join(assets_path, "game_over.jpg"))
game_over = Background(game_over_image, 1.2, 1)
#the collision detection functions that detect collisions requires a sprite group as a paramter

ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player(assets_path)
Playergroup = pygame.sprite.Group()
Playergroup.add(player)
enemy = Enemy(assets_path)
bishop = Bishop(assets_path)
enemygroup = pygame.sprite.Group()
enemygroup.add(bishop)
enemygroup.add(enemy)
lightninggroup = pygame.sprite.Group()
clock = 1001
cclock = 0
lightninggroup = pygame.sprite.Group()
clock = 1001
cclock = 0
#Creating game and event loop

#everything in game loop is meant to be code that needs to be refreshed/updated every frame
#an event is created every time something happens 
while game_run:
    player.gravity_check(player, ground_group)
    #print('line 87')
    for event in pygame.event.get():
        #Will run when the close window button is clicked 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        #For events that occur upon clicking the mouse (left)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.attacking == False: # checking to make sure that we only attack after the first is over 
                    player.attack(enemy)
                    player.attack(bishop)
                    player.attacking = True
        #event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump(ground_group)
            if event.key == pygame.K_RETURN: # enter key 
                if player.attacking == False: # checking to make sure that we only attack after the first is over 
                    player.attack(enemy)
                    player.attack(bishop)
                    player.attacking = True
        #automatically disables cooldown once something is hit 
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)

        if event.type == enemy_cooldown:
            enemy.cooldown = False
            pygame.time.set_timer(enemy_cooldown, 0)
        
        if event.type == TELEPORT and bishop.death == False:
            bishop.teleport(assets_path)

        if event.type == SUMMONLIGHTNING and bishop.death == False and enemy.death == True: 
            bishop.is_summoning = True
            cclock = clock

    player.update()
    if player.attacking == True:
        player.attack(enemy)
        player.attack(bishop)
    player.move()
    # Render functions ----
    #order matters, we must draw the background2 before drawing the ground
    #order matters, we must draw the background before drawing the ground
    if player.current_health == 0:
        player.kill()
    
    #display and background2 related functions
    background2.render(displaysurface)
    ground.render(displaysurface)
    #healthbar
    pygame.draw.rect(displaysurface,player.get_healthbar_color(),(10,10,player.get_heatlhbar_length(),25))
    pygame.draw.rect(displaysurface,(255,255,255),(10,10,200,25),4)
    
    #rendering sprites
    for p in Playergroup:
        p.render(displaysurface, player)
    # if player.health > 0:
    #     displaysurface.blit(player.image, player.rect)
#    health.render()
    for i in enemygroup:
        if i != bishop:
            level = 1
            i.update(assets_path)
            if i.cooldown == False:
                i.move()
            for j in Playergroup:
                if i.rect.colliderect(j.rect):
                    i.enemy_hit(j)
            i.render(displaysurface)
        elif i == bishop and bishop.is_summoning == False:
            level = 2
            i.move()
            i.update(assets_path)
            i.render(displaysurface, enemy)
            if (bishop.pos.x > player.pos.x):
                i.updateLeft(assets_path)
            else:
                i.updateRight(assets_path)
    for i in lightninggroup:
        i.update(assets_path, player)
        i.render(displaysurface)
    if clock - cclock == 0:
        cpos = player.pos.x
    if clock - cclock == 30 or clock - cclock == 60 or clock - cclock == 90 or clock - cclock == 120 or clock - cclock == 150:
        lightning = Lightning(assets_path, cpos, player.rect.bottom)
        lightninggroup.add(lightning)
        cpos = player.pos.x

    if bishop.is_summoning == True:
        bishop.summon(assets_path)
        bishop.render(displaysurface, enemy)
        bishop.move()
        bishop.update(assets_path)
    
    if bishop.death == True:
        congrats.render(displaysurface)
        if exitVictory.draw(displaysurface):
            pygame.quit()

    if player.current_health <= 0:
        player.alive = False
        player.kill()
        bishop.kill()
        game_over.render(displaysurface)
        if exitVictory.draw(displaysurface):
            pygame.quit()
    
    pygame.display.update()
    FPS_CLOCK.tick(FPS)
    clock += 1
