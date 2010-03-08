'''
Created on Mar 7, 2010

@author: abrad087
'''

import pygame

class Player:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.highScore = 0;
        self.playerImg = pygame.image.load("player.bmp")
        self.playerRect = self.playerImg.get_rect()
        self.ySpeed = 0;
        self.xSpeed = 0;
        
    def changeSpeed(self, direction, value):
        if direction == "UP":
            self.ySpeed -= value
        elif direction == "DOWN":
            self.ySpeed += value
        elif direction == "LEFT":
            self.xSpeed -= value
        elif direction == "RIGHT":
            self.xSpeed += value
            
    def death(self):
        
        
#   def move(self, obstacles):
#       
#       self.playerRect.left += self.xSpeed
#       
#       if (self.playerRect.collidelist != -1):
#           print "You dead!"
#       
#      
#       if playerRect.bottom < deadlyObject.top:
#           if playerRect.top 
#           if playerRect.right > deadlyObject.left: