#!/usr/bin/python
import pygame, sys, time, random
from pygame.locals import *

pygame.init()

fpsClock = pygame.time.Clock()  # game speed control
playSurface = pygame.display.set_mode((640,480))  # canvas to display
pygame.display.set_caption("Snake Game")
pygame.display.set_icon(pygame.image.load('img/icon.png'))

# define some color
redColor = pygame.Color(255,0,0)
blackColor = pygame.Color(0,0,0)
whiteColor = pygame.Color(255,255,255)
greyColor = pygame.Color(150,150,150)

#some variable pre-defined
snakePosition = [100,100]
snakeSegments = [[100,100],[80,100],[60,100]]
raspberryPosition = [300,300]
raspberrySpawned = True
direction = "right"
changeDirection = direction

def gameover():
    gameOverFont = pygame.font.Font("freesansbold.ttf",72)
    gameOverSurface = gameOverFont.render("Game Over!",True,greyColor)
    gameOverRect = gameOverSurface.get_rect()
    gameOverRect.midtop = (320,10)
    playSurface.blit(gameOverSurface,gameOverRect)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            # detect which key be pressed
            if event.key == K_RIGHT or event.key == ord('d'):
                changeDirection = 'right'
            elif event.key == K_LEFT or event.key == ord('a'):
                changeDirection = 'left'
            elif event.key == K_UP or event.key == ord('w'):
                changeDirection = 'up'
            elif event.key == K_DOWN or event.key == ord('s'):
                changeDirection = 'down'
            elif event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    # have to notice that snake cannot turn head back
    if changeDirection == 'right' and not direction == 'left':
        direction = changeDirection
    if changeDirection == 'left' and not direction == 'right':
        direction = changeDirection
    if changeDirection == 'up' and not direction == 'down':
        direction = changeDirection
    if changeDirection == 'down' and not direction == 'up':
        direction = changeDirection

    # move a block foward
    if direction == 'right':
        snakePosition[0] += 20
    elif direction == 'left':
        snakePosition[0] -= 20
    elif direction == 'up':
        snakePosition[1] -= 20
    elif direction == 'down':
        snakePosition[1] += 20
    snakeSegments.insert(0,list(snakePosition))
    
    if snakePosition == raspberryPosition:
        raspberrySpawned = False
    else:
        snakeSegments.pop()

    if snakePosition[0] > 620 or snakePosition[0] < 0:
        gameover()
    elif snakePosition[1] > 460 or snakePosition[1] < 0:
        gameover()

    for snakeBody in snakeSegments[1:]:
        if snakePosition[0] == snakeBody[0] and snakePosition[1] == snakeBody[1]:
            gameover()

    # spawn a new raspberry
    if raspberrySpawned == False:
        x = random.randrange(1,32)
        y = random.randrange(1,24)
        raspberryPosition = [int(x*20),int(y*20)]
        raspberrySpawned = 1
    playSurface.fill(blackColor)
    for position in snakeSegments:
        pygame.draw.rect(playSurface, whiteColor, Rect(position[0],position[1],20,20))
    pygame.draw.circle(playSurface, redColor, (raspberryPosition[0]+10, raspberryPosition[1]+10), 10)
    pygame.display.flip()

    fpsClock.tick(5)    


