import pygame
import os
from pygame.locals import *
import sys
import random
from tkinter import filedialog #from the GUI library Tkinter
from tkinter import * #Tkinter is used to generate additional windows
from constants import *

pygame.init()
class Player(pygame.sprite.Sprite):
    def __init__(self, assets_path):
        super().__init__()
        self.image = pygame.image.load(os.path.join(assets_path, "Player_Sprite_R.png"))
        self.rect = self.image.get_rect()
        self.swordHit = pygame.Rect(self.rect.right - 20, self.rect.top, 20, self.rect.height)
        self.jumping = False

    #  Position and direction
        self.vx = 0
        self.pos = vec((340, 240)) #pos of player
        self.vel = vec(0, 0) #velocity of player
        self.acc = vec(0, 0) #acceleration of player
        self.direction = "RIGHT" #current direction of  the player

    # Movement
        self.jumping = False
        self.running = False # tracks whether the player is standing still or moving
        #used to track the current frame of the character being displayed
        self.move_frame = 0
    
    # Combat
        self.hp = 100
        self.attacking = False
        self.attack_frame = 0
        self.attack_frame = 0
        self.cooldown = False
        self.attackDamage = 10

    #run animation for the right:
        self.run_ani_R = [pygame.image.load(os.path.join(assets_path, "Player_Sprite_R.png")), pygame.image.load(os.path.join(assets_path, "Player_Sprite2_R.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite3_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Sprite4_R.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite5_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Sprite6_R.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite_R.png"))]
# Run animation for the LEFT
        self.run_ani_L = [pygame.image.load(os.path.join(assets_path, "Player_Sprite_L.png")), pygame.image.load(os.path.join(assets_path, "Player_Sprite2_L.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite3_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Sprite4_L.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite5_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Sprite6_L.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite_L.png"))]
# Attack animation for the RIGHT
        self.attack_ani_R = [pygame.image.load(os.path.join(assets_path, "Player_Sprite_R.png")), pygame.image.load(os.path.join(assets_path, "Player_Attack_R.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack2_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack2_R.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack3_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack3_R.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack4_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack4_R.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack5_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack5_R.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Sprite_R.png"))]
 
# Attack animation for the LEFT
        self.attack_ani_L = [pygame.image.load(os.path.join(assets_path, "Player_Sprite_L.png")), pygame.image.load(os.path.join(assets_path, "Player_Attack_L.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack2_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack2_L.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack3_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack3_L.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack4_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack4_L.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack5_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack5_L.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Sprite_L.png"))]

    def render(self, sur, player):
        sur.blit(player.image, player.rect)
    
    def getX(self):
        return self.pos.x

    def move(self):
        #Keep a constant acceleration of 0.5 in the downwards direciton (gravity)
        self.acc = vec(0, 0.5)

        #Will set running false if the player has slowed down to a certain extent 
        #abs used to return the magnitude since velocity can be in the neg direction
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        #returns the current key presses
        pressed_keys = pygame.key.get_pressed()
        #accelerates the player in the directiown of the key presses
        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC

        #Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc #updates position with new values 
        #you can tweak this to change the ground's friction (ice, sand)

        #warping player
        #this causes character warping from one point of the screen the other
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        #if we weant to restrict the player to not move past the edge, switch WIDTH and 0
        self.rect.midbottom = self.pos #update rect with new pos
        if self.direction == "LEFT":
            self.swordHit.left = self.rect.left
        else:
            self.swordHit.left = self.rect.right
        self.swordHit.top = self.rect.top


    #only one frame must be updated per game cycle (update function will not cycle through all the movement frames at once)
    #it will keep incrementing them by one (every time called)
    def update(self):
        # return to base frame if at end of movement sequence
        if self.move_frame > 6:
            self.move_frame = 0 #we have 7 frames
            return
        #actually changes the frames
        #ensures that the frames aren't updated while the player is standing still
        #thhe player must also not be in a state of jumping
        #first direction the player is going is determined --> if velocity is greater than 0, then player is going right
        #once direction is decided, the list of images are updated 
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = self.run_ani_R[self.move_frame]
                self.direction = "RIGHT"
            else:
                self.image = self.run_ani_L[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1 #changes frame
        
        #makes sure no bugs 
        #returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = self.run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = self.run_ani_L[self.move_frame]

    
    def attack(self, enemy):
        #If attack frame has reached the end of sequence, return to base frame
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
            
        #check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = self.attack_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.correction()
            self.image = self.attack_ani_L[self.attack_frame]
        if self.swordHit.colliderect(enemy.rect):
            self.player_hit(enemy)
        
        #update the current attack frame
        self.attack_frame += 1
    def player_hit(self, enemy):
        if self.cooldown == False: #if cooldown is over 
            self.cooldown = True #enable the cooldown
            pygame.time.set_timer(hit_cooldown, 500) #resets cooldown
            enemy.hp -= 10
            if self.direction == "LEFT":
                enemy.pos.x -= 30
            else:
                enemy.pos.x += 30
            #for now!! 
            print("hit")
    
    #cancels out the 20 pixels error during the left attack
    #when we turn our character from right to left and attack, the center point of image changes (pushes player back)
    def correction(self):
        #Function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
            self.pos.x -= 20
        if self.attack_frame == 10:
            self.pos.x += 20

    def jump(self, ground_group):
        self.rect.x += 1

        #check to see if player is in contact with the ground 
        hits = pygame.sprite.spritecollide(self, ground_group, False)

        self.rect.x -= 1

        #If touching the ground, and not currently jumping, cause the player to jump
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12 #must be negative direction

    #uses spritecollide() which takes three parameters, the sprite to be tested, and the sprite group against which the sprite will be tested
    #third paramter takes a boolean value which determines whether or not to kill the sprite if a collision occurs 
    def gravity_check(self, player, ground_group):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        #check if the player has any veloicty in the downwards direction (if he's falling)
        if self.vel.y > 0:
            #if the hits var records a collision between ground and player
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

