#-----------------
#Final Project User
#Hailey-lynn Aldred
#-----------------
import pygame
from settings import *

class User(pygame.sprite.Sprite): 
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        sprite_original = pygame.image.load('C:/Users/Brald/HL CompSci 30/OOP/Final Game/Graphics/User/test/user_test.png').convert_alpha()
        #--I had to look this part up bc my sprite was too small
        original_width,original_height = sprite_original.get_size() 
        new_width,new_height = original_width * 2, original_height * 2
        self.image = pygame.transform.scale(sprite_original,(new_width,new_height))
        #--
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        self.direction = pygame.math.Vector2()
        self.speed = 3
        self.status = 'for'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.obstacle_sprites = obstacle_sprites
    
        
    def input(self): 
        keys = pygame.key.get_pressed()
        #--y direction
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'back'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'for'
        else:
            self.direction.y = 0
        #--x direction
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0
            
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                self.status = self.status + '_idle'
            
    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collisions('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collisions('vertical')
        self.rect.center = self.hitbox.center
        
    def collisions(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #mov ing left
                        self.hitbox.left = sprite.hitbox.right
                        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom
        
    def update(self):
        self.input()
        self.get_status()
        self.move(self.speed)
