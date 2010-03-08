'''
Created on Mar 7, 2010

@author: kmott071
'''

import sys, pygame, time

class Game:
    
    def __init__(self):
        pygame.init()

        self.size = self.width, self.height = (1024, 768)
        self.speed = [0, 0]
        self.black = 0, 0, 0

        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        
        ''' load the images '''
        self.background = pygame.image.load("3D_Hot_Planet.jpg")
        self.backgroundrect = self.background.get_rect()

        self.player = pygame.image.load("player_ship_resized.png")
        self.playerrect = self.player.get_rect()
    
        self.enemy = pygame.image.load("ufo_resized.png");
        self.enemyrect = self.enemy.get_rect()
        
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
        ''' the arrow keys affect mouvement '''
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
        ''' the arrow keys affect mouvement ''' 
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
        
            
    def update(self):       
        ''' adjust the speeds '''
        if self.travelLeft:
            self.speed[0] -= 2
        if self.travelRight:
            self.speed[0] += 2
        if self.travelUp:
            self.speed[1] -= 2
        if self.travelDown:
            self.speed[1] += 2
        
        ''' prevent the player from going off screen '''
        if self.playerrect.top + self.speed[1] < 0:
            self.speed[1] = 0
        if self.playerrect.bottom + self.speed[1] > self.height:
            self.speed[1] = 0
        if self.playerrect.left + self.speed[0] < 0:
            self.speed[0] = 0
        if self.playerrect.right + self.speed[0] > self.width:
            self.speed[0] = 0
  
        ''' move the player '''
        self.playerrect = self.playerrect.move(self.speed)
        
    def draw(self):
        ''' draw the scene '''
        self.screen.fill(self.black)
        self.screen.blit(self.background, self.backgroundrect)
        self.screen.blit(self.player, self.playerrect)
        self.screen.blit(self.enemy, self.enemyrect)
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

        game.update()
        game.draw()        
        time.sleep(0.01)       
