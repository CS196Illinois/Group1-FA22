#Imports
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
import player
import tiles

#Setups
pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
state=C.RUNNING
p=player.Player((0,0))
a=[-1 for i in range(C.MAP_SIZE[1])] #just used for initializing
room=[a.copy() for i in range(C.MAP_SIZE[0])]
for i in room:
	i[11] = 0
room[3][10] = 0
room[5][9] = 0
room[8][10] = 0
#for i in room:
#	i[len(room[0])-1] = 0
all_entity=pygame.sprite.Group()
all_entity.add(p)
structure=pygame.sprite.Group()
for i in range(C.MAP_SIZE[0]):
	for j in range(C.MAP_SIZE[1]):
		if room[i][j] != -1:
			newstru=tiles.Tile(C.TAGS[room[i][j]], (i,j))
			structure.add(newstru)
			all_entity.add(newstru)


#Functions

def update(): #Function that updates info on screen
	keys=pygame.key.get_pressed()
	p.update(keys, structure)


def refresh(): #Function that refreshes the screen so the updates are displayed
	screen.fill((255, 255, 255))
	for i in all_entity:
		screen.blit(i.surf, i.rect)
	pygame.display.flip()

#Main loop
while state==C.RUNNING:
	#Event processing
	for i in pygame.event.get():
		#Process keys
		if i.type==KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
			if i.key==K_ESCAPE:
				state=C.PAUSE
       	#Check if the game is quit
		elif i.type==QUIT:
			state=C.END

	update()
	refresh()
	clock.tick(C.FRAME_RATE)
  