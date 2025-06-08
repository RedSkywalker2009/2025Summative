import pygame
import math

class PhyisicsEntity:
    def __init__(self,game,e_type, pos, size, tilesize):
        self.game = game
        self.type = e_type  
        self.pos = list(pos)
        self.size = size
        self.velosity = [0,0]
        self.tile_size = tilesize
        self.collisions = {"up": False,"down": False,"left": False,"right": False}

        self.actions = ""
        self.anim_offset = (0,0)
        self.flip = False
        self.set_actions("idle")
        self.input_map = {}

        self.movement = [False, False]
        self.last_movement = [0,0]
        self.dead = False
        self.do_gravity = True
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_actions(self,action):
        if action != self.actions:
            self.actions = action
            self.animations = self.game.assets[self.type + "/" + self.actions].copy()


    def checkCollision(self, object):
         entity_rect = self.rect()
         object_rect = object.rect()
         if (not entity_rect.colliderect(object_rect)):
             return
         
         self.hit(object)
         object.hit(self)

    def hit(self, object):
        return


    def update(self, tilemap):

        movement = self.movement
        self.collisions = {"up": False,"down": False,"left": False,"right": False}

        frame_movement = (movement[0] + (self.velosity[0] * self.tile_size/16), movement[1] + (self.velosity[1] * self.tile_size/16))

        self.pos[0] += frame_movement[0]

        entity_rect = self.rect()
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
        entity_rect = self.rect()
        for rects in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rects):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rects.top
                    self.collisions["down"] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rects.bottom
                    self.collisions["up"] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True 
        
        self.last_movement = movement

        if self.do_gravity:
            self.velosity[1] = min(2, self.velosity[1] + (0.201))

        if self.collisions["down"] or self.collisions["up"]:
            self.velosity[1] = 0

        self.animations.update()


    def render(self, surf, offset = (0,0)):
        surf.blit(pygame.transform.flip(self.animations.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        if (self.game.draw_hitbox):
            rect = self.rect()  
            rect.topleft = (rect.left - offset[0], rect.top - offset[1])
            pygame.draw.rect(surf, (0,0,100), rect)

class Player(PhyisicsEntity):
    def __init__(self, game, id, pos, size, tile_size):
        super().__init__(game,"player", pos, size, tile_size)
        self.air_time = 0
        self.jumps = 2
        self.super_jumps = 1
        self.wall_slide = False
        self.dashing = 0
        self.s = {}
        self.id = id
        self.dying = False
        self.dead = False

    def update(self, tilemap):
        super().update(tilemap)

        movement = self.movement

        if (self.dying) or self.actions == "die":
            self.set_actions("die")
            self.dying = True
            self.dead = self.animations.done
            return

        self.air_time += 1
        if self.collisions["down"]:
            self.air_time = 0
            self.jumps = 2
            self.super_jumps = 1
        
        self.wall_slide = False
        if (self.collisions ["right"] or self.collisions ["left"]) and self.air_time > 4:
            self.wall_slide = True
            self.velosity[1] = min(self.velosity[1], 0.5)

            if self.collisions["right"]:
                self.flip = False
            else:
                self.flip = True
            self.set_actions("wall_slide")
    

        if not self.wall_slide :
            if self.air_time > 4:
                self.set_actions("jump")
            elif movement[0] != 0:
                self.set_actions("run")
            else:
                self.set_actions("idle")
        
        
            
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velosity[0] = abs(self.dashing) / self.dashing * 10
            if abs(self.dashing) == 51:
                self.velosity[0] *= 0.1
        
        if self.velosity[0] > 0:
            self.velosity[0] = max(self.velosity[0] - 0.1, 0)
        else:
            self.velosity[0] = min(self.velosity[0] + 0.1, 0)

    def render(self,surf,offset=(0,0)):
        super().render(surf,offset=offset)

    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velosity[0] = 3.5
                self.velosity[1] = -3.5
                self.air_time = 5
                if self.jumps > 1:
                    self.jumps = max(1, self.jumps - 1)
                elif self.jumps < 1:
                    self.jumps = min(1, self.jumps + 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velosity[0] = -3.5 
                self.velosity[1] = -3.5 
                self.air_time = 5
                if self.jumps > 1:
                    self.jumps = max(1, self.jumps - 1)
                elif self.jumps < 1:
                    self.jumps = min(1, self.jumps + 1)
                return True
            
        elif self.jumps:
            if self.air_time <= 5:
                self.velosity[1] = -4.5
            else:
                self.velosity[1] = -3.5
            self.jumps -= 1
            self.air_time = 5
            

    def super_jump(self):
        if self.super_jumps:
            self.velosity[1] = -6
            self.super_jumps -= 1
            self.jumps = 0
            self.air_time = 5
    

    def dash (self):
        if self.super_jumps > 0:
            if not self.dashing:
                if self.flip:
                    self.dashing = -60 
                else:
                    self.dashing = 60 


    def set_inputmap(self, inputs):
        self.input_map = inputs
        # Stores the direction string and the state of the direction
        self.inputs = {direction: False for direction in inputs.values()}


    def on_key_press(self, symbol: int, mod: int) -> bool:
        direction = self.input_map.get(symbol)
        if direction:
            self.inputs[direction] = True
            return True

        return False

    def on_key_release(self, symbol: int, mod: int) -> bool:
        direction = self.input_map.get(symbol)
        if direction:
            self.inputs[direction] = False
            return True

        return False
    

    def hit(self, object):
        if (object.type == "bullet"):
            self.dying = True



    def get_inputs(self):
        deltax = 0
        deltay = 0
        hasInput = any(self.inputs.values())

        if (True):
            if "JUMP" in self.inputs and self.inputs["JUMP"]:
                self.jump()
                self.inputs["JUMP"] = False
            
            if "LEFT" in self.inputs and self.inputs["LEFT"]:
                deltax -= int(self.tile_size/8)

            if "RIGHT" in self.inputs and self.inputs["RIGHT"]:
                deltax += int(self.tile_size/8)

            if "SPECIAL1" in self.inputs and self.inputs["SPECIAL1"]:
                self.dash()
            if "SPECIAL2" in self.inputs and self.inputs["SPECIAL2"]:
                self.super_jump()
            if "BLOCK" in self.inputs and self.inputs["BLOCK"]:
                deltay += 0
            if "ATTACK1" in self.inputs and self.inputs["ATTACK1"]:
                deltay += 0
            if "ATTACK2" in self.inputs and self.inputs["ATTACK2"]:
                deltay += 0
            if "ATTACK3" in self.inputs and self.inputs["ATTACK3"]:
                deltay += 0
            if "DIE" in self.inputs and self.inputs["DIE"]:
                self.dying = True

        self.movement = (deltax, deltay)
        return




class Turret(PhyisicsEntity):
    def __init__(self, game, pos, size, tilesize, xdir = 1, ydir = 0):
        super().__init__(game, "turret", pos, size, tilesize)
        self.fireCountMax = 100
        self.fireCount = self.fireCountMax
        self.xdir = xdir
        self.ydir = ydir
        self.flip = xdir < 0
        self.flip_up = ydir > xdir
        self.do_gravity = False

    def tryfire(self):
        if (self.fireCount > 0):
            return
        self.fireCount = self.fireCountMax
        self.set_actions("fire")
    
    def update(self, tilemap):

        if (self.fireCount > 0):
            self.fireCount -= 1

        if (self.actions == "idle"):
            self.tryfire()

        if (self.animations.done == True): #reset the turret
            self.game.objects.append(Bullet(self.game, self.pos, self.size, self.tile_size, self.xdir, self.ydir))
            self.set_actions("idle")

        return super().update(tilemap)

    def render(self, surf, offset=(0, 0)):
        return super().render(surf, offset)
    

class Bullet(PhyisicsEntity):
    def __init__(self, game, pos, size, tilesize, xdir = 1, ydir = 0):
        super().__init__(game, "bullet", pos, size, tilesize)
        self.velosity[0] = xdir
        self.velosity[1] = ydir
        self.do_gravity = False

    def hit(self, object):
        if (object.type == "player"):
            self.set_actions("die")
            self.velosity = (0,0)
    
    def update(self, tilemap):
        if any(self.collisions.values()):
            self.set_actions("die")
            self.velosity = (0,0)
        
        if (self.actions == "die"):
            self.dead = self.animations.done
        
        super().update(tilemap)
        

