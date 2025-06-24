#-----------------
#Final Project Settings
#Hailey-lynn Aldred
#-----------------

from os import walk #i spent like 20 minutes trying to figure out where walk was coming from only to see this 2 days later
from csv import reader

WIDTH    = 1280
HEIGHT   = 700
FPS      = 120
TILESIZE = 32


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
