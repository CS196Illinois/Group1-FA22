import pygame
import os
from pygame.locals import *
import sys
from tkinter import * #Tkinter is used to generate additional windows
from constants import *
from background import *
from ground import *
from player import *
from enemy import *
from bishop import *
from lightning import *
from Cannon import*
#from Bullet import*
from bishop import *
from lightning import *

#initializing variables and settings

pygame.init() #begin pygame

#create absolute path
base_path = os.path.dirname(__file__)
print(base_path)

assets_path = os.path.join(base_path, "Assets")
print("line 24: " + str(assets_path))

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
bishop = Bishop(assets_path)
enemygroup.add(bishop)
enemygroup.add(enemy)
lightninggroup = pygame.sprite.Group()
cannon = Cannon(assets_path)
enemygroup.add(cannon)
bulletgroup = pygame.sprite.Group()
#bullet = Bullet(assets_path, cannon)
#bulletgroup.add(bullet)
clock = 1001
cclock = 0
lightninggroup = pygame.sprite.Group()
clock = 1001
cclock = 0
enemy.sequence = 0
#Creating game and event loop
#everything in game loop is meant to be code that needs to be refreshed/updated every frame
#an event is created every time something happens 
while True:
    #print('bullet x: ' + str(bullet.x) + ' y: ' + str(bullet.y))
    player.gravity_check(player, ground_group)
    #print('line 87')
    for event in pygame.event.get():
        #Will run when the close window button is clicked 
        if event.type == QUIT:
            pygame.quit()
            sys.exit

        #For events that occur upon clicking the mouse (left)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.attacking == False: # checking to make sure that we only attack after the first is over 
                    player.attack(enemy)
                    player.attack(bishop)
                    player.attack(cannon)
                    player.attacking = True
        #event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump(ground_group)
            if event.key == pygame.K_RETURN: # enter key 
                if player.attacking == False: # checking to make sure that we only attack after the first is over 
                    player.attack(enemy)
                    player.attack(bishop)
                    player.attack(cannon)
                    player.attacking = True
        #automatically disables cooldown once something is hit 
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)

        if event.type == enemy_cooldown:
            for i in enemygroup:
                i.cooldown = False
            pygame.time.set_timer(enemy_cooldown, 0)
        
        if event.type == TELEPORT and bishop.death == False:
            bishop.teleport(assets_path)

        if event.type == SUMMONLIGHTNING and bishop.death == False and cannon.death == True: 
            bishop.is_summoning = True
            cclock = clock
        
        if (event.type == BULLLETFIRE and cannon.flag):
            b = Bullet(assets_path, cannon)
            bulletgroup.add(b)

    player.update()
    if player.attacking == True:
        player.attack(enemy)
        player.attack(bishop)
        player.attack(cannon)
    player.move()
    # Render functions ----
    #order matters, we must draw the background before drawing the ground
    if player.current_health == 0:
        player.kill()
    
    #display and background related functions
    background.render(displaysurface)
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
    if not cannon.flag and not cannon.death and enemy.death:
        cannon.flag = True
        pygame.time.set_timer(BULLLETFIRE, 2000)
    if enemy.sequence == 0:
        enemy.update(assets_path)
        if enemy.cooldown == False:
            enemy.move()
        for j in Playergroup:
            if enemy.rect.colliderect(j.rect):
                enemy.enemy_hit(j)
        enemy.render(displaysurface)
    elif enemy.sequence == 1 and not cannon.death:
        cannon.update(assets_path)
        if cannon.cooldown == False:
            cannon.move()
        for j in Playergroup:
            if cannon.rect.colliderect(j.rect):
                cannon.enemy_hit(j)
        cannon.render(displaysurface)
    elif bishop.is_summoning == False:
        bishop.move()
        bishop.update(assets_path)
        bishop.render(displaysurface, enemy)
        if (bishop.pos.x > player.pos.x):
            bishop.updateLeft(assets_path)
        else:
            bishop.updateRight(assets_path)
    """for i in enemygroup:
        if i != bishop:
            i.update(assets_path)
            if i.cooldown == False:
                i.move()
            for j in Playergroup:
                if i.rect.colliderect(j.rect):
                    i.enemy_hit(j)
            i.render(displaysurface)
        elif i == bishop and bishop.is_summoning == False:
            i.move()
            i.update(assets_path)
            i.render(displaysurface, enemy)
            if (bishop.pos.x > player.pos.x):
                i.updateLeft(assets_path)
            else:
                i.updateRight(assets_path)"""
    for i in lightninggroup:
        i.update(assets_path, player)
        i.render(displaysurface)
    if clock - cclock == 0:
        cpos = player.pos.x
    if clock - cclock == 30 or clock - cclock == 60 or clock - cclock == 90 or clock - cclock == 120 or clock - cclock == 150:
        lightning = Lightning(assets_path, cpos, player.rect.bottom)
        lightninggroup.add(lightning)
        cpos = player.pos.x

    for i in bulletgroup:
        i.move()
        for j in Playergroup:
                if i.rect.colliderect(j.rect):
                    i.hit(j)
        i.render(displaysurface)
        
    
    if bishop.is_summoning == True:
        bishop.summon(assets_path)
        bishop.render(displaysurface, enemy)
        bishop.move()
        bishop.update(assets_path)
    pygame.display.update()
    FPS_CLOCK.tick(FPS)
    clock += 1