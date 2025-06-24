#-----------------
#Final Project Week Two
#May 29 - June 4 
#Hailey-lynn Aldred
#HHHhhhhhhhhHHHhHHHHHhh
#-----------------

import pygame, sys #this is important
from os import walk #i spent like 20 minutes trying to figure out where walk was coming from only to see this 2 days later
from csv import reader

#I'm gonna do everything in one file for now

#settings
WIDTH    = 1280
HEIGHT   = 700
FPS      = 120
TILESIZE = 64

class User(pygame.sprite.Sprite): 
    #hell yeah
    def __init__(self,pos,groups,obstacle_sprites): #this is also important
        super().__init__(groups)
        sprite_original = pygame.image.load('C:/Users/Brald/HL CompSci 30/OOP/Final Game/Graphics/User/test/user_test.png').convert_alpha()
        #--I had to look this part up bc my sprite was too small
        original_width,original_height = sprite_original.get_size() 
        new_width,new_height = original_width * 3, original_height * 3
        self.image = pygame.transform.scale(sprite_original,(new_width,new_height))
        #--
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.rect = self.image.get_rect(topleft = pos)
        self.import_user_assets()
        self.direction = pygame.math.Vector2()
        self.speed = 3
        self.status = 'for'
        self.frame_index = 0
        self.animation_speed = 0.15
        
    def import_user_assets(self):
        character_path = '../Graphics/User/'
        self.animations = {'back': [],'for': [],'left': [],'right': [],
            'right_idle': [],'left_idle': [],'back_idle': [],'for_idle': [],
            'right_attack': [],'left_attack': [],'back_attack': [],'for_attack': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        
    def input(self): #this will include other actions later, but for now it will just have movement
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
        self.rect.center += self.direction * speed
            
            
    def animate(self):
        animation = self.animations[self.status]
        
        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        #set image
        #self.image = animation[int(self.frame_index)]
        
    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)
        
def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
            
def import_folder(path): 
    surface_list = []
    
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/'+ image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list
            
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
            'floor': import_csv_layout('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_ground.csv'),
            'floor details': import_csv_layout('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_ground details.csv'),
            'fence': import_csv_layout('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_fence_fence.csv'),
            'fence ends': ('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_fence_fence ends.csv'),
            'road details': import_csv_layout('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_road details.csv'),
            'trees': import_csv_layout('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_trees_tree2.csv'),
            'trees again': ('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_trees_tree4.csv'),
            'trees againx2': ('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_trees_tree1.csv'),
            'trees againx3': ('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_trees_tree3.csv'),
            'trees againx4': ('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_trees_tree5.csv'),
            'wow this is alot of trees': ('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_trees_Tile Layer 18.csv'),
            'darkness': import_csv_layout('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_darkness.csv'),
            'more darkness': ('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_darkness2.cvs'),
            'house details': import_csv_layout('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_ground details.csv'),
            'doors': import_csv_layout('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_door layer 1.csv'),
            'more doors': ('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_door layer 2 because apparently i hate myself.csv'),
            'UGH MORE DOORS': ('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_another damn door layer because i clearly hate myself.csv'),
            'houses': import_csv_layout('C:/Users/Brald/HL CompSci 30/maps/Mystery Hunt Map_houses.csv')
        }
        
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                #if col == 'u':
                self.user = User((575,400),[self.visible_sprites],self.obstacle_sprites)
        
    def run(self):
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
            
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Mystery Hunt')#i need to come up with a better name
        self.clock = pygame.time.Clock()
        
        self.level = Level()
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.screen.fill('pink')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
            
            
if __name__ == '__main__':
    game = Game()
    game.run()
