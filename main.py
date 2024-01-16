# Imports
import pygame, sys, threading
import time
import numpy as np
pygame.init()

# Screen and font
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Loading Bar!")

FONT = pygame.font.SysFont("Roboto", 100)

# Clock
CLOCK = pygame.time.Clock()

# Work
WORK = 10000000

# Loading BG
LOADING_BG = pygame.image.load("Loading Bar Background.png")
LOADING_BG_RECT = LOADING_BG.get_rect(center=(640, 360))

# Loading Bar and variables
loading_bar = pygame.image.load("Loading Bar.png")
loading_bar_rect = loading_bar.get_rect(midleft=(280, 360))
loading_finished = False
loading_progress = 0
loading_bar_width = 8

def doWork():
	# Do some math WORK amount times
	global loading_finished, loading_progress

	for i in range(WORK):
		math_equation = 523687 / 789456 * 89456
		loading_progress = i

	loading_finished = True

# Finished text
finished = FONT.render("Done!", True, "white")
finished_rect = finished.get_rect(center=(640, 360))

# Thread
threading.Thread(target=doWork).start()

width,height = 1000,1000
screen=pygame.display.set_mode((width,height))
bg =25,25,25
screen.fill(bg)
nxC, nyC =50,50
dimCW= width / nxC
dimCH= height / nyC


gameState =np.zeros((nxC,nyC))


gameState[21,21]=1
gameState[22,22]=1
gameState[22,23]=1
gameState[21,23]=1
gameState[20,23]=1

pausa=False
# Game loop
i=0
while i==0:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill("#0d0e2e")

	if not loading_finished:
	 	loading_bar_width = loading_progress / WORK * 720

	 	loading_bar = pygame.transform.scale(loading_bar, (int(loading_bar_width), 150))
	 	loading_bar_rect = loading_bar.get_rect(midleft=(280, 360))

	 	screen.blit(LOADING_BG, LOADING_BG_RECT)
	 	screen.blit(loading_bar, loading_bar_rect)
	else:
	 	screen.blit(finished, finished_rect)

	loading_bar_width = loading_progress / WORK * 720

	loading_bar = pygame.transform.scale(loading_bar, (int(loading_bar_width), 150))
	loading_bar_rect = loading_bar.get_rect(midleft=(280, 360))

	screen.blit(LOADING_BG, LOADING_BG_RECT)
	screen.blit(loading_bar, loading_bar_rect)

	pygame.display.update()
	CLOCK.tick(50)
	i=1

while True:

    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    events=pygame.event.get()
    for event in events:
        if event.type== pygame.KEYUP:
            pausa=not pausa
        click=pygame.mouse.get_pressed()
        if sum(click)>0:
            posX,posY=pygame.mouse.get_pos()
            celX,celY = int(np.floor(posX/dimCW)),int(np.floor(posY/dimCH))
            newGameState[celX,celY]=not click[2]
    for y in range(0,nxC):
        for x in range(0,nyC):
            if not pausa:
                n_vecinos=gameState[(x-1)%nxC,(y-1)%nyC]+\
                          gameState[(x)%nxC,(y-1)%nyC]+\
                          gameState[(x+1)%nxC,(y-1)%nyC]+\
                          gameState[(x-1)%nxC,(y)%nyC]+\
                          gameState[(x+1)%nxC,(y)%nyC]+\
                          gameState[(x-1)%nxC,(y+1)%nyC]+\
                          gameState[(x)%nxC,(y+1)%nyC]+\
                          gameState[(x+1)%nxC,(y+1)%nyC]

                if gameState[x,y]==0 and n_vecinos==3:
                    newGameState[x,y]=1
                elif gameState[x,y]==1 and(n_vecinos< 2 or n_vecinos>3):
                    newGameState[x,y]=0

            poly = [((x)* dimCW,y * dimCH),
                    ((x+1)* dimCW, y * dimCH),
                    ((x+1)*dimCW, (y+1)* dimCH),
                    ((x)* dimCW,(y+1)*dimCH)]

            if newGameState[x,y]==0:
                pygame.draw.polygon(screen,(128,128,128), poly,1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    gameState=np.copy(newGameState)
    pygame.display.flip()