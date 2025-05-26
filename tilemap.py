import pygame

NEIGHBOR_OFFSETS = [(-1,0), (-1,1), (-1,-1), (0,0), (1,0), (1,1), (1,-1), (0,1), (0,-1)]

PHYSICS_TILES = {"grass", "stone"}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.setTile(20+i, 20, "grass", 1) 
            self.setTile(5, 20+i,"stone", 1) 
            self.setTile(3+i, 5, "grass", 1) 
            self.setTile(15, 19+i,"stone", 1) 
            self.setTile(2, 10+i,"stone", 1) 
            self.setTile(0+i, 40, "grass", 1) 
            self.setTile(10+i, 40, "grass", 1) 
            self.setTile(-10+i, 40, "grass", 1) 
            self.setTile(20+i, 40, "grass", 1) 
            self.setTile(30+i, 40, "grass", 1) 
            self.setTile(-20+i, 40, "grass", 1) 
            self.setTile(6+i, 9, "grass", 1) 
            self.setTile(4, 20+i,"stone", 1) 
            self.setTile(29+i, 16, "grass", 1) 
            self.setTile(11, 22+i,"stone", 1) 
            self.setTile(21, 10+i,"stone", 1) 
            self.setTile(27+i, 19, "grass", 1) 
            self.setTile(16, 17+i,"stone", 1) 
            self.setTile(7+i, 1, "grass", 1) 
            self.setTile(30, 3+i,"stone", 1) 
            self.setTile(11, 22+i,"stone", 1) 

    def setTile(self, x, y, type, variant):
        self.tilemap[str(x) + ';' + str(y)] = {"type": type, "variant": variant, "pos": (x, y)}
    
    def tiles_around(self,pos):
        
        tiles = []

        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile["pos"][0] * self.tile_size,tile["pos"][1] * self.tile_size, self.tile_size, self.tile_size)) 
        return rects

        
    def render(self,surf, offset = (0,0)):

        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile["type"]][tile["variant"]],(tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size):
             for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size):
                 loc = str(x) + ";" + str(y)
                 if loc in self.tilemap:
                     tile = self.tilemap[loc] 
                     surf.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["pos"][0] * self.tile_size - offset[0], tile["pos"][1] * self.tile_size - offset[1]))