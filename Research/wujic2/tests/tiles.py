import pygame
from pygame.locals import (
	K_w,
	K_a,
	K_d,
	K_ESCAPE,
	KEYDOWN,
	QUIT
)
import player
import constants as C

class Tile(pygame.sprite.Sprite):
	def __init__(self, tag, location):
		super(Tile, self).__init__()
		self.surf=pygame.Surface((C.TILE_WIDTH, C.TILE_HEIGHT))
		self.surf.fill((255, 0, 0))
		self.rect=self.surf.get_rect()

		#Position on map
		self.x,self.y=location
		self.rect.left=location[0]*C.TILE_WIDTH
		self.rect.top=location[1]*C.TILE_HEIGHT
		#Type of tile
		self.tag=tag

	#detect collision
	def collide(self, player):
		if player.vy>=player.rect.bottom-self.rect.top:
			player.rect.bottom=self.rect.top-1
			player.on_ground = True
			player.vy=0
		elif player.vy<=player.rect.top-self.rect.bottom:
			player.rect.top=self.rect.bottom+1
		elif player.vx<0:
			player.rect.left=self.rect.right+1
		elif player.vx>0:
			player.rect.right=self.rect.left-1
		