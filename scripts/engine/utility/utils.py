import os

import pygame

BASE_IMG_PATH = 'data/images/'

# Load a single PNG
def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((255,255,255))
    return img

# Load all PNGs in a path
def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

# Get a single tile from a sheet
def get_tile_image_from_sheet(sheet, pos_x, pos_y, width, height):
    # Create a new surface for the specific tile
    tile_image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    tile_image.blit(sheet, (0, 0), (pos_x, pos_y, width, height))
    
    return tile_image


# Get a defined range of sprites from a sheet
# Version x and y represent how many tiles on x and y axis should be extracted
# Starting y and x represent the starting position on the sheet
# Size x and y is the total size of each tile
# Color is the colorkey that needs to be filtered out
def get_tiles_from_sheet(path, versions_x, versions_y, starting_x, starting_y, size_x, size_y):
    sheet = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    images = []
    
    # Setup for double while loop
    current_iteration_y = 0
    
    while current_iteration_y <= versions_y:
        x_holder = starting_x  # Store the original starting_x position
        current_iteration_x = 0
        
        while current_iteration_x <= versions_x:
            # Go through the tiles from the sheet on the y and x location, with a given size
            images.append(get_tile_image_from_sheet(sheet, starting_x, starting_y, size_x, size_y))
            starting_x += size_x  # Move to the next tile on the x-axis
            current_iteration_x += 1
        
        # Increment the position and current iteration
        starting_y += size_y  # Move to the next row
        current_iteration_y += 1
        current_iteration_x = 0
        starting_x = x_holder  # Reset starting_x for the next row
    
    return images





class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0  
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def Update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]