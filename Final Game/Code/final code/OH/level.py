#-----------------
#Final Project Week Two Level
#May 29 - June 4
#Hailey-lynn Aldred
#-----------------
from user import User
from settings import *
import pygame
from tile import Tile


class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        #sprite set-up
        self.create_map()
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_you shall not pass.csv')
            } #supposed to stop user from going over the house but its not working
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')

        self.user = User((2100,1050),[self.visible_sprites],self.obstacle_sprites)
        
    def run(self): 
        # update and draw game
        self.visible_sprites.custom_draw(self.user)
        self.visible_sprites.update()
        
class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        #creating the floor
        self.floor_surf = pygame.image.load('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        
    def custom_draw(self,user):
        #getting the offset
        self.offset.x = user.rect.centerx - self.half_width
        self.offset.y = user.rect.centery - self.half_height
        
        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        
        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)