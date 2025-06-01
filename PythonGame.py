import sys
import pygame


from entities import PhyisicsEntity,Player
from utils import Utils
from utils import Animations
from tilemap import Tilemap
from clouds import Clouds
from Menu import Menu, Options, CommandOption,Win


class Game:

    Resolution = (1920, 1080)
    

    xIncx = {
        "Easy" : 0,
        "Medium" : 1,
        "Hard" : 1.9
    }

    players_num = {
        "1 Player" : 1,
        "2 Players" : 2,
        "3 Players" : 3
    }

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("plat former")
        #creating the screen and setting the size
        # consider 1920x1080
        self.screen = pygame.display.set_mode(Game.Resolution)

        self.display = pygame.Surface((Game.Resolution[0]/3, Game.Resolution[1]/3))
        #setting framerate
        self.clock = pygame.time.Clock()
        self.tilemap = Tilemap(self, tile_size=16)
        self.movement = [False,False]
        self.p_inputs = {}
        self.config = {}
        self.winner = False
        self.winscreen = Win(self)

        self.assets = {
            "decor" : Utils.load_images("tiles/decor"),
            "grass" : Utils.load_images("tiles/grass"),
            "large_decor" : Utils.load_images("tiles/large_decor"),
            "stone" : Utils.load_images("tiles/stone"),
            "player" : Utils.load_image("entities/player.png"),
            "clouds": Utils.load_images("clouds"),
            "player/idle" : Animations(Utils.load_images("entities/player/idle"), img_dur=6),
            "player/die" : Animations(Utils.load_images("entities/player/die"), loop=False),
            "player/run" : Animations(Utils.load_images("entities/player/run"), img_dur=4),
            "player/jump" : Animations(Utils.load_images("entities/player/jump")),
            "player/slide" : Animations(Utils.load_images("entities/player/slide")),
            "player/wall_slide" : Animations(Utils.load_images("entities/player/wall_slide"))
        }

        self.isMenuOpen = False
        self.menu = Menu([Options("Difficulty", ["Easy", "Medium", "Hard"], "Easy"), Options("Players", ["1 Player", "2 Players", "3 Players"], "1 Player"), CommandOption("Save", self.Save), CommandOption("Quit", self.Quit)])
        self.Save(False)
        self.clouds = Clouds(self.assets["clouds"], count = 60)
        



    def LoadLevel(self):
        self.players = {}
        for i in range(1, Game.players_num[self.config.get("Players", "1 Player")] + 1):
            self.players[i] = Player(self, i, (200 + 10 * i, 330), (8, 15))

        for p in self.players.values():
            p.set_inputmap(self.p_inputs[p.id])

        self.tilemap.load("map.json")
        self.scroll = [0, 0]
        self.minx = 0
        self.miny = 380
        self.finishline = 1228
        self.winner = False

        
    def Save(self, reloadLevel = True):
        self.config = {}
        for p in self.menu.options:
            self.config[p.name] = p.value

        if (reloadLevel):
            self.LoadLevel()

    def Quit(self):
         pygame.quit()
         sys.exit()
        

    def isPaused(self):
        return self.winner or self.isMenuOpen


    def run (self):
        #game loop
        while True:
            self.display.fill((0,0,80))

            x = 0
            y = 0
            num_players = 0
            for p in self.players.values():
                if p.dead:
                    continue
                if (p.rect().centerx < self.minx or p.rect().centery > self.miny):
                    p.dying = True
                num_players += 1
                x += p.rect().centerx
                y += p.rect().centery
                if (p.rect().centerx > self.finishline):
                    self.winner = True
            
            #compute the average position of the players
            if (num_players > 0):
                x = x / num_players
                y = y / num_players
                self.scroll[0] += (x - self.display.get_width()/2 - self.scroll[0]) /10
                self.scroll[1] += (y - self.display.get_height()/2 - self.scroll[1]) /10



            render_scroll = (max(int(self.minx), int(self.scroll[0])), min(int(self.scroll[1]), int(self.miny)))
            
            if (not self.isPaused()):
                if (num_players > 0):
                    self.minx += Game.xIncx[self.config.get("Difficulty", "Easy")]

            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)

            if (self.isPaused() == False):
                for p in self.players.values():
                    if p.dead or p.dying:
                        continue
                    p.get_inputs() #,(self.movement[1] - self.movement[0],0)

                for p in self.players.values():
                    if p.dead:
                        continue
                    p.update(self.tilemap) #,(self.movement[1] - self.movement[0],0))
            elif(self.isMenuOpen):
                self.menu.draw(self.display)
            elif (self.winner):
                self.winscreen.draw(self.display)
                

            for p in self.players.values():
                if p.dead:
                    continue
                p.render(self.display, render_scroll)

            
        # set an event to close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.Quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.isMenuOpen = True if not self.isMenuOpen else False

                if (not self.isMenuOpen):
                   if event.type == pygame.KEYDOWN:
                        self.on_key_press(event.key, event.mod)
                   if event.type == pygame.KEYUP:
                        self.on_key_release(event.key, event.mod)
                else:
                    if event.type == pygame.KEYDOWN:
                        self.menu.on_key_press(event.key, event.mod) 
                
            
                
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()) ,(0,0))

            #tell the game to update 
            pygame.display.update()
            # a sleep untill 60fps is maintained
            self.clock.tick(60)
    
    def on_key_press(self, symbol: int, mod: int) -> bool:
        for p in self.players.values():
            p.on_key_press(symbol, mod)
        


    def on_key_release(self, symbol: int, mod: int) -> bool:
        for p in self.players.values():
            p.on_key_release(symbol, mod)


g = Game()

g.p_inputs[1] = {  # Look up direction based on key symbol
            pygame.K_w: "JUMP",
            pygame.K_s: "CROUCH",
            pygame.K_a: "LEFT",
            pygame.K_d: "RIGHT",
            pygame.K_e: "SPECIAL1",
            pygame.K_r: "BLOCK",
            pygame.K_q: "SPECIAL2",
            pygame.K_z: "ATTACK1",
            pygame.K_x: "ATTACK2",
            pygame.K_c: "ATTACK3",
            pygame.K_y: "DIE",
            pygame.CONTROLLER_BUTTON_DPAD_LEFT: "LEFT",
            pygame.CONTROLLER_BUTTON_DPAD_LEFT: "RIGHT",
            pygame.CONTROLLER_BUTTON_A: "JUMP",
            pygame.CONTROLLER_BUTTON_LEFTSHOULDER: "SPECIAL1",
            pygame.CONTROLLER_BUTTON_RIGHTSHOULDER: "SPECIAL2",
            }
g.p_inputs[2] = {  # Look up direction based on key symbol
            pygame.K_i: "JUMP",
            pygame.K_k: "CROUCH",
            pygame.K_j: "LEFT",
            pygame.K_l: "RIGHT",
            pygame.K_u: "SPECIAL1",
            pygame.K_p: "BLOCK",
            pygame.K_o: "SPECIAL2",
            pygame.K_m: "ATTACK1",
            pygame.K_COMMA: "ATTACK2",
            pygame.K_PERIOD: "ATTACK3",
            pygame.CONTROLLER_BUTTON_DPAD_LEFT: "LEFT",
            pygame.CONTROLLER_BUTTON_DPAD_LEFT: "RIGHT",
            pygame.CONTROLLER_BUTTON_A: "JUMP",
            pygame.CONTROLLER_BUTTON_LEFTSHOULDER: "SPECIAL1",
            pygame.CONTROLLER_BUTTON_RIGHTSHOULDER: "SPECIAL2",
            }
g.p_inputs[3] = {  # Look up direction based on key symbol
            pygame.CONTROLLER_BUTTON_DPAD_LEFT: "LEFT",
            pygame.CONTROLLER_BUTTON_DPAD_LEFT: "RIGHT",
            pygame.CONTROLLER_BUTTON_A: "JUMP",
            pygame.CONTROLLER_BUTTON_LEFTSHOULDER: "SPECIAL1",
            pygame.CONTROLLER_BUTTON_RIGHTSHOULDER: "SPECIAL2",
            }
g.p_inputs[4] = {  # Look up direction based on key symbol
            pygame.CONTROLLER_BUTTON_DPAD_LEFT: "LEFT",
            pygame.CONTROLLER_BUTTON_DPAD_LEFT: "RIGHT",
            pygame.CONTROLLER_BUTTON_A: "JUMP",
            pygame.CONTROLLER_BUTTON_LEFTSHOULDER: "SPECIAL1",
            pygame.CONTROLLER_BUTTON_RIGHTSHOULDER: "SPECIAL2",
            }
            
g.LoadLevel()

g.run()