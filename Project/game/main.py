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
from knight import *
from Cannon import*
#from Bullet import*
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

backgroundGroup = pygame.sprite.Group()
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
knight = Knight(assets_path)
enemygroup.add(knight)
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
                    if knight.death == True:
                        player.attack(bishop)
                    if enemy.death == True and knight.jmpcooldown == True:
                        player.attack(knight)
                    player.attack(cannon)
                    player.attacking = True
        #event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump(ground_group)
            if event.key == pygame.K_RETURN: # enter key 
                if player.attacking == False: # checking to make sure that we only attack after the first is over 
                    player.attack(enemy)
                    if knight.death == True:
                        player.attack(bishop)
                    if enemy.death == True and knight.jmpcooldown == True:
                        player.attack(knight)
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
        
        
        if event.type == TELEPORT and bishop.death == False and bishop.is_summoning == False:
            bishop.teleport(assets_path)

        if event.type == SUMMONLIGHTNING and bishop.hp > 0 and knight.death == True: 
            bishop.is_summoning = True
            cclock = clock
        
        if event.type == JMPCOOLDOWN and cannon.death == True:
            knight.jmpcooldown = False
            pygame.time.set_timer(JMPCOOLDOWN, 0)
    
        
        
        if (event.type == BULLLETFIRE and cannon.flag):
            b = Bullet(assets_path, cannon)
            bulletgroup.add(b)

    player.update()
    if player.attacking == True:
        player.attack(enemy)
        if knight.death == True:
            player.attack(bishop)
        if enemy.death == True and knight.jmpcooldown == True:
            player.attack(knight)
        player.attack(cannon)
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
    if not cannon.flag and not cannon.death and enemy.death:
        cannon.flag = True
        pygame.time.set_timer(BULLLETFIRE, 2000)
    if enemy.sequence == 0:
        enemy.update(assets_path, player)
        if enemy.cooldown == False:
            enemy.move(player)
        for j in Playergroup:
            if enemy.rect.colliderect(j.rect):
                enemy.enemy_hit(j)
        enemy.render(displaysurface, enemy)
    elif enemy.sequence == 1 and not cannon.death:
        cannon.update(assets_path)
        if cannon.cooldown == False:
            cannon.move(player)
        for j in Playergroup:
            if cannon.rect.colliderect(j.rect):
                cannon.enemy_hit(j)
        cannon.render(displaysurface)
    elif bishop.is_summoning == False and knight.death == True:
        bishop.move()
        bishop.update(assets_path)
        bishop.render(displaysurface, knight)
        if (bishop.pos.x > player.pos.x):
            bishop.updateLeft(assets_path)
        else:
            bishop.updateRight(assets_path)
    """for i in enemygroup:
        if i != bishop:
            i.update(assets_path, player.pos.x)
            i.move(player.rect)
            i.render(displaysurface, enemy)
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
            i.render(displaysurface, knight)
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

    if cannon.death == True:
        knight.jump(player, cannon)
        knight.render(displaysurface, cannon)
        knight.move(player)
        knight.update(assets_path, player.pos.x)
        if knight.hp <= 0:
            knight.kill()

        
    
    if bishop.is_summoning == True:
        bishop.summon(assets_path, player.pos.x)
        bishop.render(displaysurface, knight)
        bishop.move()
        bishop.update(assets_path)
    
    if bishop.death == True and bishop.deathcounter > 300:
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