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
yellowColor = pygame.Color(255,255,0)

#some variable pre-defined
snakePosition = [100,100]
snakeSegments = [[100,100],[80,100],[60,100]]
raspberryPosition = [300,300]
raspberrySpawned = True
direction = "right"
score = 0
speed = 5
stopWatch = 1

def speedwarning():
    warningFont = pygame.font.Font("freesansbold.ttf",20)
    warningSurface = warningFont.render("Warning! Ready to speed up!" ,True ,redColor)
    warningRect = warningSurface.get_rect()
    warningRect.midtop = (320,10)
    playSurface.blit(warningSurface,warningRect)

def showscore():
    scoreFont = pygame.font.Font("freesansbold.ttf",18)
    scoreSurface = scoreFont.render("Score:" + str(score),True,yellowColor)
    scoreRect = scoreSurface.get_rect()
    scoreRect.midtop = (580,460)
    playSurface.blit(scoreSurface,scoreRect)

def gameover():
    # "Game Over!"
    gameOverFont = pygame.font.Font("freesansbold.ttf",72)
    gameOverSurface = gameOverFont.render("Game Over!",True,greyColor)
    gameOverRect = gameOverSurface.get_rect()
    gameOverRect.midtop = (320,10)
    # "Score:    "
    scoreSurface = gameOverFont.render("Score:" + str(score),True,yellowColor)
    scoreRect = scoreSurface.get_rect()
    scoreRect.midtop = (320,100)
    playSurface.blit(gameOverSurface,gameOverRect)
    playSurface.blit(scoreSurface,scoreRect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            # detect which key be pressed
            if (event.key == K_RIGHT or event.key == ord('d')) and not direction == 'left':
                direction = 'right'
            elif (event.key == K_LEFT or event.key == ord('a')) and not direction == 'right':
                direction = 'left'
            elif (event.key == K_UP or event.key == ord('w')) and not direction == 'down':
                direction = 'up'
            elif (event.key == K_DOWN or event.key == ord('s')) and not direction == 'up':
                direction = 'down'
            elif event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

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

    # if snake ate the raspberry
    if snakePosition == raspberryPosition:
        raspberrySpawned = False
        score += 10
        # speed up every 50 points
        if score % 50 == 0:
            speed += 2
    else:
        snakeSegments.pop()

    # if snake is out of area
    if snakePosition[0] > 620 or snakePosition[0] < 0:
        gameover()
    elif snakePosition[1] > 460 or snakePosition[1] < 0:
        gameover()

    # check if snake eats itself
    for snakeBody in snakeSegments[1:]:
        if snakePosition[0] == snakeBody[0] and snakePosition[1] == snakeBody[1]:
            gameover()

    # spawn a new raspberry
    if raspberrySpawned == False:
        x = random.randrange(1,32)
        y = random.randrange(1,24)
        raspberryPosition = [int(x*20),int(y*20)]
        raspberrySpawned = 1

    # draw the surface
    playSurface.fill(blackColor)
    for position in snakeSegments:
        pygame.draw.rect(playSurface, whiteColor, Rect(position[0],position[1],20,20))
    pygame.draw.circle(playSurface, redColor, (raspberryPosition[0]+10, raspberryPosition[1]+10), 10)
    showscore()
    if (score + 10) % 50 == 0 and stopWatch % 3 == 0:
        speedwarning()
        stopWatch = 1
    stopWatch += 1

    pygame.display.flip()

    fpsClock.tick(speed)
