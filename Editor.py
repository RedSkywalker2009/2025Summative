import sys
import pygame
from utils import Utils
from tilemap import Tilemap

#the scale in witch the pixels are being scaled up
RENDER_SCALE = 3.0

class Editor:

    Resolution = (1920, 1080)


    def __init__(self):

        #name the screen

        pygame.init()
        
        pygame.display.set_caption("editor")
        #creating the screen and setting the size
        self.screen = pygame.display.set_mode(Editor.Resolution)
        #creating as smaller screen to put every thing on and then scaleing up to the first screen
        self.display = pygame.Surface((Editor.Resolution[0]/3, Editor.Resolution[1]/3))
        #creating as smaller screen to put every thing on and then scaleing up to the first screen

        #setting framerate
        self.clock = pygame.time.Clock()

        #loading in my immages
        self.assets = {
            "decor" : Utils.load_images("tiles/decor"),
            "grass" : Utils.load_images("tiles/grass"),
            "large_decor" : Utils.load_images("tiles/large_decor"),
            "stone" : Utils.load_images("tiles/stone"),
            "turret" : Utils.load_images("tiles/turret"),
            "scroll" : Utils.load_images("tiles/scroll")

        }
        #setting my movement
        self.movement = [False,False,False,False]
        #setting camra
        self.scroll = [0, 0]
        #setting tilemap
        self.tilemap = Tilemap(self, tile_size=16)
        
        try:
            self.tilemap.load("data/maps/easy.json")
        except FileNotFoundError:
            pass
        #setting my list and the group and varian for the users choosing 
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        #setting my bools to false
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def run (self):
        #game loop
        while True:
            #setting backround to black
            self.display.fill((0,0,0))

            self.scroll[0] += (self.movement[1] - self.movement [0]) * 3
            self.scroll[1] += (self.movement[3] - self.movement [2]) * 3
            
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)

            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))
            
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {"type" : self.tile_list[self.tile_group], "variant" : self.tile_variant, "pos" : tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile["type"]][tile["variant"]]
                    tile_r = pygame.Rect(tile["pos"][0] - self.scroll[0], tile["pos"][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            
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
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({"type" : self.tile_list[self.tile_group],  "variant" : self.tile_variant, "pos" : (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
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
                    if event.key == pygame.K_r:
                        self.tilemap.save("data/maps/easy.json")
                    if event.key == pygame.K_f:
                        self.ongrid = not self.ongrid
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