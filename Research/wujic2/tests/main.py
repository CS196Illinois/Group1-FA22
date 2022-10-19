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

#Setups
pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
state=C.RUNNING
p=player.Player()

#Functions
 
def update(): #Function that updates info on screen
	keys=pygame.key.get_pressed()
	p.update(keys)

def refresh(): #Function that refreshes the screen so the updates are displayed
	screen.fill((0, 0, 0))
	screen.blit(p.surf, p.rect)
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
				print(state)
       	#Check if the game is quit
		elif i.type==QUIT:
			state=C.END

	update()
	refresh()
	clock.tick(C.FRAME_RATE)
  