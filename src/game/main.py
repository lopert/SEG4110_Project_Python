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

        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        
        ''' load the images '''
        self.background = pygame.image.load("3D_Hot_Planet.jpg")
        self.backgroundrect = self.background.get_rect()

        self.player = player.Player(pygame.image.load("player_ship_resized.png"))
        
        self.enemyone = enemy.Enemy(pygame.image.load("ufo_resized.png"), 5)
        
        self.obstacles = []
        self.obstacles.append(self.enemyone)
        
        self.obstaclerects = []
        for o in self.obstacles:
            self.obstaclerects.append(o.rect)
        
        self.enemyone.rect.left = 500
        self.enemyone.rect.top = 500
    
        #self.enemy = ;
        #self.enemyrect = self.enemy.get_rect()
        
        ''' mouvement directions '''
        self.travelLeft = False
        self.travelRight = False
        self.travelUp = False
        self.travelDown = False
        
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
            
    def update(self):
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
                print "Death"
        
        
    def draw(self):
        ''' draw the scene '''
        self.screen.fill(self.black)
        self.screen.blit(self.background, self.backgroundrect)
        self.screen.blit(self.player.img, self.player.rect)
        self.screen.blit(self.enemyone.img, self.enemyone.rect)
        pygame.display.flip() 
        

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
        
    print "Done"       
