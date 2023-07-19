import pygame as pg
import random
import time
from options import *
from pygame.sprite import Group
from pygame import mixer
from sprites import *
import sys
from math import cos, sin, radians



# class for the game
class Game:
    def __init__(self):
        # Initialize of the game
        pg.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()
        pg.init()
        self.intTime = time.time()

        # Characteristics of the background
        self.bg = pg.image.load(bg)
        self.bg = pg.transform.scale(self.bg, (1200, 800))
        self.bg2 = pg.image.load(bg2)
        self.bg2 = pg.transform.scale(self.bg2, (1200, 800))

        self.rectBg = self.bg.get_rect()
        self.rectBg2 = self.bg2.get_rect()

        self.font_name = pg.font.match_font(FONT_NAME)
        self.moon = pg.image.load(moon)
        self.moon = pg.transform.scale(self.moon, (75, 75))
        self.rectMoon = self.moon.get_rect()
        self.rectMoon.center = (200, 50)

        # Our logo
        self.logo = pg.image.load(logo)
        self.logo = pg.transform.scale(self.logo, (290, int(290/2)))
        self.rectLogo = self.logo.get_rect()
        self.rectLogo.center = (WIDTH/2-10, HEIGHT/2-75)

        # Team DATA
        self.teamLogo = pg.image.load(team_logo)
        self.teamLogo = pg.transform.scale(self.teamLogo, (250, 100))
        self.rectTeamLogo = self.teamLogo.get_rect()
        self.rectTeamLogo.center = (1000, 100)

        # The exit
        self.exit = pg.image.load(exit_close)
        self.exit = pg.transform.scale(self.exit, (45, 75))
        self.rectExit = self.exit.get_rect()
        self.rectExit.center = (1175, 75)
        self.escape = False

        # Some boolean
        self.playing = True
        self.GameInProcess = True
        self.waitingMenu = False
        self.waitingPause = False
        self.finished = False
        self.rules = False
        self.menu = True

        # The level
        self.lvl = 1
        self.current_time = 0
        self.time_paused = 0
        self.time = 0

        # Start a new Game
        self.score = 0

        # Window parameters
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

        # A rectangle for the pause menu
        self.rectPause = pg.Surface(self.screen.get_size())
        self.rectPause.set_alpha(160)
        self.rectPause.fill(WHITE)

        # A rectangle for the wining menu
        self.rectWin = pg.Surface(self.screen.get_size())
        self.rectWin.set_alpha(130)
        self.rectWin.fill(BLACK)

        # Initialization of the clock for the FPS
        self.clock = pg.time.Clock()
        self.player = Player(Game)

        # The canon
        self.baseCanon = BaseCanon()
        self.canon = Canon()

        self.spawnBallX, self.spawnBallY = 0, 0

        # Player's head for the health
        self.ninjaHead = pg.image.load(NinjaHead)
        self.ninjaHead = pg.transform.scale(self.ninjaHead, (35, 35))
        self.HeadRect = self.ninjaHead.get_rect()
        self.HeadRect.center = (HealthX-50, HealthY+15)

        self.plat = Platform(dirtImg, 140, 284)

        self.current_tile = (50, 50, 0, 0)

    def drawGrid(self):
        for line in range(0, 24):
            pg.draw.line(self.screen, BLACK, (0, line * tileSize), (WIDTH, line * tileSize))
            pg.draw.line(self.screen, BLACK, (line * tileSize, 0), (line * tileSize, HEIGHT))

    def new(self):  # Initializations of groups and levels

        # Put all my sprites in a GROUP
        self.allSprites = pg.sprite.Group()
        self.allPlatforms = pg.sprite.Group()
        self.allShurikens = pg.sprite.Group()
        self.allZombies = pg.sprite.Group()
        self.allBall = pg.sprite.Group()
        self.allBirds = pg.sprite.Group()

        # A variable that represent the player himself
        self.player = Player(self)

        # Add the player in all the Sprites of the game (all the graphical things)
        self.allSprites.add(self.player)

        # Add the canon
        self.allSprites.add(self.canon)

        # Add the base
        self.allSprites.add(self.baseCanon)

        row_count, col_count = 0, 0

        # creating levels
        if self.lvl == 1:
            row_count = 0
            for row in lvl1:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 2:
            for row in lvl1:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl2:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 3:
            for row in lvl2:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl3:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 4:
            for row in lvl3:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl4:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 5:
            for row in lvl4:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl5:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 6:
            for row in lvl5:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl6:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 7:
            for row in lvl6:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl7:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 8:
            for row in lvl7:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl8:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 9:
            for row in lvl8:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl9:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 10:
            for row in lvl9:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl10:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 11:
            for row in lvl10:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl11:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 12:
            for row in lvl11:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl12:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 13:
            for row in lvl12:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl13:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 14:
            for row in lvl13:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl14:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

        elif self.lvl == 15:
            for row in lvl14:
                for col in row:
                    self.allPlatforms.remove(self.plat)
                    self.allSprites.remove(self.plat)

            row_count = 0
            for row in lvl15:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        self.plat = Platform(dirtImg, row_count, col_count)

                    elif tile == 2:
                        self.plat = Platform(grassImg, row_count, col_count)

                    elif tile == 3:
                        self.plat = Platform(lavaImg, row_count, col_count)
                    self.allPlatforms.add(self.plat)
                    self.allSprites.add(self.plat)

                    col_count += 1
                row_count += 1

    # Main loop function that calls other functions in Game and defines the FPS
    def main_loop(self):
        # Game loop
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.waitingPause:
                self.update()
            self.draw()

    # An update function to see if the player collides with a platform
    def update(self):

        if self.lvl == 16 :
            self.playing = not self.playing
            self.finished = not self.finished
            self.finished_game()

        # Just to have the key button in pygame
        keys = pg.key.get_pressed()

        # Game loop - Update
        self.allSprites.update()

        ############################################# ALL THE COLLISIONS #############################################

        player_door = self.player.rect.colliderect(self.rectExit)

        if player_door and self.escape:
            self.intTime = time.time()
            self.lvl += 1
            self.score += 500      # Increase the score
            self.playing = False
            self.new_level()

        for bird in self.allBirds:
            for shuriken in self.allShurikens:
                shuriken_bird = shuriken.rect.colliderect(bird.rect)
                if shuriken_bird:
                    bird.health -= 20
                    self.allSprites.remove(shuriken)
                    self.allShurikens.remove(shuriken)

            if bird.health < 1:
                self.allSprites.remove(bird)
                self.allBirds.remove(bird)
                self.score += 20     # Increase the score

            bird_player = self.player.rect.colliderect(bird.rect)
            if bird_player:
                bird.image = pg.image.load(BIRD_STANDING[bird.direction])
                bird.image = pg.transform.scale(bird.image, (50, 48))
                bird.stop = 0
                self.player.health -= BIRD_DAMAGE
            else:
                bird.stop = 1
                bird.image = pg.transform.scale(bird.image, (50, 48))

        for proj in self.allShurikens:
            for zombie in self.allZombies:
                shuriken_monster = proj.rect.colliderect(zombie)  # collisions between monsters and the shurikens
                if shuriken_monster:
                    zombie.health -= 20
                    if zombie.health < 1:
                        self.allSprites.remove(zombie)
                        self.allZombies.remove(zombie)  # delete the zombies
                        self.score += 10     # Increase the score
                    proj.remove(self.allShurikens)
                    proj.remove(self.allSprites)

            if proj.rect.x > WIDTH or proj.rect.x < 0:  # If shuriken touch the limits of the screen
                self.allShurikens.remove(proj)
                self.allSprites.remove(proj)

        for plat in self.allPlatforms:
            for ball in self.allBall:
                ball_platform = plat.rect.colliderect(ball.rect)  # Collision between the balls and the platforms

                if ball_platform:
                    ball.AnimCount += 1

                if ball.AnimCount > len(ballAnim) - 3:
                    self.allBall.remove(ball)
                    self.allSprites.remove(ball)

        for ball in self.allBall:
            player_ball = self.player.rect.colliderect(ball.rect)  # Collision between the balls and the player
            if player_ball:
                ball.AnimCount += 1
                self.player.health -= BALL_DAMAGE

            if ball.AnimCount > len(ballAnim) - 3:
                self.allBall.remove(ball)
                self.allSprites.remove(ball)

        for proj in self.allShurikens:
            for plat in self.allPlatforms:
                shuriken_platform = proj.rect.colliderect(plat)  # Collision between the shurikens and the platforms
                if shuriken_platform:
                    proj.remove(self.allShurikens)
                    proj.remove(self.allSprites)

        for zombie in self.allZombies:
            if zombie.velocity.y > -5:

                for platform in self.allPlatforms:

                    # A variable that check collisions between the player and the platforms (initialize as False)
                    monster_plat = zombie.rect.colliderect(platform.rect)
                    if monster_plat:

                        if zombie.position.y < platform.rect.bottom:
                            zombie.position.y = platform.rect.top
                            zombie.velocity.y = 0

        if self.player.velocity.y < 0:
            for plat in self.allPlatforms:
                player_platform = self.player.rect.colliderect(plat.rect)
                if player_platform and self.player.rect.midtop[1] < plat.rect.midbottom[1] and plat.img != lavaImg:
                    self.player.velocity.y = PlayerSpeed

        elif self.player.velocity.y > 0:
            # A variable that check collisions between the player and the platforms (initialize as False)
            for plat in self.allPlatforms:
                if plat.img == lavaImg:
                    player_lava = self.player.rect.colliderect(plat)
                    if player_lava:
                        self.player.health -= LAVA_DAMAGE

                elif plat.img == grassImg or plat.img == dirtImg:
                    player_grass = self.player.rect.colliderect(plat)
                    if player_grass and self.player.position.y > plat.rect.top:
                        self.player.isJumping = False
                        if self.player.position.y < plat.rect.bottom:
                            self.player.position.y = plat.rect.top
                            self.player.velocity.y = 0

        # Check if the player goes belows of the map

        if self.player.rect.y > 690:
            self.player.health = 0
            self.lvl = 1

        # Analysis of a collision between the player and a wall

        for plat in self.allPlatforms:
            val = 75
            tile = (plat.rect.x - 20, plat.rect.y, val + 20, plat.rect.height)
            player_tile = self.player.rect.colliderect(tile)
            if player_tile and plat.rect.y < self.player.rect.centery < plat.rect.bottom:
                self.current_tile = plat

                if self.player.rect.right < plat.rect.left:
                    self.player.right = False
                    self.player.velocity.x *= 0
                    self.player.acceleration.x = -0.7
                    self.player.collides = True

                    if keys[pg.K_UP]:
                        self.player.acceleration.x = 0
                        self.player.velocity.x = 0

                        if keys[pg.K_RIGHT]:
                            self.player.right = False

                    if keys[pg.K_LEFT]:

                        self.player.moves = True
                        self.player.collides = False
                        self.player.right = False

                elif self.player.rect.left > plat.rect.right:
                    self.player.left = False
                    self.player.velocity.x *= 0
                    self.player.acceleration.x = -0.7
                    self.player.collides = True

                    if keys[pg.K_UP]:
                        self.player.acceleration.x = 0
                        self.player.velocity.x = 0

                    if keys[pg.K_RIGHT]:

                        self.player.collides = False
                        self.player.left = False
                        self.player.moves = True

            else:
                self.player.moves = False

        # Function for the animation of the player

        self.player.walk_anim()

        # For the animation of the zombies and their behaviour
        for zombie in self.allZombies:
            player_monster = zombie.rect.colliderect(self.player.rect)
            if player_monster:
                self.player.health -= ZOMBIE_DAMAGE
                zombie.image = pg.image.load(ZOMBIE_STANDING[zombie.direction])
                zombie.stop = 0
            else:
                zombie.stop = 1

            zombie.walk_anim()

            if self.player.rect.y - 30 < zombie.rect.y < self.player.rect.y + 30:
                # Detect position of the player with respect to the zombie

                if self.player.rect < zombie.rect:
                    zombie.target = -1
                elif self.player.rect > zombie.rect:
                    zombie.target = 1
                else:
                    if zombie.target == -1:
                        zombie.walkCount = -2
                    else:
                        zombie.walkCount = -1
                    zombie.target = 0

            else:
                zombie.image = pg.image.load(ZOMBIE_STANDING[zombie.direction])
                zombie.image = pg.transform.scale(zombie.image, (PlayerHeight + 8, PlayerWidth))
                zombie.stop = 0

        for bird in self.allBirds:
            # For the animation of the birds and their behaviour

            bird.walk_anim()

            if self.player.rect < bird.rect:  # PLAYER     BIRD
                bird.target = -1
            elif self.player.rect > bird.rect:  # BIRD     PLAYER
                bird.target = 1
            else:
                if bird.target == -1:
                    bird.walkCount = -2
                else:
                    bird.walkCount = -1
                bird.target = 0

        # Check if the player shoots and if the number of projectile allowed is not higher

        if self.player.shoots and len(self.allShurikens) < PlayerShootLimit and not self.player.spamButton:
            shuriken = Projectile(self.player.shurikenCoordinates[0], self.player.shurikenCoordinates[1], self.player.side)
            self.allSprites.add(shuriken)
            self.allShurikens.add(shuriken)
            self.player.shoots = False

        if self.lvl == 16:
            if len(self.allZombies) < 3:  # 14 is the number of zombies on the screen, you can increase it or decrease it if you want
                zombie = Zombie(0)
                self.allSprites.add(zombie)
                self.allZombies.add(zombie)

            if len(self.allBirds) < 3:   # 6 is the number of birds on the screen, you can increase it or decrease it if you want
                bird = Bird(0, self)
                self.allSprites.add(bird)
                self.allBirds.add(bird)
        else:
            if len(self.allZombies) < 3:  # 8 is the number of zombies on the screen, you can increase it or decrease it if you want
                zombie = Zombie(0)
                self.allSprites.add(zombie)
                self.allZombies.add(zombie)

            if len(self.allBirds) < 3:  # 3 is the number of birds on the screen, you can increase it or decrease it if you want
                bird = Bird(0, self)
                self.allSprites.add(bird)
                self.allBirds.add(bird)

        self.canon.image = self.canon.rotation(pg.image.load(CanonImg), self.canon.angle)  # rotation of the canon
        self.canon.image = pg.transform.scale(self.canon.image, (40, 40))

        # Analyze the position of the player to rotate the canon
        if 50 < self.player.rect.y < HEIGHT/3:
            self.canon.angle = 20
            self.spawnBallX = posCanonX + 20
            self.spawnBallY = posCanonY
        elif HEIGHT / 3 < self.player.rect.y < 2 * HEIGHT/3:
            self.canon.angle = 0
            self.spawnBallX = posCanonX + 20
            self.spawnBallY = posCanonY - 10
        elif 2 * HEIGHT / 3 < self.player.rect.y < HEIGHT-100:
            self.canon.angle = -20
            self.spawnBallX = posCanonX
            self.spawnBallY = posCanonY - 20

        # Analyze the position of the player
        self.canon.velocity = self.canon.power(self.player.rect.centerx, self.player.rect.centery)

        if not self.canon.launched and 0 < float(time.time() - self.intTime) % 2 < 0.05:  # Shoots a ball every 3 seconds
            # create a new ball

            ball = Ball(self.canon.angle)
            # initial velocity of the ball

            ball.v0 = vec(self.canon.velocity * cos(radians(self.canon.angle)), -self.canon.velocity * sin(radians(self.canon.angle)))
            self.allBall.add(ball)
            self.allSprites.add(ball)

        if self.player.rect.x > WIDTH - 150 and self.player.rect.y < 50:  # Check if the player is next to the door
            self.exit = pg.image.load(exit_open)
            self.exit = pg.transform.scale(self.exit, (45, 75))
            self.escape = True
        else:
            self.exit = pg.image.load(exit_close)
            self.exit = pg.transform.scale(self.exit, (45, 75))
            self.escape = False

        # Update health of player
        if self.player.health < 1 or self.player.position.y > 810 or self.player.position.x > WIDTH:  # Check if he dies
            self.playing = False
            self.menu = True
            self.lvl = 1
            die_theme_fx.play()
            time.sleep(1)

    # Function check some buttons pressed by the player

    def events(self):

        # Game loop - Events

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if not self.waitingPause:
                    if event.key == pg.K_UP:
                        self.player.isJumping = True
                        self.player.jump()
                    elif event.key == pg.K_SPACE:
                        self.player.spamButton = True

                if event.key == pg.K_p:
                    self.waitingPause = not self.waitingPause

                    if self.waitingPause:
                        self.waitPause()
                    else:
                        self.playing = True

            if event.type == pg.KEYUP:
                self.player.spamButton = False

    def drawText(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    # Function that display all the Sprites on the screen
    def draw(self):
        # Game loop - Draw (display everything on the screen)

        self.screen.blit(self.bg, self.rectBg)
        self.screen.blit(self.moon, self.rectMoon)
        self.screen.blit(self.exit, self.rectExit)
        self.allSprites.draw(self.screen)
        self.player.UpdateHealthBar(self.screen)

        for monster in self.allZombies:
            monster.UpdateHealthBar(self.screen)  # update the health bar of the monster

        for bird in self.allBirds:
            bird.UpdateHealthBar(self.screen)  # update the health bar of the bird
        self.screen.blit(self.ninjaHead, self.HeadRect)
        self.drawText("Score: "+str(self.score), 30, GREEN, 8*50, 35)
        self.drawText("HP", 30, GREEN, HealthX + 550, HealthY + 15)
        self.drawText("Level " + str(self.lvl), 30, BLACK, 13*50, 35)
        pg.display.flip()

    # Display the menu
    def menuScreen(self):
        if self.menu:
            self.screen.blit(self.bg2, self.rectBg2)

            self.screen.blit(self.logo, self.rectLogo)
            self.drawText("Right key to go right - Left key to go left - Up key to jump - Space to shoot", 30, BLACK, WIDTH/2, HEIGHT/2 + 100)
            self.drawText("Press 'P' to start ! - Press 'R' to see the rules ! - Press 'Q' to quit !", 35, ORANGE, WIDTH/2, HEIGHT/2 + 200)
            self.drawText("Press 'C' to see the credits !", 28, ORANGE, WIDTH / 2, HEIGHT / 2 + 240)
            pg.display.flip()
        self.waitMenu()

    # Display the credits
    def credits(self, numb):
        if numb == 0:
            self.screen.blit(self.bg, self.rectBg)
            self.screen.blit(self.teamLogo, self.rectTeamLogo)
            self.drawText("By WELLINGTON James / LIN Jefferson / SOTAK Maxime / KEGREISZ Clément / LECOMTE Solène", 25, GREEN, WIDTH/2, HEIGHT/2-200)
            self.drawText("Music made by Fantasy & World Music by the Fiechters", 35, BLACK, WIDTH/2, HEIGHT/2-100)
            self.drawText("Design of the birds : from the game 'Flappy Bird'", 35, BLACK, WIDTH/2, HEIGHT/2)
            self.drawText("Sound effects : https://freesound.org/", 35, BLACK, WIDTH/2, HEIGHT/2 + 100)
            self.drawText("Press 'P' to start ! / Press 'R' to see the rules ! / Press 'Q' to quit the game !", 25, ORANGE, WIDTH / 2, HEIGHT / 2 + 200)
        else:
            self.screen.blit(self.bg, self.rectBg)
            self.screen.blit(self.teamLogo, self.rectTeamLogo)
            self.drawText("By WELLINGTON James / LIN Jefferson / SOTAK Maxime / KEGREISZ Clément / LECOMTE Solène", 25, GREEN, WIDTH / 2, HEIGHT / 2 - 200)
            self.drawText("Music made by Fantasy & World Music by the Fiechters", 35, BLACK, WIDTH / 2, HEIGHT / 2-100)
            self.drawText("Design of the birds : from the game 'Flappy Bird'", 35, BLACK, WIDTH / 2, HEIGHT / 2)
            self.drawText("Sound effects : https://freesound.org/", 35, BLACK, WIDTH / 2, HEIGHT / 2 + 100)
            self.drawText("Press 'P' to restart ! / Press 'Q' to quit to menu", 25, ORANGE, WIDTH / 2, HEIGHT/2 + 200)
        pg.display.flip()

    # Display the game over screen
    def gameOver(self):
        self.screen.blit(self.bg2, self.rectBg2)

        self.screen.blit(pg.transform.scale(self.logo, (290, int(290/2))), self.rectLogo)
        if self.score <= 1000:
            text = BAD_GAME_OVER[random.randint(0, 5)]
        elif 1000 < self.score < 2000:
            text = GOOD_GAME_OVER[4]
        else:
            text = GOOD_GAME_OVER[random.randint(0, 3)]

        self.drawText(text, 32, WHITE, WIDTH / 2, HEIGHT / 2 + 80)
        if self.score > self.highScore():
            self.updateScore(self.score)
            self.drawText("New high score: " + str(self.score), 45, GREEN, WIDTH / 2, HEIGHT / 2 + 120)
        else:
            self.updateScore(self.score)
            self.drawText("Score: " + str(self.score), 45, GREEN, WIDTH / 2, HEIGHT / 2 + 130)
        self.drawText("High score : " + str(self.highScore()), 25, ORANGE, WIDTH / 2, HEIGHT / 2 + 170)
        self.drawText("Press 'P' to restart ! / Press 'R' to see the rules !", 24, ORANGE, WIDTH / 2, HEIGHT / 2 + 210)
        self.drawText("Right key to go right / Left key to go left / Up key to jump / Space to shoot", 17, BLACK, WIDTH / 2, HEIGHT / 2 + 240)
        pg.display.flip()
        self.waitMenu()
        self.score = 0

    # Display the new level screen
    def new_level(self):
        self.screen.blit(self.bg2, self.rectBg2)
        self.screen.blit(pg.transform.scale(self.logo, (290, int(290/2))), self.rectLogo)
        self.drawText("You reached level "+str(self.lvl)+" !", 34, GREEN, WIDTH / 2, HEIGHT / 2 + 90)
        self.drawText("Press 'P' to continue ! / Press 'R' to see the rules !", 24, ORANGE, WIDTH / 2, HEIGHT / 2 + 170)
        self.drawText("Right key to go right / Left key to go left - Up key to jump / Space to shoot", 17, BLUE, WIDTH / 2, HEIGHT / 2 + 220)
        pg.display.flip()
        self.waitMenu()

    # Display the winning screen
    def finished_game(self):
        play_theme_fx.stop()
        self.finished = True
        self.screen.blit(self.bg, self.rectBg)
        self.screen.blit(self.rectWin, (0, 0))
        self.screen.blit(pg.transform.scale(self.logo, (290, int(290/2))), self.rectLogo)
        self.drawText("Congratulations ! You found the sword of immortality !", 45, GREEN, WIDTH / 2, HEIGHT / 2 - 200)
        self.rectSword.center = (WIDTH / 2, HEIGHT / 2 + 180)
        self.drawText("Press 'P' to restart ! / Press 'Q' to quit to menu / 'Press 'C' to see the credits", 25, ORANGE, WIDTH/2, HEIGHT/2)
        self.screen.blit(self.sword, self.rectSword)
        wining_theme_fx.play(loops=-1)
        cpt = 0
        while self.finished:
            self.screen.blit(self.bg, self.rectBg)
            self.screen.blit(self.rectWin, (0, 0))
            self.screen.blit(pg.transform.scale(self.logo, (290, int(290 / 2))), self.rectLogo)
            self.sword = pg.image.load(KATANA[cpt % 30])
            self.sword = pg.transform.scale(self.sword, (400, 400))
            self.screen.blit(self.sword, self.rectSword)

            self.drawText("Congratulations ! You found the sword of immortality !", 45, GREEN, WIDTH / 2, HEIGHT / 2 - 200)
            self.rectSword.center = (WIDTH / 2, HEIGHT / 2 + 180)
            self.drawText("Press 'P' to restart ! / Press 'Q' to quit to menu / 'Press 'C' to see the credits", 25, ORANGE, WIDTH / 2, HEIGHT/2)
            cpt += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        wining_theme_fx.stop()
                        play_theme_fx.play(loops=-1)
                        self.lvl = 1
                        self.new()
                        self.score = 0
                        self.finished = False

                    elif event.key == pg.K_r:
                        self.display_rules(0)

                    elif event.key == pg.K_q:
                        wining_theme_fx.stop()
                        menu_theme_fx.play(loops=-1)
                        self.lvl = 1
                        self.menu = True
                        self.finished = False
                        self.menuScreen()

                    elif event.key == pg.K_c:
                        self.credits(1)

            pg.display.flip()

    # Display the rules
    def display_rules(self, numb):
        if numb == 0:
            self.screen.blit(self.bg2, self.rectBg2)
            self.screen.blit(self.teamLogo, self.rectTeamLogo)
            self.screen.blit(pg.transform.scale(self.logo, (290, int(290/2))), self.rectLogo)
            self.drawText("- To win you have to escape by the door.", 30, WHITE, WIDTH / 2, HEIGHT / 2 + 80)
            self.drawText("- When you shoot a zombie, it gives you 10 points.", 30, WHITE, WIDTH / 2, HEIGHT / 2 + 130)
            self.drawText("- When you shoot a bird, it gives 20 points.", 30, WHITE, WIDTH / 2, HEIGHT / 2 + 180)
            self.drawText("- It is forbidden to go outside the map or screen, we warned you !", 30, RED, WIDTH / 2, HEIGHT / 2 + 230)
            self.drawText("- Lava kills !", 30, RED, WIDTH / 2, HEIGHT / 2 + 280)
            self.drawText("Press 'P' if you want to start ! / Press 'Q' to quit the game ! / Press C to see the credits !", 20, ORANGE, WIDTH / 2, HEIGHT / 2 + 330)
        else:
            self.screen.blit(self.bg2, self.rectBg2)
            self.screen.blit(self.teamLogo, self.rectTeamLogo)
            self.screen.blit(pg.transform.scale(self.logo, (290, int(290 / 2))), self.rectLogo)
            self.drawText("- To win you have to escape by the door.", 30, WHITE, WIDTH / 2, HEIGHT / 2 + 80)
            self.drawText("- When you shoot a zombie, it gives you 10 points.", 30, WHITE, WIDTH / 2, HEIGHT / 2 + 130)
            self.drawText("- When you shoot a bird, it gives 20 points.", 30, WHITE, WIDTH / 2, HEIGHT / 2 + 180)
            self.drawText("- It is forbidden to go outside the map or screen, we warned you !", 30, RED, WIDTH / 2, HEIGHT / 2 + 230)
            self.drawText("- Lava kills !", 30, RED, WIDTH / 2, HEIGHT / 2 + 280)
            self.drawText("Press 'C' if you want to continue / Press 'S' to restart / Press 'Q' to quit the game", 20, ORANGE, WIDTH / 2, HEIGHT / 2 + 330)

        pg.display.flip()

    # Display the wait menu
    def waitMenu(self):
        self.waitingMenu = True
        play_theme_fx.stop()
        if not self.finished:
            menu_theme_fx.play(loops=-1)
        self.screen.blit(self.teamLogo, self.rectTeamLogo)
        while self.waitingMenu:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.display_rules(0)

                    if event.key == pg.K_q:
                        sys.exit()

                    elif event.key == pg.K_p:
                        self.waitingMenu = not self.waitingMenu
                        menu_theme_fx.stop()
                        play_theme_fx.play(loops=-1)
                        self.intTime = time.time()
                        self.new()

                    elif event.key == pg.K_c:
                        self.credits(0)

            pg.display.flip()

    # Display the wait pause
    def waitPause(self):
        self.waitingPause = True
        play_theme_fx.stop()
        menu_theme_fx.play(loops=-1)
        self.screen.blit(self.rectPause, (0, 0))
        self.screen.blit(self.teamLogo, self.rectTeamLogo)
        self.drawText("PAUSED", 45, RED, WIDTH / 2, (HEIGHT / 2)-20)
        self.drawText("Press 'C' to continue / Press 'S' to restart / Press 'R' to see the rules !", 28, BLACK, WIDTH/2, (HEIGHT/2) + 20)
        while self.waitingPause:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        menu_theme_fx.stop()
                        play_theme_fx.play(loops=-1)
                        self.lvl = 1
                        self.new()
                        self.score = 0
                        self.waitingPause = False

                    elif event.key == pg.K_r:
                        self.display_rules(1)

                    elif event.key == pg.K_q:
                        menu_theme_fx.stop()
                        self.lvl = 1
                        self.menu = True
                        self.waitingPause = False
                        self.menuScreen()

                    elif event.key == pg.K_c:
                        self.waitingPause = False
                        play_theme_fx.play(loops=-1)
            pg.display.flip()

        menu_theme_fx.stop()

    # Function that returns the highest score
    def highScore(self):
        with open("All_graphism_sounds/score.txt", "r") as file:
            line = file.readline()
        try:
            result = int(str.rstrip(line))
        except ValueError:
            result = 0
        return result

    # Function that update the score
    def updateScore(self, New_value):
        Score = [New_value]

        # Create a list
        with open("All_graphism_sounds/score.txt", "r") as file:
            for line in file:
                Score.append(int(line))

        for i in range(len(Score) - 1):
            for j in range(len(Score)-i):
                if Score[i] < Score[j+i]:
                    wait = Score[j+i]
                    Score[j+i] = Score[i]
                    Score[i] = wait

        # Rewriting file in ascending score order
        with open("All_graphism_sounds/score.txt", "w") as file:
            for i in range(len(Score) - 1):
                file.write(str(Score[i]))
                file.write("\n")

G = Game()
G.menuScreen()
while G.GameInProcess:
    G.new()
    G.main_loop()
    if G.player.health < 1:
        G.gameOver()
pg.quit()