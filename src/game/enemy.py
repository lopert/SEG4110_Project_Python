'''
Created on Mar 7, 2010

@author: abrad087
'''

import pygame
import random

class Enemy(object):
    '''
    classdocs
    '''


    def __init__(self, surface, speed):
        '''
        Constructor
        '''
        
        self.img = surface;
        self.rect = self.img.get_rect()
        self.rect.left = -5000
        self.speed = speed
        
    def movement(self):
        ''' move the enemy's rectangle '''
        self.rect.left = self.rect.left - self.speed
        
    def reset(self, screenwidth, screenheight):
        ''' reset the enemy offscreen with random height and speed '''
        self.rect.left = screenwidth + (self.rect.width * random.randint(1,4))
        self.rect.top = self.rect.height * random.randint(0, screenheight % self.rect.height) 
        self.speed = random.randint(10, 15)
        