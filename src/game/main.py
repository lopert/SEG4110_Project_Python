'''
Created on Mar 7, 2010

@author: kmott071
'''

import sys, pygame, time\


if __name__ == '__main__':
    print "Hello World"
     
    pygame.init()

    size = width, height = 1024, 768
    speed = [0, 0]
    gravity = [0, 0]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    
    
    background = pygame.image.load("3D_Hot_Planet.jpg")
    backgroundrect = background.get_rect()

    player = pygame.image.load("player_ship_resized.png")
    playerrect = player.get_rect()
    
    enemy = pygame.image.load("ufo_resized.png");
    enemyrect = enemy.get_rect()

    while 1:
        key = pygame.key.get_pressed()
        
        if key[pygame.K_ESCAPE]:            
            pygame.event.post(pygame.event.Event(pygame.QUIT))
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        if key[pygame.K_UP] and key[pygame.K_DOWN]:
            speed[1] = 0
        elif key[pygame.K_UP]:
            speed[1] -= 2
        elif key[pygame.K_DOWN]:
            speed[1] += 2
        #else:
        #    speed[1] = 0
            
        if key[pygame.K_LEFT] and key[pygame.K_RIGHT]:
            speed[0] = 0
        elif key[pygame.K_LEFT]:
            speed[0] -= 2
        elif key[pygame.K_RIGHT]:
            speed[0] += 2
        #else:
        #    speed[0] = 0
            
        speed[0] -= gravity[0]
        speed[1] -= gravity[1]       
        
        if playerrect.top + speed[1] < 0:
            speed[1] = 0
        if playerrect.bottom + speed[1] > height:
            speed[1] = 0
        if playerrect.left + speed[0] < 0:
            speed[0] = 0
        if playerrect.right + speed[0] > width:
            speed[0] = 0
  
        playerrect = playerrect.move(speed)

        screen.fill(black)
        screen.blit(background, backgroundrect)
        screen.blit(player, playerrect)
        screen.blit(enemy, enemyrect)
        pygame.display.flip() 
        time.sleep(0.01)       
