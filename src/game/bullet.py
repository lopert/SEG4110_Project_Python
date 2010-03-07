'''
Created on Mar 7, 2010

@author: abrad087
'''
import pygame

class Bullet:
    '''
    classdocs
    '''


    def __init__(self, velocity, direction):
        '''
        Constructor
        '''
        self.bulletImg = pygame.image.load("player.bmp")
        self.bulletRect = self.bulletImg.get_rect()
        self.velocity = velocity
        self.direction = direction
        
    def move(self):
        if (self.direction == "LEFT"):
            self.bulletRect.left -= self.velocity
            
        elif (self.direction == "RIGHT"):
            self.bulletRect.left += self.velocity 
        
        