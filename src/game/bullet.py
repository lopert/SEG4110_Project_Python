'''
Created on Mar 7, 2010

@author: abrad087
'''
import pygame

class Bullet:
    '''
    classdocs
    '''


    def __init__(self, velocity):
        '''
        Constructor
        '''
        self.img = pygame.image.load("player.bmp")
        self.rect = self.img.get_rect()
        self.velocity = velocity
        
    def movement(self):
        self.rect.left += velocity 
        
        