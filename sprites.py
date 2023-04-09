import pygame as pg
from pygame.sprite import Sprite

from options import *
import random
import numpy as np
from math import sqrt
vec = pg.math.Vector2

# class for the player
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('All_graphism_sounds/ninja/sl.png')   # load an image for the player
        self.image = pg.transform.scale(self.image, (PlayerHeight + 8, PlayerWidth + 7))  # Transform the size
        self.image.set_colorkey(BLACK)
        self.game = game    # import the Game class
        self.healthMax = 100   # Maximum health
        self.health = 100   # current health

        # resize the size of the player's rectangle
        self.rect = self.image.get_rect(width=PlayerWidth-23, height=PlayerHeight+39)

        self.rect.center = (100, HEIGHT/2)    # Starting position

        # initialisation of vectors
        self.position = vec(self.rect.center)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.dx = 0

        # Index for the animation, the direction of the player for the shurikens
        self.walkCount = 0   # from 0 to 8
        self.direction = 1   # if direction == 1 ==> the player is facing right / if direction == 0 ==> the player is facing left
        self.side = 1        # if side == 1 ==> the player is facing right / if side == -1 ==> the player is facing left

        # boolean to check each actions if the player
        self.isJumping = False
        self.left = False
        self.right = False
        self.collides = False
        self.moves = False
        self.time = 0
        self.shoots = False
        self.shurikenCoordinates = [0, 0]
        self.spamButton = False

    # Health bar for the player
    def UpdateHealthBar(self, surface):

        bar_position = [HealthX, HealthY, self.health*5, 30]
        Maxbar_position = [HealthX, HealthY, self.healthMax*5, 30]

        pg.draw.rect(surface, BLACK, Maxbar_position)
        pg.draw.rect(surface, GREEN, bar_position)

    # Function for jumps
    def jump(self):
        if self.velocity.y == 0:
            jump_fx.play()

        for tile in self.game.allPlatforms:
            hits = tile.rect.colliderect(self.rect)
            if hits:
                self.velocity.y = -PlayerJump
                self.dx = -PlayerJump
        self.rect.x -= 1

    # Function for the animation
    def walk_anim(self):

        if self.walkCount + 1 >= 8:   # because there are 8 images per animation
            self.walkCount = 0

        if self.left:  # goes left
            self.direction = 0
            self.walkCount += 1
            self.image = pg.image.load(WALKLEFT[self.walkCount])
            self.image = pg.transform.scale(self.image, (PlayerHeight + 8, PlayerWidth + 7))

        elif self.right:  # goes right
            self.direction = 1
            self.walkCount += 1
            self.image = pg.image.load(WALKRIGHT[self.walkCount])
            self.image = pg.transform.scale(self.image, (PlayerHeight + 8, PlayerWidth + 7))

        else:   # not moving
            self.image = pg.image.load(STANDING[self.direction])
            self.image = pg.transform.scale(self.image, (PlayerHeight + 8, PlayerWidth + 7))

    # An update function to change some variables if the player presses one the keys
    def update(self):
        self.acceleration = vec(0, PlayerGrav)  # the y component is constantly equal to the gravity
        keys = pg.key.get_pressed()  # get all the buttons from the keyboard

        # the player is on the screen and he wants to go left
        if keys[pg.K_LEFT] and self.rect.x > 60 and not self.collides or self.moves:
            self.acceleration.x = -PlayerSpeed   # the x component of the vector acceleration is negative (to go left)
            self.left = True
            self.side = -1
            self.right = False
            self.direction = 0

        # the player is on the screen and he wants to go right
        elif keys[pg.K_RIGHT] and self.rect.x < WIDTH - 75 and not self.collides or self.moves:
            self.acceleration.x = PlayerSpeed    # the x component of the vector acceleration is negative (to go left)
            self.left = False
            self.right = True
            self.side = 1
            self.direction = 1

        # Doing nothing
        else:
            self.left = False
            self.right = False
            self.collides = False
            self.walkCount = 0
            self.velocity.x = 0

        # the player is close from escaping
        if keys[pg.K_LEFT] and self.rect.y < 100:
            self.acceleration.x = -PlayerSpeed
            self.left = True
            self.side = -1
            self.right = False
            self.direction = 0

        # the player is close from escaping
        elif keys[pg.K_RIGHT] and self.rect.y < 100:
            self.acceleration.x = PlayerSpeed
            self.left = False
            self.right = True
            self.side = 1
            self.direction = 1

        # if the player throws a shuriken
        if keys[pg.K_SPACE] and self.left:
            self.right = False
            self.shoots = True
            self.shurikenCoordinates = [self.rect.x, self.rect.y]
            self.spamButton = True

        elif keys[pg.K_SPACE] and self.right:
            self.left = False
            self.shoots = True
            self.shurikenCoordinates = [self.rect.x, self.rect.y]
            self.spamButton = True

        elif keys[pg.K_SPACE] and not self.right and not self.left:
            self.shoots = True
            self.shurikenCoordinates = [self.rect.x, self.rect.y]
            self.spamButton = True

        # update the player's position on the screen with the vectors
        self.acceleration += self.velocity * (-0.19)
        self.velocity += self.acceleration
        self.position += self.velocity + PlayerSpeed * self.acceleration
        self.rect.midbottom = self.position

# Class for a platform
class Platform(pg.sprite.Sprite):
    def __init__(self, img, row, col):
        pg.sprite.Sprite.__init__(self)

        self.img = img
        self.image = pg.image.load(img)
        self.image = pg.transform.scale(self.image, (tileSize, tileSize))
        self.rect = self.image.get_rect()

        # position of the image on the screen
        self.rect.x = col * tileSize
        self.rect.y = row * tileSize

        # a tuple to get all the information faster
        self.tile = (self.rect, self.image)


# Class for a projectile
class Projectile(pg.sprite.Sprite):

    def __init__(self, x, y, side):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(SHURIKEN)
        self.image = pg.transform.scale(self.image, (12, 12))  # resize the shuriken

        self.rect = self.image.get_rect(width=8, height=8)
        self.side = side  # 1 or -1

        # Starting position of the projectiles when they are thrown
        if self.side == -1:
            self.rect.centery = y + 25
            self.rect.centerx = x - 10
        else:
            self.rect.centery = y + 25
            self.rect.centerx = x + 35
        self.speed = SHURIKEN_SPEED   # speed of the shuriken

    def update(self):
        self.rect.x += self.speed * self.side  # trajectory

# Class for zombies
class Zombie(pg.sprite.Sprite):

    def __init__(self, target):
        pg.sprite.Sprite.__init__(self)
        self.side = 0
        self.target = target

        self.image = pg.image.load('All_graphism_sounds/zombie/zombie_r1.png')
        self.image = pg.transform.scale(self.image, (PlayerHeight + 8, PlayerWidth))

        # resize the rectangle of the monster
        self.rect = self.image.get_rect(width=PlayerWidth-20, height=PlayerHeight+38)

        # random spawn
        self.spawn = random.randint((WIDTH/2)-100, (WIDTH/2)+100)
        self.rect.center = (self.spawn, HEIGHT/2-10)

        # initialization of vectors
        self.position = vec(self.rect.center)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

        # Some counters just like the player
        self.walkCount = 0
        self.direction = 1
        self.randSpeed = np.random.uniform(1, 2)
        self.stop = 1
        self.side = 1

        # Heath
        self.healthMax = 60
        self.health = 60

    def update(self):
        if self.target == -1:
            self.acceleration = vec(-1 * self.randSpeed * self.stop * self.side, ZombieGrav)
            self.direction = 0
        elif self.target == 1:
            self.acceleration = vec(1 * self.randSpeed * self.stop * self.side, ZombieGrav)
            self.direction = 1

        else: self.acceleration = vec(self.target, ZombieGrav)

        # just as the player
        self.acceleration += self.velocity * (-0.55)
        self.velocity += self.acceleration
        self.position += self.velocity + 1 * self.acceleration
        self.rect.midbottom = self.position

    def UpdateHealthBar(self, surface):

        bar_position = [self.rect.centerx - 25, self.rect.centery - 50, self.health, 5]
        maxbar_position = [self.rect.centerx - 25, self.rect.centery - 50, self.healthMax, 5]

        pg.draw.rect(surface, BLACK, maxbar_position)
        pg.draw.rect(surface, GREEN, bar_position)

    def walk_anim(self):
        # Same as the player

        if self.walkCount + 1 >= 24: self.walkCount = 0
        if self.walkCount == -1: self.image = pg.image.load(ZOMBIE_WALKRIGHT[1])
        elif self.walkCount == -2: self.image = pg.image.load(ZOMBIE_WALKLEFT[0])

        if self.target == -1 and self.walkCount >= 0:
            self.direction = 0
            self.walkCount += 1
            self.image = pg.image.load(ZOMBIE_WALKLEFT[self.walkCount])

        elif self.target == 1 and self.walkCount >= 0:
            self.direction = 1
            self.walkCount += 1
            self.image = pg.image.load(ZOMBIE_WALKRIGHT[self.walkCount])

        else: self.image = pg.image.load(ZOMBIE_STANDING[self.direction])
        self.image = pg.transform.scale(self.image, (PlayerHeight + 8, PlayerWidth))

# Class for raven
class Bird(pg.sprite.Sprite):

    # same as the player

    def __init__(self, target, game):
        pg.sprite.Sprite.__init__(self)

        self.game = game
        self.side = 0
        self.target = target
        self.image = pg.image.load(BIRD_ANIM_LEFT[0])
        # resize the rectangle of the bird
        self.image = pg.transform.scale(self.image, (50, 48))
        self.rect = self.image.get_rect(height=40, width=40)
        # random spawn
        self.spawn = random.randint((WIDTH/2)-100, (WIDTH/2)+100)
        self.rect.center = (self.spawn, self.spawn)
        self.randSpeed = np.random.uniform(1, 2)
        # initialization of vectors
        self.position = vec(self.rect.center)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        # Some counters just like the player
        self.walkCount = 0
        self.direction = 1   # facing right = 1 / facing left = 0
        self.stop = 1
        self.side = 1
        # Heath
        self.healthMax = 60
        self.health = 60

    # update each bird
    def update(self):
        if self.target == -1:
            self.acceleration = vec(-1 * self.randSpeed * self.stop * self.side, 0)
            self.direction = 0
        elif self.target == 1:
            self.acceleration = vec(1 * self.randSpeed * self.stop * self.side, 0)  # acc represent the vector of
            self.direction = 1
        else:
            self.acceleration = vec(0, 0)
            self.image = pg.image.load(BIRD_STANDING[self.direction])

        if self.rect.y > self.game.player.rect.y + 10: self.acceleration.y = -BirdGrav
        elif self.rect.y < self.game.player.rect.y - 10: self.acceleration.y = BirdGrav
        else: self.acceleration.y = 0

        # just as the player
        self.acceleration += self.velocity * (-0.55)
        self.velocity += self.acceleration
        self.position += self.velocity + 1 * self.acceleration
        self.rect.midbottom = self.position

    # health bar for the bird
    def UpdateHealthBar(self, surface):
        bar_position = [self.rect.centerx - 25, self.rect.centery - 50, self.health, 5]
        Maxbar_position = [self.rect.centerx - 25, self.rect.centery - 50, self.healthMax, 5]
        pg.draw.rect(surface, BLACK, Maxbar_position)
        pg.draw.rect(surface, GREEN, bar_position)

    def walk_anim(self):
        # Same as the player

        if self.walkCount + 1 >= 12:
            self.walkCount = 0

        if self.walkCount == -1:
            self.image = pg.image.load(BIRD_ANIM_RIGHT[1])

        elif self.walkCount == -2:
            self.image = pg.image.load(BIRD_ANIM_LEFT[0])

        if self.target == -1 and self.walkCount >= 0:
            self.direction = 0
            self.walkCount += 1
            self.image = pg.image.load(BIRD_ANIM_LEFT[self.walkCount])

        elif self.target == 1 and self.walkCount >= 0:
            self.direction = 1
            self.walkCount += 1
            self.image = pg.image.load(BIRD_ANIM_RIGHT[self.walkCount])

        else:
            self.image = pg.image.load(BIRD_STANDING[self.direction])

        self.image = pg.transform.scale(self.image, (50, 48))


class BaseCanon(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("All_graphism_sounds/canon/baseCanon.gif")
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(width=10, height=10)
        self.rect.center = (posCanonX + 2, posCanonY)


class Canon(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        # initialization of the canon
        self.image = pg.image.load("All_graphism_sounds/canon/Canon.gif")
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(width=50, height=50)
        self.rect.center = (posCanonX + 20, posCanonY)
        # no angles
        self.angle = 0
        self.velocity = 65
        self.launched = False

    def rotation(self, image, angle):
        # rotate an image while keeping its center and size
        orig_rect = image.get_rect()
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self):

        self.rotation(self.image, self.angle)
        self.image = pg.transform.scale(self.image, (40, 40))

    def power(self, x, y):  # Analyze the position of the player and return an appropriate initial velocity

        if 100 < x < 200 and 50 < y < 80:     return 10
        elif 50 < x < 150 and 50 < y < 175:   return 20
        elif 150 < x < 250 and 50 < y < 175:  return 40
        elif 250 < x < 350 and 50 < y < 175:  return 55
        elif 350 < x < 450 and 50 < y < 175:  return 65
        elif 450 < x < 550 and 50 < y < 175:  return 75
        elif 550 < x < 650 and 50 < y < 175:  return 85
        elif 650 < x < 750 and 50 < y < 175:  return 90
        elif 750 < x < 850 and 50 < y < 175:  return 96
        elif 850 < x < 950 and 50 < y < 175:  return 110
        elif 950 < x < 1050 and 50 < y < 175: return 120
        #############################
        elif 0 < x < 50 and 175 < y < 310:     return 15
        elif 50 < x < 150 and 175 < y < 225:   return 20
        elif 150 < x < 250 and 175 < y < 225:  return 35
        elif 250 < x < 350 and 175 < y < 225:  return 45
        elif 350 < x < 450 and 175 < y < 225:  return 58
        elif 450 < x < 550 and 175 < y < 225:  return 65
        elif 550 < x < 650 and 175 < y < 225:  return 78
        elif 650 < x < 750 and 175 < y < 225:  return 87
        elif 750 < x < 850 and 175 < y < 225:  return 93
        elif 850 < x < 950 and 175 < y < 225:  return 100
        elif 950 < x < 1050 and 175 < y < 225: return 108
        #############################
        elif 0 < x < 50 and 225 < y < 250:      return 15
        elif 50 < x < 150 and 225 < y < 250:    return 20
        elif 150 < x < 250 and 225 < y < 250:   return 28
        elif 250 < x < 350 and 225 < y < 250:   return 40
        elif 350 < x < 450 and 225 < y < 250:   return 54
        elif 450 < x < 550 and 225 < y < 250:   return 64
        elif 550 < x < 650 and 225 < y < 250:   return 73
        elif 650 < x < 750 and 225 < y < 250:   return 80
        elif 750 < x < 850 and 225 < y < 250:   return 88
        elif 850 < x < 950 and 225 < y < 250:   return 96
        elif 950 < x < 1050 and 225 < y < 250:  return 103
        elif 1050 < x < 1150 and 225 < y < 250: return 105
        #############################
        elif 50 < x < 150 and 251 < y < 279:   return 15
        elif 150 < x < 250 and 251 < y < 279:  return 25
        elif 250 < x < 350 and 251 < y < 279:  return 40
        elif 350 < x < 450 and 251 < y < 279:  return 53
        elif 450 < x < 550 and 251 < y < 279:  return 61
        elif 550 < x < 650 and 251 < y < 279:  return 69
        elif 650 < x < 750 and 251 < y < 279:  return 76
        elif 750 < x < 850 and 251 < y < 279:  return 86
        elif 850 < x < 950 and 251 < y < 279:  return 95
        elif 950 < x < 1050 and 251 < y < 279: return 103
        elif 950 < x < 1050 and 251 < y < 279: return 106
        #############################
        elif 50 < x < 150 and 280 < y < 330:    return 15
        elif 150 < x < 250 and 280 < y < 330:   return 25
        elif 250 < x < 350 and 280 < y < 330:   return 40
        elif 350 < x < 450 and 280 < y < 330:   return 54
        elif 450 < x < 550 and 280 < y < 330:   return 64
        elif 550 < x < 650 and 280 < y < 330:   return 80
        elif 650 < x < 750 and 280 < y < 330:   return 93
        elif 750 < x < 850 and 280 < y < 330:   return 109
        elif 850 < x < 950 and 280 < y < 330:   return 120
        elif 950 < x < 1050 and 280 < y < 330:  return 130
        elif 1050 < x < 1150 and 280 < y < 330: return 140
        #############################
        elif 50 < x < 150 and 331 < y < 380:    return 15
        elif 150 < x < 250 and 331 < y < 380:   return 27
        elif 250 < x < 350 and 331 < y < 380:   return 37
        elif 350 < x < 450 and 331 < y < 380:   return 48
        elif 450 < x < 550 and 331 < y < 380:   return 60
        elif 550 < x < 650 and 331 < y < 380:   return 73
        elif 650 < x < 750 and 331 < y < 380:   return 84
        elif 750 < x < 850 and 331 < y < 380:   return 97
        elif 850 < x < 950 and 331 < y < 380:   return 113
        elif 950 < x < 1050 and 331 < y < 380:  return 125
        elif 1050 < x < 1150 and 331 < y < 380: return 137
        #############################
        elif 50 < x < 150 and 381 < y < 430:    return 15
        elif 150 < x < 250 and 381 < y < 430:   return 25
        elif 250 < x < 350 and 381 < y < 430:   return 35
        elif 350 < x < 450 and 381 < y < 430:   return 47
        elif 450 < x < 550 and 381 < y < 430:   return 57
        elif 550 < x < 650 and 381 < y < 430:   return 69
        elif 650 < x < 750 and 381 < y < 430:   return 81
        elif 750 < x < 850 and 381 < y < 430:   return 93
        elif 850 < x < 950 and 381 < y < 430:   return 105
        elif 950 < x < 1050 and 381 < y < 430:  return 117
        elif 1050 < x < 1150 and 381 < y < 430: return 130
        #############################
        elif 50 < x < 150 and 431 < y < 480:    return 15
        elif 150 < x < 250 and 431 < y < 480:   return 23
        elif 250 < x < 350 and 431 < y < 480:   return 35
        elif 350 < x < 450 and 431 < y < 480:   return 42
        elif 450 < x < 550 and 431 < y < 480:   return 54
        elif 550 < x < 650 and 431 < y < 480:   return 65
        elif 650 < x < 750 and 431 < y < 480:   return 75
        elif 750 < x < 850 and 431 < y < 480:   return 85
        elif 850 < x < 950 and 431 < y < 480:   return 97
        elif 950 < x < 1050 and 431 < y < 480:  return 109
        elif 1050 < x < 1150 and 431 < y < 480: return 119
        #############################
        elif 50 < x < 150 and 481 < y < 530:    return 15
        elif 150 < x < 250 and 481 < y < 530:   return 21
        elif 250 < x < 350 and 481 < y < 530:   return 32
        elif 350 < x < 450 and 481 < y < 530:   return 41
        elif 450 < x < 550 and 481 < y < 530:   return 51
        elif 550 < x < 650 and 481 < y < 530:   return 62
        elif 650 < x < 750 and 481 < y < 530:   return 70
        elif 750 < x < 850 and 481 < y < 530:   return 80
        elif 850 < x < 950 and 481 < y < 530:   return 93
        elif 950 < x < 1050 and 481 < y < 530:  return 105
        elif 1050 < x < 1150 and 481 < y < 530: return 116
        ############################
        elif 50 < x < 150 and 531 < y < 580:   return 13
        elif 150 < x < 250 and 531 < y < 580:  return 22
        elif 250 < x < 350 and 531 < y < 580:  return 33
        elif 350 < x < 450 and 531 < y < 580:  return 44
        elif 450 < x < 550 and 531 < y < 580:  return 63
        elif 550 < x < 650 and 531 < y < 580:  return 75
        elif 650 < x < 750 and 531 < y < 580:  return 96
        elif 750 < x < 850 and 531 < y < 580:  return 108
        elif 850 < x < 950 and 531 < y < 580:  return 127
        elif 950 < x < 1150 and 531 < y < 580: return 145
        #############################
        elif 50 < x < 150 and 581 < y < 630:   return 15
        elif 150 < x < 250 and 581 < y < 630:  return 22
        elif 250 < x < 350 and 581 < y < 630:  return 33
        elif 350 < x < 450 and 581 < y < 630:  return 46
        elif 450 < x < 550 and 581 < y < 630:  return 58
        elif 550 < x < 650 and 581 < y < 630:  return 73
        elif 650 < x < 750 and 581 < y < 630:  return 94
        elif 750 < x < 850 and 581 < y < 630:  return 106
        elif 850 < x < 950 and 581 < y < 630:  return 127
        elif 950 < x < 1150 and 581 < y < 630: return 145
        #############################
        elif 50 < x < 150 and 631 < y < 680:   return 15
        elif 150 < x < 250 and 631 < y < 680:  return 23
        elif 250 < x < 350 and 631 < y < 680:  return 31
        elif 350 < x < 450 and 631 < y < 680:  return 46
        elif 450 < x < 550 and 631 < y < 680:  return 57
        elif 550 < x < 650 and 631 < y < 680:  return 67
        elif 650 < x < 750 and 631 < y < 680:  return 84
        elif 750 < x < 850 and 631 < y < 680:  return 95
        elif 850 < x < 950 and 631 < y < 680:  return 114
        elif 950 < x < 1150 and 631 < y < 680: return 124
        else: return 34


class Ball(pg.sprite.Sprite):
    def __init__(self, angle):

        pg.sprite.Sprite.__init__(self)
        self.v0 = vec(0, 0)
        self.a = vec(0.0, 10)
        self.v = vec(0, 0)
        self.angle = angle
        self.pos = vec(spawnBallX, spawnBallY)  # initial position
        self.cpt = 0  # A sort of timer
        self.AnimCount = 0  # for the explosion animation

        self.image = pg.image.load(ballAnim[self.AnimCount])
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(width=25, height=25)
        self.rect.center = (spawnBallX, spawnBallY)
        self.pos_collision = (0, 0)


    def update(self):
        # update trajectory of the ball
        if self.AnimCount < 1:
            self.cpt += 0.2

            # We update the ball's velocity with respect to the time (in this case, the time is self.cpt)

            self.v = vec(self.a.x * self.cpt, self.a.y * self.cpt)
            # We update the ball's position using the velocity at a given instant

            self.rect.center = (self.pos.x + (self.v0.x * self.cpt) + (self.a.x * self.cpt * self.cpt) / 2,
                                self.pos.y + (self.v0.y * self.cpt) + (self.a.y * self.cpt * self.cpt) / 2)
            self.pos_collision = self.rect.center

        else:
            # happens when the ball touches something and provokes an explosion

            self.AnimCount += 1
            self.image = pg.image.load(ballAnim[self.AnimCount])
            self.image = pg.transform.scale(self.image, (100, 100))
            self.rect = self.image.get_rect(width=100, height=100)
            self.rect.center = self.pos_collision