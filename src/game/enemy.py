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


    def __init__(self):
        '''
        Constructor
        '''
        
        self.enemyImg = pygame.image.load("player.bmp")
        self.enemyRect = self.enemyImg.get_rect()
        
    def shootRandom(self):
        if (random.sample([0,1], 1) == 1):
            self.shoot(self);
            
        
    def shoot(self):
        #generate a bullet here
        