'''
Created on Mar 7, 2010

@author: kmott071
'''

import sys, pygame, time, enemy, player, bullet, random

class Game:
    
    def __init__(self):
        pygame.init()
        
        ''' we don't use a mouse in this game so we hide it '''
        pygame.mouse.set_visible(False)

        self.size = self.width, self.height = (1024, 768)
        self.black = 0, 0, 0
        self.fontColor = (255,255,255)
        
        self.gameStarted = False
        self.gameOver = False

        ''' set the display size and put it in fullscreen mode '''
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        
        ''' the font for the score board '''
        fontPath = pygame.font.match_font("Arial", True, False)
        self.scoreFont = pygame.font.Font(fontPath, 30)
        
        ''' the font for the hit space to start '''
        self.titleFont = pygame.font.Font(fontPath, 120)
        self.spaceToStartFont = pygame.font.Font(fontPath, 40)
        
        ''' the font for game over '''
        self.gameOverFont = pygame.font.Font(fontPath, 120)
        self.gameOverScoreFont = pygame.font.Font(fontPath, 60)
        self.gameOverSpaceForMainMenu = pygame.font.Font(fontPath, 40)      
        
        ''' load the images '''
        self.background = pygame.image.load("pictures/3D_Hot_Planet.jpg")        
        self.playerImage = pygame.image.load("pictures/player_ship_resized.png")
        self.alienUFOskin = pygame.image.load("pictures/ufo_resized.png")
        self.laser = pygame.image.load("pictures/laser.png")
        self.laserBall = pygame.image.load("pictures/laser_ball.png")
        self.fire = pygame.image.load("pictures/cartoon_fire_resized.png")
        self.afterburnSurface = pygame.image.load("pictures/afterburn.png")
        
        ''' the background's rectangle '''
        self.backgroundrect = self.background.get_rect()

        ''' the player's ship '''
        self.player = player.Player(self.playerImage)

        ''' Generate bullets '''
        self.playerreservebulletlist = []
        self.enemyreservebulletlist = []
        self.playeractivebulletlist = []
        self.enemyactivebulletlist = []
        
        ''' add bullets to the players reserve '''
        self.playerbulletskin = self.laser
        for _ in range(50):
            self.playerreservebulletlist.append(bullet.Bullet(self.playerbulletskin))
        
        ''' add bullets to the enemies reserve '''
        self.enemybulletskin = self.laserBall
        for _ in range(100):
            self.enemyreservebulletlist.append(bullet.Bullet(self.enemybulletskin))
        
        ''' Generate Enemies '''
        self.enemylist = []
        self.enemylist.append(enemy.Enemy(self.alienUFOskin, 10))
        self.enemylist.append(enemy.Enemy(self.alienUFOskin, 15))
        self.enemylist.append(enemy.Enemy(self.alienUFOskin, 12))
        
        ''' add the enemies to the list of enemies ''' 
        self.enemyrectlist = []
        for e in self.enemylist:
            self.enemyrectlist.append(e.rect)
        
        ''' add the enemies to the list of obstacles '''
        self.obstaclelist = []        
        for e in self.enemylist:
            self.obstaclelist.append(e)
        
        ''' create a list of the rectangles of the obstacles '''
        self.obstaclerectlist = []
        for o in self.obstaclelist:
            self.obstaclerectlist.append(o.rect)
        
        ''' load the sounds '''
        pygame.mixer.init()
        self.afterburnSound = pygame.mixer.Sound("sounds/afterburn.ogg")
        self.bigExplosionSound = pygame.mixer.Sound("sounds/big_explosion.ogg")
        self.explosionSound = pygame.mixer.Sound("sounds/explosion.ogg")
        self.gameOverSound = pygame.mixer.Sound("sounds/game_over.ogg")
        self.pewSound = pygame.mixer.Sound("sounds/pew.ogg")
        self.powSound = pygame.mixer.Sound("sounds/pow.ogg")
        self.tinkSound = pygame.mixer.Sound("sounds/tink.ogg")
        self.tuckSound = pygame.mixer.Sound("sounds/tink.ogg")

        ''' movement directions '''
        self.travelLeft = False
        self.travelRight = False
        self.travelUp = False
        self.travelDown = False
        
        ''' shooting '''
        self.shooting = False
        
        ''' afterburner '''
        self.afterburn = False
     
        
    def handleKeyDownEvent(self, event):
        ''' the arrow keys affect movement '''
        if event.key == pygame.K_UP:
            self.travelUp = True
        elif event.key == pygame.K_DOWN:
            self.travelDown = True
        elif event.key == pygame.K_LEFT:
            self.travelLeft = True
        elif event.key == pygame.K_RIGHT:
            self.travelRight = True
        elif event.key == pygame.K_SPACE:
            ''' the space key also starts the game '''
            if self.gameOver:
                self.gameOver = False
                self.__reset()                
            elif not self.gameStarted:
                self.gameStarted = True                
            else:
                self.shooting = True
        elif event.key == pygame.K_LALT:
            if not self.afterburn:
                self.afterburn = True
                self.playAfterburnSound()
            
    def handleKeyUpEvent(self, event):
        ''' the arrow keys affect movement ''' 
        if event.key == pygame.K_UP:
            self.travelUp = False
        elif event.key == pygame.K_DOWN:
            self.travelDown = False
        elif event.key == pygame.K_LEFT:
            self.travelLeft = False
        elif event.key == pygame.K_RIGHT:
            self.travelRight = False
        elif event.key == pygame.K_SPACE:
            self.shooting = False
        elif event.key == pygame.K_LALT:
            self.afterburn = False
       
            
    def update(self):
        ''' don't do anything if the game is not started '''
        if not self.gameStarted:
            return
        
        acceleration = 1
        if self.afterburn:
            acceleration = 3
               
        ''' adjust the speeds '''
        if self.travelLeft:
            self.player.xSpeed -= acceleration
        if self.travelRight:
            self.player.xSpeed += acceleration
        if self.travelUp:
            self.player.ySpeed -= acceleration
        if self.travelDown:
            self.player.ySpeed += acceleration
            
        ''' prevent the player from going off screen '''
        if self.player.rect.top + self.player.ySpeed < 0:
            self.player.ySpeed = 0
        if self.player.rect.bottom + self.player.ySpeed > self.height:
            self.player.ySpeed = 0
        if self.player.rect.left + self.player.xSpeed < 0:
            self.player.xSpeed = 0
        if self.player.rect.right + self.player.xSpeed > self.width:
            self.player.xSpeed = 0
  
        ''' move the player '''
        self.player.movement()
        
        ''' move all obstacles their respective speeds and paths '''
        for o in self.obstaclelist:
            o.movement()
            
        for b in self.playeractivebulletlist:
            b.movement()
            
        for b in self.enemyactivebulletlist:
            b.movement()
        
        ''' check for collisions '''
        if ((self.player.rect.collidelist(self.obstaclerectlist) != -1) or (self.player.rect.collidelist(self.enemyactivebulletlist) != -1)):
                ''' death code '''
                self.player.death()
                self.__doPlayerDeathAnimation()
                ''' the game is over, end the update '''
                return
        
        ''' check for colisions between enemies and our bullets '''
        bulletstoreserve = []
        for e in self.enemylist:
            for b in self.playeractivebulletlist:
                if (e.rect.colliderect(b.rect)):
                    ''' enemy death code '''
                    e.reset(self.width, self.height)
                    b.reset(self.width, self.height)
                    bulletstoreserve.append(b)                    
                    self.playExplosionSound()
                    self.player.score += 50
                
        ''' reset any obstaclelist that have gone by '''
        for o in self.obstaclelist:
            if o.rect.right < 0:
                o.reset(self.width, self.height)
        
        ''' move any bullets that are off screen to the reserve '''
        for b in self.playeractivebulletlist:
            if (b.rect.left > self.width):
                bulletstoreserve.append(b) 
                b.reset(self.width, self.height)
        
        ''' move the active bullets over to inactive '''
        for b in bulletstoreserve:
            self.playerreservebulletlist.append(b)
            self.playeractivebulletlist.remove(b)
        
        ''' move enemy bullets that are offscreen to the reserve list '''
        bulletstoreserve = []        
        for b in self.enemyactivebulletlist:
            if (b.rect.right < 0):
                bulletstoreserve.append(b)                
                b.reset(self.width, self.height)

        for b in bulletstoreserve:
            self.enemyreservebulletlist.append(b)
            self.enemyactivebulletlist.remove(b)
                
        ''' check if shooting '''
        if self.shooting:
            
            bullet = self.playerreservebulletlist.pop(0)
            self.playeractivebulletlist.append(bullet)
            bullet.rect.left = self.player.rect.right
            bullet.rect.top = self.player.rect.top + (self.player.rect.height / 2)
            bullet.xvelocity = 35
            self.playPewSound()
            self.shooting = False
            
        ''' make enemies fire '''
        for e in self.enemylist:
            shoot = random.randint(1, 50)
            if (shoot == 1):
                bullet = self.enemyreservebulletlist.pop(0)
                self.enemyactivebulletlist.append(bullet)
                bullet.rect.right = e.rect.left
                bullet.rect.top = e.rect.top + (e.rect.height / 2)
                bullet.xvelocity = -25
                bullet.yvelocity = random.randint(-10,10)
                self.playPowSound()
            
                
        ''' update the player score '''
        self.player.score += 1
        
        
    def draw(self):
        ''' draw the background '''
        self.screen.fill(self.black)
        self.screen.blit(self.background, self.backgroundrect)
        
        if self.gameOver:
            ''' display game over '''
            surfaceGameOverFont = self.gameOverFont.render("GAME OVER", True, self.fontColor)
            gameOverRect = surfaceGameOverFont.get_rect()
            gameOverRect.bottom = self.height / 2
            gameOverRect.left = (self.width - gameOverRect.width) / 2
            self.screen.blit(surfaceGameOverFont, gameOverRect)
            
            ''' display the player's score '''
            surfaceGameOverScoreFont = self.gameOverScoreFont.render("Score: %d" % self.player.score, True, self.fontColor)
            gameOverScoreRect = surfaceGameOverScoreFont.get_rect()
            gameOverScoreRect.top = gameOverRect.bottom + 20
            gameOverScoreRect.left = (self.width - gameOverScoreRect.width) / 2
            self.screen.blit(surfaceGameOverScoreFont, gameOverScoreRect)
            
            ''' display the hit space for main menu '''
            surfaceGameOverSpaceFont = self.gameOverSpaceForMainMenu.render("Hit Space to return to main menu", True, self.fontColor)
            gameOverSpaceRect = surfaceGameOverSpaceFont.get_rect()
            gameOverSpaceRect.top = gameOverScoreRect.bottom + 20
            gameOverSpaceRect.left = (self.width - gameOverSpaceRect.width) / 2
            self.screen.blit(surfaceGameOverSpaceFont, gameOverSpaceRect)
            
            ''' refresh the screen '''
            pygame.display.flip()
            return
        
        if not self.gameStarted:
            ''' only draw the click to start screen if the game is not started '''
            ''' draw the title '''
            surfaceTitleFont = self.titleFont.render("Paradox", True, self.fontColor)
            titleRect = surfaceTitleFont.get_rect()
            titleRect.top = (self.height - titleRect.height) / 2
            titleRect.left = (self.width - titleRect.width) / 2
            self.screen.blit(surfaceTitleFont, titleRect)
            
            ''' draw the click to start message '''
            surfaceSpaceToStart = self.spaceToStartFont.render("Hit Space to start", True, self.fontColor)
            spaceRect = surfaceSpaceToStart.get_rect()
            spaceRect.top = titleRect.bottom + 20
            spaceRect.left = (self.width - spaceRect.width) / 2
            self.screen.blit(surfaceSpaceToStart, spaceRect)
            
            ''' update the screen '''
            pygame.display.flip() 
            return
        
        ''' draw the bullets '''
        for b in self.playeractivebulletlist:
            self.screen.blit(b.img, b.rect)
            
        for b in self.enemyactivebulletlist:
            self.screen.blit(b.img, b.rect)

        ''' draw the player '''
        self.screen.blit(self.player.img, self.player.rect)
        
        ''' draw the afterburn fire, if it is engaged '''
        if self.afterburn:
            afterburnRect = self.afterburnSurface.get_rect()
            afterburnRect.right = self.player.rect.left
            afterburnRect.top = self.player.rect.top - 30
            self.screen.blit(self.afterburnSurface, afterburnRect) 
            
        
        ''' draw the enemies '''
        for o in self.obstaclelist:
            self.screen.blit(o.img, o.rect)
            
        ''' draw the score '''
        fontSurface = self.scoreFont.render("%d" % self.player.score, True, self.fontColor)
        fontRect = fontSurface.get_rect()
        fontRect.top = 0
        fontRect.left = (self.width - fontRect.width) / 2
        self.screen.blit(fontSurface, fontRect)
            
        ''' refresh the display '''
        pygame.display.flip()
        
    def __doPlayerDeathAnimation(self):
        
        self.draw()
        self.playBigExplosionSound()
        
        ''' generate a bunch of fires on the screen '''
        for _ in range(20):
            fireRect = self.fire.get_rect()
            fireRect.left = self.player.rect.left - fireRect.width / 2 + random.randint(0, self.player.rect.width)
            fireRect.top = self.player.rect.top - random.randint(0, self.player.rect.height)  
            self.screen.blit(self.fire, fireRect)
            pygame.display.flip()
            time.sleep(0.2)

        ''' play the game over sound '''
        self.playGameOverSound()
        
        ''' 
        clear the event list
        this is to prevent the game to returning the main menu
        if the player presses the space bar during the death animation 
        '''        
        pygame.event.clear()      
        
        ''' change the game state variables '''
        self.gameStarted = False
        self.gameOver = True
         
    
    def playAfterburnSound(self):
        ''' play the afterburn sound '''
        self.afterburnSound.play()
        
    def playBigExplosionSound(self):
        ''' play the big explosion sound '''
        self.bigExplosionSound.play()
        
    def playExplosionSound(self):
        ''' play the explosion sound '''
        self.explosionSound.play()
        
    def playGameOverSound(self):
        ''' play the game over sound '''
        self.gameOverSound.play()
        
    def playPewSound(self):
        ''' play the pew sound '''
        self.pewSound.play()    
    
    def playPowSound(self):
        ''' play the pow sound '''
        self.powSound.play()
        
    def playTinkSound(self):
        ''' play the tink sound '''
        self.tinkSound.play()
        
    def playTuckSound(self):
        ''' play the tuck sound '''
        self.tuckSound.play()
        
    def __reset(self):
        ''' movement directions '''
        self.travelLeft = False
        self.travelRight = False
        self.travelUp = False
        self.travelDown = False
        
        ''' shooting and afterburn '''
        self.shooting = False
        self.afterburn = False
        
        ''' reset the enemies '''
        for e in self.enemylist:
            e.reset(self.width, self.height)
        
        ''' move all the active bullets into the reserve '''    
        playerbulletstoreserve = []
        enemybulletstoreserve = []
            
        for b in self.playeractivebulletlist:
            playerbulletstoreserve.append(b)
            
        for b in self.enemyactivebulletlist:
            enemybulletstoreserve.append(b)
            
        for b in playerbulletstoreserve:    
            self.playerreservebulletlist.append(b)
            self.playeractivebulletlist.remove(b)
        
        for b in enemybulletstoreserve:
            self.enemyreservebulletlist.append(b)
            self.enemyactivebulletlist.remove(b)
        
        ''' reset the position of the reserve bullets '''    
        for b in self.playerreservebulletlist:
            b.reset(self.width, self.height)
            
        for b in self.enemyreservebulletlist:
            b.reset(self.width, self.height)
            
        self.player.reset()
          

if __name__ == '__main__':
    
    game = Game()    
    
    ''' the main game loop '''
    while 1:
        ''' the game is exited by pressing the escape key '''
        key = pygame.key.get_pressed()
        
        if key[pygame.K_ESCAPE]:            
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        
        ''' handle events, sysexit and keyboard '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                game.handleKeyDownEvent(event)
            elif event.type == pygame.KEYUP:
                game.handleKeyUpEvent(event)

        ''' update the game logic '''
        game.update()
        
        ''' draw the updated game '''
        game.draw()
        
        ''' sleep so the game doesn't run too fast '''        
        time.sleep(0.01)
               
