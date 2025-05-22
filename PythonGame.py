import sys
import pygame


from entities import PhyisicsEntity
from utils import Utils
from tilemap import Tilemap
from clouds import Clouds


class Game:


    def __init__(self):

        #name the screen
        print("Hi, im initializing") 

        pygame.init()
        
        pygame.display.set_caption("plat former")
        #creating the screen and setting the size
        self.screen = pygame.display.set_mode((640,480))

        self.display = pygame.Surface((320,240))

        #setting framerate
        self.clock = pygame.time.Clock()

        self.movement = [False,False]

        self.assets = {
            "decor" : Utils.load_images("tiles/decor"),
            "grass" : Utils.load_images("tiles/grass"),
            "large_decor" : Utils.load_images("tiles/large_decor"),
            "stone" : Utils.load_images("tiles/stone"),
            "player" : Utils.load_image("entities/player.png"),
            "clouds": Utils.load_images("clouds")
        }

        self.clouds = Clouds(self.assets["clouds"], count = 16)
        
        self.player = PhyisicsEntity(self, 'player', (50, 50), (8, 15))

        self.scroll = [0, 0]

        self.tilemap = Tilemap(self, tile_size=16)


    def run (self):
        #game loop
        while True:
            self.display.fill((0,0,80))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0]) /10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1]) /10

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)

            self.player.update(self.tilemap,(self.movement[1] - self.movement[0],0))
            self.player.render(self.display, render_scroll)

            print(self.tilemap.physics_rects_around(self.player.pos))

            
        # set an event to close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.player.velosity[1] = -3
                    if event.key == pygame.K_SPACE:
                        self.player.velosity[1] = -10
                if event.type == pygame.KEYUP:      
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                
            self.screen.blit(pygame.transform.scale (self.display, self.screen.get_size()) ,(0,0))
            #tell the game to update 
            pygame.display.update()
            # a sleep untill 60fps is maintained
            self.clock.tick(60)


Game().run()