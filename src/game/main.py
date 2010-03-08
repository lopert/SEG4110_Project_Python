'''
Created on Mar 7, 2010

@author: kmott071
'''

import sys, pygame, time, enemy, player

class Game:
    
    def __init__(self):
        pygame.init()

        self.size = self.width, self.height = (1024, 768)
        self.speed = [0, 0]
        self.black = 0, 0, 0
        
        self.gameStarted = False

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
        
        self.enemyone = enemy.Enemy(self.alienUFOskin, 43)
        self.enemytwo = enemy.Enemy(self.alienUFOskin, 20)
        self.enemythree = enemy.Enemy(self.alienUFOskin, 36)
        
        self.obstacles = []
        self.obstacles.append(self.enemyone)
        self.obstacles.append(self.enemytwo)
        self.obstacles.append(self.enemythree)
        
        self.obstaclerects = []
        for o in self.obstacles:
            self.obstaclerects.append(o.rect)
        
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
        for o in self.obstacles:
            o.movement()
        
        ''' check for collisions '''
        if (self.player.rect.collidelist(self.obstaclerects) != -1):
                ''' death code '''
                self.player.death()
                self.playBigExplosionSound()                
                
        ''' reset any obstacles that have gone by '''
        for o in self.obstacles:
            if o.rect.right < 0:
                o.reset(self.width, self.height)
                
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

        ''' draw the player '''
        self.screen.blit(self.player.img, self.player.rect)
        
        ''' draw the enemies '''
        for o in self.obstacles:
            self.screen.blit(o.img, o.rect)
            
        ''' draw the score '''
        fontSurface = self.scoreFont.render("%d" % self.player.score, True, (255,255,0))
        fontRect = fontSurface.get_rect()
        fontRect.top = 0
        fontRect.left = (self.width - fontRect.width) / 2
        self.screen.blit(fontSurface, fontRect)
            
        pygame.display.flip() 
    
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
               
