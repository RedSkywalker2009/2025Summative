import pygame

import os

BASE_IMG_PATH = "Python/__pycache__/ninja_game/data/images/"

class Utils:
    def load_image(path):
        img = pygame.image.load(BASE_IMG_PATH + path).convert()
        img.set_colorkey((0,0,0))
        return img
    def load_images(path):
        images = []
        print(path)
        for img_name in os.listdir(BASE_IMG_PATH + path):
            print(path + "/" + img_name)
            images.append(Utils.load_image( path + "/" + img_name))
        return images
