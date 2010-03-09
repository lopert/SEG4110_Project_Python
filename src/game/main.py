'''
Created on Mar 7, 2010

@author: kmott071
'''

import sys, pygame, time, enemy, player, bullet, random

class Game:
    
    def __init__(self):
        pygame.init()

        self.size = self.width, self.height = (1024, 768)
        self.black = 0, 0, 0
        
        self.gameStarted = False
        self.gameOver = False

        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        
        ''' the font for the score board '''
        fontPath = pygame.font.match_font("Arial", True, False)
        self.scoreFont = pygame.font.Font(fontPath, 30)
        
        ''' the font for the click to start '''
        self.titleFont = pygame.font.Font(fontPath, 50)
        self.clickToStartFont = pygame.font.Font(fontPath, 20)      
        
        ''' load the images '''
        self.background = pygame.image.load("3D_Hot_Planet.jpg")
        self.backgroundrect = self.background.get_rect()
        self.player = player.Player(pygame.image.load("player_ship_resized.png"))
        self.alienUFOskin = pygame.image.load("ufo_resized.png")
        self.laser = pygame.image.load("laser.png")
        self.laserBall = pygame.image.load("laser_ball.png")
        self.fire = pygame.image.load("cartoon_fire_resized.png")
        
        ''' Generate bullets '''
        self.playerreservebulletlist = []
        self.enemyreservebulletlist = []
        self.playeractivebulletlist = []
        self.enemyactivebulletlist = []
        
        self.playerbulletskin = pygame.image.load("laser.png")
        for i in range(50):
            self.playerreservebulletlist.append(bullet.Bullet(self.playerbulletskin))
            
        self.enemybulletskin = self.laserBall
        for i in range(50):
            self.enemyreservebulletlist.append(bullet.Bullet(self.enemybulletskin))
            
        ''' Generate enemy bullets '''
            
        
        
        ''' Generate Enemies '''
        self.enemylist = []
        self.enemylist.append(enemy.Enemy(self.alienUFOskin, 26))
        self.enemylist.append(enemy.Enemy(self.alienUFOskin, 20))
        self.enemylist.append(enemy.Enemy(self.alienUFOskin, 16))
        
        self.enemyrectlist = []
        for e in self.enemylist:
            self.enemyrectlist.append(e.rect)
        
        ''' What can the player be killed by? '''
        self.obstaclelist = []        
        for e in self.enemylist:
            self.obstaclelist.append(e)
        
        self.obstaclerectlist = []
        for o in self.obstaclelist:
            self.obstaclerectlist.append(o.rect)
        
        ''' load the sounds '''
        pygame.mixer.init()
        self.afterburnSound = pygame.mixer.Sound("../../sounds/afterburn.ogg")
        self.bigExplosionSound = pygame.mixer.Sound("../../sounds/big_explosion.ogg")
        self.explosionSound = pygame.mixer.Sound("../../sounds/explosion.ogg")
        self.gameOverSound = pygame.mixer.Sound("../../sounds/game_over.ogg")
        self.pewSound = pygame.mixer.Sound("../../sounds/pew.ogg")
        self.powSound = pygame.mixer.Sound("../../sounds/pow.ogg")
        self.tinkSound = pygame.mixer.Sound("../../sounds/tink.ogg")
        self.tuckSound = pygame.mixer.Sound("../../sounds/tink.ogg")

        ''' movement directions '''
        self.travelLeft = False
        self.travelRight = False
        self.travelUp = False
        self.travelDown = False
        
        self.shooting = False     
        
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
            self.shooting = True
            
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
            
    def handleMouseDownEvent(self, event):
        if event.button == 1:
            if not self.gameStarted:
                self.gameStarted = True
        
            
    def update(self):
        ''' don't do anything if the game is not started '''
        if not self.gameStarted:
            return
               
        ''' adjust the speeds '''
        if self.travelLeft:
            self.player.xSpeed -= 2
        if self.travelRight:
            self.player.xSpeed += 2
        if self.travelUp:
            self.player.ySpeed -= 2
        if self.travelDown:
            self.player.ySpeed += 2
            
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
                
        for b in self.playeractivebulletlist:
            if (b.rect.left > self.width):
                bulletstoreserve.append(b) 
                b.reset(self.width, self.height)
                
        for b in bulletstoreserve:
            self.playerreservebulletlist.append(b)
            self.playeractivebulletlist.remove(b)
        
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
                bullet.xvelocity = -35
                self.playPowSound()
            
                
        ''' update the player score '''
        self.player.score += 1
        
        
    def draw(self):
        ''' draw the background '''
        self.screen.fill(self.black)
        self.screen.blit(self.background, self.backgroundrect)
        
        if not self.gameStarted:
            ''' only draw the click to start screen if the game is not started '''
            ''' draw the title '''
            surfaceTitleFont = self.titleFont.render("Paradox", True, (255,255,0))
            titleRect = surfaceTitleFont.get_rect()
            titleRect.top = (self.height - titleRect.height) / 2
            titleRect.left = (self.width - titleRect.width) / 2
            self.screen.blit(surfaceTitleFont, titleRect)
            
            ''' draw the click to start message '''
            surfaceClickToStart = self.clickToStartFont.render("Click to start", True, (255,255,0))
            clickRect = surfaceClickToStart.get_rect()
            clickRect.top = titleRect.bottom + 20
            clickRect.left = (self.width - clickRect.width) / 2
            self.screen.blit(surfaceClickToStart, clickRect)
            
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
        
        ''' draw the enemies '''
        for o in self.obstaclelist:
            self.screen.blit(o.img, o.rect)
            
        ''' draw the score '''
        fontSurface = self.scoreFont.render("%d" % self.player.score, True, (255,255,0))
        fontRect = fontSurface.get_rect()
        fontRect.top = 0
        fontRect.left = (self.width - fontRect.width) / 2
        self.screen.blit(fontSurface, fontRect)
            
        pygame.display.flip()
        
    def __doPlayerDeathAnimation(self):
        
        self.playBigExplosionSound()
        
        ''' generate a bunch of fires on the screen '''
        for _ in range(20):
            fireRect = self.fire.get_rect()
            fireRect.left = self.player.rect.left - fireRect.width / 2 + random.randint(0, self.player.rect.width)
            fireRect.top = self.player.rect.top - random.randint(0, self.player.rect.height)  
            self.screen.blit(self.fire, fireRect)
            pygame.display.flip()
            time.sleep(0.2)
            
        self.playGameOverSound()
                
        self.__reset()
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
        
        self.shooting = False
        
        for e in self.enemylist:
            e.reset(self.width, self.height)
            
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
            
        for b in self.playerreservebulletlist:
            b.reset(self.width, self.height)
            
        for b in self.enemyreservebulletlist:
            b.reset(self.width, self.height)
            
        self.player.reset()
          

if __name__ == '__main__':
    
    game = Game()
    
    while 1:
        key = pygame.key.get_pressed()
        
        if key[pygame.K_ESCAPE]:            
            pygame.event.post(pygame.event.Event(pygame.QUIT))
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                game.handleKeyDownEvent(event)
            elif event.type == pygame.KEYUP:
                game.handleKeyUpEvent(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handleMouseDownEvent(event)

        game.update()
        game.draw()        
        time.sleep(0.01)
               
