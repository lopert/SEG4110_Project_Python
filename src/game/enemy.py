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


    def __init__(self, speed):
        '''
        Constructor
        '''
        
        self.enemyImg = pygame.image.load("ufo_resized.png");
        self.enemyRect = self.enemyImg.get_rect()
        self.speed = speed
        
    def shootRandom(self):
        if (random.sample([0,1], 1) == 1):
            self.shoot(self);
            
        
    def shoot(self):
        #generate a bullet here
        
    def movement(self):
        self.left = self.left - self.speed
        