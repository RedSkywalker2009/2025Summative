import pygame

class PhyisicsEntity:
    def __init__(self,game,e_type,pos,size):
        self.game = game
        self.type = e_type  
        self.pos = list(pos)
        self.size = size
        self.velosity = [0,0]
        self.collisions = {"up": False,"down": False,"left": False,"right": False}
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement = (0, 0)):

        self.collisions = {"up": False,"down": False,"left": False,"right": False}

        frame_movement = (movement[0] + self.velosity[0], movement[1] + self.velosity[1])

        self.pos[0] += frame_movement[0]

        entity_rect =self.rect()
        for rects in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rects):
                if frame_movement[0] > 0:
                    entity_rect.right = rects.left
                    self.collisions["right"] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rects.right
                    self.collisions["left"] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect =self.rect()
        for rects in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rects):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rects.top
                    self.collisions["down"] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rects.bottom
                    self.collisions["up"] = True
                self.pos[1] = entity_rect.y

        self.velosity[1] = min(2,self.velosity[1] + 0.201)

        if self.collisions["down"] or self.collisions["up"]:
            self.velosity[1] = 0
    
    def render(self, surf, offset = (0,0)):
        surf.blit(self.game.assets["player"], (self.pos[0] - offset[0], self.pos[1] - offset[1]))