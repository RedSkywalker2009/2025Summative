import sys
import pygame
from utils import Utils
from tilemap import Tilemap

#the scale in witch the pixels are being scaled up
RENDER_SCALE = 2.0

class Editor:


    def __init__(self):

        #name the screen
        print("Hi, im initializing") 

        pygame.init()
        
        pygame.display.set_caption("editor")
        #creating the screen and setting the size
        self.screen = pygame.display.set_mode((640,480))
        #creating as smaller screen to put every thing on and then scaleing up to the first screen
        self.display = pygame.Surface((320,240))

        #setting framerate
        self.clock = pygame.time.Clock()

        #loading in my immages
        self.assets = {
            "decor" : Utils.load_images("tiles/decor"),
            "grass" : Utils.load_images("tiles/grass"),
            "large_decor" : Utils.load_images("tiles/large_decor"),
            "stone" : Utils.load_images("tiles/stone"),
        }
        #setting my movement
        self.movement = [False,False,False,False]
        #setting camra
        self.scroll = [0, 0]
        #setting tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        #setting my list and the group and varian for the users choosing 
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        #setting my bools to false
        self.clicking = False
        self.right_clicking = False
        self.shift = False

    def run (self):
        #game loop
        while True:
            #setting backround to black
            self.display.fill((0,0,0))

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            self.display.blit(current_tile_img, (100,100))
        # set an event to close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                    if event.button == 3:
                        self.right_clicking = True

                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:      
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                
            self.screen.blit(pygame.transform.scale (self.display, self.screen.get_size()) ,(0,0))
            #tell the game to update 
            pygame.display.update()
            # a sleep untill 60fps is maintained
            self.clock.tick(60)


Editor().run()