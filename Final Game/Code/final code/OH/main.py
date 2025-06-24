#-----------------
#Final Project Week Two Main
#May 29 - June 4
#Hailey-lynn Aldred
#-----------------

import pygame, sys #this is important
from level import Level
from settings import *

class Game:
    def __init__(self):
        pygame.init() #this is imported
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Mystery Hunt')#i need to come up with a better name
        self.clock = pygame.time.Clock()
        #self.background = pygame.image.load('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map.png') this was a test to see if it would work
        
        self.level = Level() #this is imported
        
    def run(self):
        while True:
           # self.screen.blit(self.background,(0,0)) #this was also the test
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #this is imported
                    
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
            
            
if __name__ == '__main__':
    game = Game()
    game.run()