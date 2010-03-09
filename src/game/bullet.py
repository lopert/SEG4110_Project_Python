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
        self.velocity = 0
        self.rect.top = 6000
        
    def movement(self):
        self.rect.left += self.velocity 
        
    def reset(self):
        velocity = 0
        self.rect.top = 6000
        
        