import pygame
import sys
import random
from donas import Dona

from config import *

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("donuts war")

#----------------------------------------------------
#paso para hacer el icono 
icono = pygame.image.load("./assets/imagenes/dona.png").convert_alpha()
icono = pygame.transform.scale(icono,SIZE_ICON)
pygame.display.set_icon(icono)
#--------------------------------------------------------------
#pasos para el fondo
fondo = pygame.image.load("./assets/imagenes/background.jpg").convert()
fondo = pygame.transform.scale(fondo,SIZE_SCREEN)
#-----------------------------------------------------------------------------------------
donas = []
for i in range(10):
    x = random.randrange(30,WIDTH-30)
    y = random.randrange(-1000,0)

    dona = Dona(DONUT_SIZE,(x,y), "./assets/imagenes/dona.png")

    donas.append(dona)
#----------------------------------------------------------------
#homero 
homero_l = pygame.image.load("./assets/imagenes/homer_left.png").convert_alpha()
homero_l = pygame.transform.scale(homero_l,HOMERO_SIZE)

homero_r = pygame.image.load("./assets/imagenes/homer_right.png").convert_alpha()
homero_r = pygame.transform.scale(homero_r,HOMERO_SIZE)

#---------------------------------------------------------------------------
#rectangulo homero
rect_homer = homero_l.get_rect()
rect_homer.midbottom = (CENTER_X,DISPLAY_BOTTOM)
#----------------------------------------------------------------------
homero = homero_l
#-------------------------------------------------------------------------
#dona
#dona = pygame.image.load("./assets/imagenes/dona.png").convert_alpha()
#dona = pygame.transform.scale(dona,DONUT_SIZE)
#rect_dona = dona.get_rect()
#rect_dona.midtop = DISPLAY_MIDTOP
#flag_dona = True
#---------------------------------------------------------------------------------
#rect boca
rect_boca = pygame.rect.Rect(0,0,50,10)
rect_boca.x = rect_homer.x + 40 #estas posiciones para que empiece en la boca del homero
rect_boca.y = rect_homer.y + 130
#------------------------------------------------------------------------------------------
#sonido ouch
sonido = pygame.mixer.Sound("./assets/sonido/ouch.mp3")
flag_sound = True
#---------------------------------------------------------------------------------
#fuente
font = pygame.font.Font("./assets/simpsons.ttf",48)
#como una flag
score = 0

while True:
    clock.tick(FPS)#tiempo fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()#lista de boleanos
    
    
    #movimientos de homer
    if keys[pygame.K_LEFT]:
        if rect_homer.left > DISPLAY_LEFT:
            rect_homer.x -= HOMER_SPEED
            rect_boca.x = rect_homer.x + 45
            rect_boca.y = rect_homer.y + 130
            homero = homero_l

    if keys[pygame.K_RIGHT]:
        if rect_homer.right < DISPLAY_RIGHT:
            rect_homer.x += HOMER_SPEED
            rect_boca.x = rect_homer.x + 60
            rect_boca.y = rect_homer.y + 130
            homero = homero_r
    
    

    #colision
    #if rect_boca.colliderect(rect_dona):
    #    flag_dona = False
    #    if flag_sound:
    #        score += 1
    #        sonido.play()
    #       flag_sound = False
    #    else:
    #        flag_sound = True

    screen.blit(fondo,ORIGIN)
    
    screen.blit(font.render("Score: "+ str(score),True,GREEN),SCORE_POS)

    pygame.draw.rect(screen,RED,rect_boca)

    screen.blit(homero,rect_homer)

    #caida de las donas
    for dona in donas:
        if dona.rect.bottom < DISPLAY_BOTTOM:
            flag_dona = True
            flag_sound = True
            if dona.active:
                dona.update()
            else:
                dona.rect.y = 0

        if rect_boca.colliderect(dona.rect):
            dona.active = False
            if flag_sound:
                score += 1
                sonido.play()
                flag_sound = False
            else:
                flag_sound = True

        if dona.active:
            screen.blit(dona.image,dona.rect)

    pygame.display.flip()