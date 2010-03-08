'''
Created on Mar 7, 2010

@author: abrad087
'''
import pygame

class Cube:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cubeImg = pygame.image.load("player.bmp")
        self.cubeRect = self.cubeImg.get_rect()
        self.speed = 2
        