import math
import random
import pygame
from pygame import mixer

pygame.init()
pygame.display.set_caption("Space Fight")
pygame.display.set_icon(pygame.image.load('superpower.png'))
win = pygame.display.set_mode((800, 600))

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
game_ov = pygame.font.Font('freesansbold.ttf', 64)

Background = pygame.image.load('Background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)
playerImg = pygame.image.load('spaceship.png')
px, py, vel = 368, 500, 5
bulletImg = pygame.image.load('bullet.png')
bx, by, byc, b_state = 0, 0, 10, 'ready'

enemyNumber = 6
enemyImg, ex, ey, exc = [], [], [], []
for i in range(enemyNumber):
    enemyImg.append(pygame.image.load('enemy.png'))
    ex.append(random.randint(0, 734))
    ey.append(random.randint(64, 300))
    exc.append(2)


def showScore(x, y):
    sco = font.render("Score :"+str(score), True, (255, 255, 255))
    win.blit(sco, (x, y))

def game_over():
    gav = game_ov.render("GAME OVER", True, (255, 255, 255))
    win.blit(gav, (200, 250))

def player(x, y):
    win.blit(playerImg, (x, y))


def enemy(x, y, po):
    win.blit(enemyImg[po], (x, y))


def fire(x, y):
    global b_state
    b_state = "fire"
    win.blit(bulletImg, (x + 20, y + 10))


def isCollision(ex, ey, bx, by):
    distance = math.sqrt((math.pow(ex - bx, 2)) + (math.pow(ey - by, 2)))
    if distance < 27:
        return True
    return False


run = True
while run:
    win.fill((0, 0, 0))
    win.blit(Background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and b_state == "ready":
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                by, bx = py, px
                fire(bx, by)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        px -= vel

    if keys[pygame.K_RIGHT]:
        px += vel

    # if keys[pygame.K_UP]:
    #     py -= vel
    #
    # if keys[pygame.K_DOWN]:
    #     py += vel

    if px >= 736:
        px = 736
    elif px <= 0:
        px = 0
    if py >= 536:
        py = 536
    elif py <= 0:
        py = 0
    for i in range(enemyNumber):
        if ey[i] >= 480:
            for j in range(enemyNumber):
                ey[j] = 1000
            game_over()
            # run = False
            break
        if ex[i] >= 736:
            exc[i] = -2
            ey[i] += 40
        elif ex[i] <= 0:
            exc[i] = 2
            ey[i] += 40
        ex[i] += exc[i]
        if isCollision(ex[i], ey[i], bx, by):
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            by = py
            b_state = "ready"
            ex[i], ey[i] = random.randint(0, 734), random.randint(64, 300)
            score += 1
        enemy(ex[i], ey[i], i)


    if by <= 0:
        by = py
        b_state = "ready"
    if b_state is "fire":
        fire(bx, by)
        by -= 5
    showScore(10, 10)
    player(px, py)
    pygame.display.update()

pygame.quit()
