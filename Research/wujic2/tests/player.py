import pygame
from pygame.locals import (
	K_w,
	K_a,
	K_d,
	K_ESCAPE,
	KEYDOWN,
	QUIT
)
import constants as C

class Player(pygame.sprite.Sprite):
    def __init__(self, location):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.x, self.y = location
        self.rect.left=location[0]*C.TILE_WIDTH
        self.rect.top=location[1]*C.TILE_HEIGHT
        self.JUMPVEL = 30
        self.SPEED = 10
        self.JUMPNUM = 1
        # Velocity and acceleration of the player
        self.direction = 0
        self.jumpcount = self.JUMPNUM
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = C.GRAVITY
        self.on_ground = False
        self.jump = False
        self.disx = 0
        self.disy = 0

    # Move the sprite based on user keypresses
    def update(self, pressed_keys, structure):
        if pressed_keys[K_a]:
            self.direction = -1
        elif pressed_keys[K_d]:
            self.direction = 1
        else:
        	self.direction = 0
        if pressed_keys[K_w] & self.jumpcount>0:
        	self.vy = -self.JUMPVEL
        	self.jumpcount -= 1

        # Updating velocity and acceleration of player
        self.vx = self.direction*self.SPEED+self.ax
        self.disx += self.vx
        if self.vy < 40:
        	self.vy += self.ay # In pygame, y is higher the lower it is on the screen
        else:
        	self.vy = 40
        self.disy += self.vy
        print(self.disx, self.disy)
        
        for i in structure:
        	if i.rect.colliderect(self.rect.x + self.disx, self.rect.y, self.rect.width, self.rect.height):
        		if self.vx < 0:
        			self.disx = i.rect.right-self.rect.left
        		elif self.vx >= 0:
        			self.disx = i.rect.left-self.rect.right
        	if i.rect.colliderect(self.rect.x, self.rect.y + self.disy, self.rect.width, self.rect.height):
        		if self.vy < 0:
        			self.disy = i.rect.bottom-self.rect.top
        			self.vy = 0
        		elif self.vy >= 0:
        			self.disy = i.rect.top-self.rect.bottom
        			self.vy = 0
        			self.jumpcount = self.JUMPNUM


        self.rect.move_ip(self.disx, self.disy)
        self.disx=self.disy = 0
        """for i in  pygame.sprite.spritecollide(self, structure, False):
        	i.collide(self)
        	if not pygame.sprite.spritecollideany(self, structure):
        		self.on_ground = False
        if self.on_ground:
        	if self.jump:
        		self.vy = -self.JUMPVEL
        		self.rect.move_ip(0, self.vy)
        		self.jumpcount = 1
        	else:
        		self.vy = 0"""

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > C.SCREEN_WIDTH:
            self.rect.right = C.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= C.SCREEN_HEIGHT:
            self.rect.bottom = C.SCREEN_HEIGHT
            self.jumpcount = self.JUMPNUM
 