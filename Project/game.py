import pygame
import os
from pygame.locals import *
import sys
import random
from tkinter import filedialog #from the GUI library Tkinter
from tkinter import * #Tkinter is used to generate additional windows

#initializing variables and settings

pygame.init() #begin pygame
#declaring variables to be used through the program

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

#create absolute path
base_path = os.path.dirname(__file__)
print(base_path)

assets_path = os.path.join(base_path, "Assets")
print(assets_path)
#creates display for pygame video, and changes title of window to "game"
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


#creates an event called hit_cooldown by adding 1 into the current index of pygame events
#makes surue that pygame won't record 60 collisions (how many it checks for in one second)
hit_cooldown = pygame.USEREVENT + 1

#loading animations
#run animation for the right:
run_ani_R = [pygame.image.load(os.path.join(assets_path, "Player_Sprite_R.png")), pygame.image.load(os.path.join(assets_path, "Player_Sprite2_R.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite3_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Sprite4_R.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite5_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Sprite6_R.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite_R.png"))]
# Run animation for the LEFT
run_ani_L = [pygame.image.load(os.path.join(assets_path, "Player_Sprite_L.png")), pygame.image.load(os.path.join(assets_path, "Player_Sprite2_L.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite3_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Sprite4_L.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite5_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Sprite6_L.png")),
             pygame.image.load(os.path.join(assets_path, "Player_Sprite_L.png"))]
# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load(os.path.join(assets_path, "Player_Sprite_R.png")), pygame.image.load(os.path.join(assets_path, "Player_Attack_R.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack2_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack2_R.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack3_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack3_R.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack4_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack4_R.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack5_R.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack5_R.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Sprite_R.png"))]
 
# Attack animation for the LEFT
attack_ani_L = [pygame.image.load(os.path.join(assets_path, "Player_Sprite_L.png")), pygame.image.load(os.path.join(assets_path, "Player_Attack_L.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack2_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack2_L.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack3_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack3_L.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack4_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack4_L.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Attack5_L.png")),pygame.image.load(os.path.join(assets_path, "Player_Attack5_L.png")),
                pygame.image.load(os.path.join(assets_path, "Player_Sprite_L.png"))]

bishop_idle_R = [pygame.image.load(os.path.join(assets_path, "1.png")), pygame.image.load(os.path.join(assets_path, "2.png")),
                pygame.image.load(os.path.join(assets_path, "3.png")),pygame.image.load(os.path.join(assets_path, "4.png")),
                pygame.image.load(os.path.join(assets_path, "5.png")),pygame.image.load(os.path.join(assets_path, "6.png")),

                pygame.image.load(os.path.join(assets_path, "1.png"))]

#initializing classes
#creating barebones of main classes

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #load image into var, load method takes in file path of image
        #if image is in same directory, only name and extension is needed
        self.bgimage = pygame.image.load(os.path.join(assets_path, "Background.png"))
        #\Users\helen\Downloads\Background.png
        #store x and y pos of background, good for scrolling backgrounds
        self.bgY = 0
        self.bgX = 0

    #render is used to display the background onto the window
    #blit will draw an image object with the input coordinate as the origin point 
    #origin is the top left corner of the pygame window

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(assets_path, "Ground.png"))
        #rect around it allows for collision detection
        self.rect = self.image.get_rect(center = (350, 350))

    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))


class Player(pygame.sprite.Sprite):
    def __init__(self):
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

    def render(self):
        displaysurface.blit(player.image, player.rect)

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
                self.image = run_ani_R[self.move_frame]
                self.direction = "RIGHT"
            else:
                self.image = run_ani_L[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1 #changes frame
        
        #makes sure no bugs 
        #returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = run_ani_L[self.move_frame]

    
    def attack(self, enemy):
        #If attack frame has reached the end of sequence, return to base frame
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
            
        #check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.correction()
            self.image = attack_ani_L[self.attack_frame]
        if self.swordHit.colliderect(enemy.rect):
            self.player_hit(enemy)
        
        #update the current attack frame
        self.attack_frame += 1
    def player_hit(self, enemy):
        if self.cooldown == False: #if cooldown is over 
            self.cooldown = True #enable the cooldown
            pygame.time.set_timer(hit_cooldown, 500) #resets cooldown
            enemy.hp -= 10
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

    def jump(self):
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
    def gravity_check(self):
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #loads image, gets rect object 
        self.image = pygame.image.load(os.path.join(assets_path, "Enemy1.png"))
        
        self.rect = self.image.get_rect()
        #creates two vectors for pos and velocity with two componenets each
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.hp = 100
        self.vel.y = -3
        #randomizing
        #self.direction takes a random integer betwee 0 and 1
        #self.vel.x will take a value between 2 and 6 (and divide by 2 to make sure its not too fast)
        self.direction = random.randint(0, 1) #0 for right, 1 for left
        self.vel.x = random.randint(2, 6) / 2 #randomizing velocity of enemy

        #sets starting position 
        #sets the initial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235
    def move(self):
        # causes the enemy to change directions upon reaching the end of screen
        if self.pos.x >= (WIDTH-20): # makes sure there is a little margin between the enemy and the screen
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0
        
        #enemy is only assigned magnitude of the velocity (not direction) and therefore only has speed
        #code will either subtract the velocity or add it into position x based on direction
        #updates position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
        
        self.rect.center = self.pos #Updates rect 
    def render(self):
        #displayed the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))
    def update(self):
        if self.hp < 30:
            self.image = pygame.image.load(os.path.join(assets_path, "Enemy2.png"))
        if self.hp < 0:
            if self.pos.y > HEIGHT:
                self.kill()
            self.image = pygame.image.load(os.path.join(assets_path, "EnemyInverse.png"))
            self.vel.y += 0.15
            self.pos.y += self.vel.y

class Bishop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(assets_path, "Enemy1.png"))
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.hp = 100
        self.direction = random.randint(0, 1) #0 for right, 1 for left
        self.vel.x = random.randint(2, 6) / 2 #randomizing velocity of enemy

        if self.direction == 0:
            self.pos.x = 50
            self.pos.y = 100
        if self.direction == 1:
            self.pos.x = WIDTH - 50
            self.pos.y = 100
    def render(self):
            #displayed the enemy on screen
            displaysurface.blit(self.image, (self.pos.x, self.pos.y))

#put all sprite groups in the global space 
background = Background()
ground = Ground()
#the collision detection functions that detect collisions requires a sprite group as a paramter
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)
enemy = Enemy()
bishop = Bishop()
enemygroup = pygame.sprite.Group()
enemygroup.add(enemy)
enemygroup.add(bishop)


#Creating game and event loop
#everything in game loop is meant to be code that needs to be refreshed/updated every frame
#an event is created every time something happens 
while True:
    player.gravity_check()
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
    background.render()
    ground.render()
    #rendering sprites
    player.render()
    for i in enemygroup:
        i.update()
        i.move()
        i.render()

    pygame.display.update()
    FPS_CLOCK.tick(FPS)

