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
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
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
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
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
        self.vy += self.ay # In pygame, y is higher the lower it is on the screen
        print(self.vx)
        self.rect.move_ip(self.vx, self.vy)

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