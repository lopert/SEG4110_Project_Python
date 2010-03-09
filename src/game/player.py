'''
Created on Mar 7, 2010

@author: abrad087
'''

import pygame

class Player:
    '''
    classdocs
    '''


    def __init__(self, surface):
        '''
        Constructor
        '''
        self.score = 0;
        self.img = surface
        self.rect = self.img.get_rect()        
        self.ySpeed = 0;
        self.xSpeed = 0;
                    
    def death(self):
        ''' halt the ship when it dies '''
        self.xSpeed = 0
        self.ySpeed = 0
        
    def movement(self):
       ''' move the player's rectangle '''
       self.rect.left += self.xSpeed
       self.rect.top += self.ySpeed
       
    def reset(self):
        ''' reset the player '''
        self.score = 0;
        self.ySpeed = 0;
        self.xSpeed = 0;
        self.rect.top = 0;
        self.rect.left = 0;