'''
Created on Mar 7, 2010

@author: abrad087
'''
import pygame

class Bullet:
    '''
    classdocs
    '''


    def __init__(self, surface):
        '''
        Constructor
        '''
        self.img = surface
        self.rect = self.img.get_rect()
        self.xvelocity = 0
        self.yvelocity = 0
        self.rect.top = 6000
        
    def movement(self):
        ''' move the bullet's rectangle '''
        self.rect.left += self.xvelocity
        self.rect.top += self.yvelocity  
        
    def reset(self, screenwidth, screenheight):
        ''' reset the bullet's attributes '''
        self.xvelocity = 0
        self.yvelocity = 0
        self.rect.top = screenheight * 3
        self.rect.left = screenwidth / 2
        
        