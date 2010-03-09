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
        
#    def changeSpeed(self, direction, value):
#        if direction == "UP":
#            self.ySpeed -= value
#        elif direction == "DOWN":
#            self.ySpeed += value
#        elif direction == "LEFT":
#            self.xSpeed -= value
#        elif direction == "RIGHT":
#            self.xSpeed += value
            
    def death(self):
        self.xSpeed = 0
        self.ySpeed = 0
        
    def movement(self):
       
       self.rect.left += self.xSpeed
       self.rect.top += self.ySpeed
       
    def reset(self):
        self.score = 0;
        self.ySpeed = 0;
        self.xSpeed = 0;
        self.rect.top = 0;
        self.rect.left = 0;