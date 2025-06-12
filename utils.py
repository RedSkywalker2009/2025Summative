import pygame

import os

BASE_IMG_PATH = "data/images/"

class Utils:

    def scale_by(image:pygame.Surface, scale:float) -> pygame.Surface:
        width = image.get_width() * scale
        height = image.get_height() * scale
        return pygame.transform.smoothscale(image, (width, height))

    def load_image(path, size = None, scale = 1):
        if not size is None:
            img = pygame.transform.smoothscale(pygame.image.load(BASE_IMG_PATH + path), size).convert()
        else:
            img = Utils.scale_by(pygame.image.load(BASE_IMG_PATH + path), scale).convert()
        img.set_colorkey((0,0,0))
        return img
    def load_images(path, size = None, scale = 1):
        images = []
        print(path)
        for img_name in os.listdir(BASE_IMG_PATH + path):
            print(path + "/" + img_name)
            images.append(Utils.load_image( path + "/" + img_name, size, scale))
        return images
    
class Animations:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_duration = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animations(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images [int(self.frame / self.img_duration)]
    

    print( pygame.font.get_fonts() )