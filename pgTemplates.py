import pygame as pg
import random
from options import *

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

allSprites = pg.sprite.Group()

GameInProcess = True

while GameInProcess:

    clock.tick(FPS)




    screen.fill(BLACK)
    allSprites.draw(screen)

    pg.display.flip()

pg.quit()