#imports
import sys
import pygame


from entities import PhyisicsEntity,Player, Turret, Scroll
from utils import Utils
from utils import Animations
from tilemap import Tilemap
from clouds import Clouds
from Menu import Menu, Options, CommandOption,Win, PlayerStats



class Game:

    #setting reselution and size of everything
    Resolution = (1920, 1080)
    tile_size = 16
    player_size = (12, 18)
    bullet_size = (12, 12)
    player_stats = (60, 30)

    xIncx = {
        "Easy" : 0,
        "Medium" : 1,
        "Hard" : 0.3,
        "Impossible": 1.5
    }

    bullet_speed = {
        "Easy" : 0.7,
        "Medium" : 1,
        "Hard" : 1,
        "Impossible": 1.5
    }

    turret_speed = {
        "Easy" : 200,
        "Medium" : 200,
        "Hard" : 200,
        "Impossible": 400
    }
    
    level_map = {
        "Easy" : "easy.json",
        "Medium" : "easy.json",
        "Hard" : "hard.json",
        "Impossible": "hard.json"
    }

    players_num = {
        "1 Player" : 1,
        "2 Players" : 2,
        "3 Players" : 3
    }

    def player_screen_pos(self, i):
        if (i == 1):
            return (0,0)
        if (i == 2):
            return (self.screen_width - self.player_stats[0], 0)
        if (i == 3):
            return (self.screen_width - self.player_stats[0], self.screen_height - self.player_stats[1])
        return (0, 0)

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("2025 Summative")
        #creating the screen and setting the size
        # consider 1920x1080
        self.screen = pygame.display.set_mode(Game.Resolution)

        self.screen_width = Game.tile_size * 42
        self.screen_height = (Game.Resolution[1]/Game.Resolution[0]) * self.screen_width
        self.display = pygame.Surface( (self.screen_width, int(self.screen_height)) )
        #setting framerate
        self.clock = pygame.time.Clock()
        self.tilemap = Tilemap(self, Game.tile_size)
        self.movement = [False,False]
        self.p_inputs = {}
        self.config = {}
        self.winner = False
        self.players = {}
        self.player_screen = {}
        self.objects = []
        self.draw_hitbox = False
        
        #load assets
        self.assets = {
            "decor" : Utils.load_images("tiles/decor", (Game.tile_size, Game.tile_size)),
            "grass" : Utils.load_images("tiles/grass",(Game.tile_size, Game.tile_size)),
            "large_decor" : Utils.load_images("tiles/large_decor", scale= Game.tile_size/16),
            "stone" : Utils.load_images("tiles/stone",(Game.tile_size, Game.tile_size)),
            "player" : Utils.load_image("entities/player.png",(Game.tile_size, Game.tile_size)),
            "clouds": Utils.load_images("clouds", scale= Game.tile_size/16),
            "turret": Utils.load_images("tiles/turret", Game.player_size),
            "player/idle" : Animations(Utils.load_images("entities/player/idle",Game.player_size), img_dur=6),
            "player/die" : Animations(Utils.load_images("entities/player/die",Game.player_size), loop=False),
            "player/run" : Animations(Utils.load_images("entities/player/run",Game.player_size), img_dur=4),
            "player/jump" : Animations(Utils.load_images("entities/player/jump",Game.player_size)),
            "player/slide" : Animations(Utils.load_images("entities/player/slide",Game.player_size)),
            "player/wall_slide" : Animations(Utils.load_images("entities/player/wall_slide",Game.player_size)),
            "turret/idle" : Animations(Utils.load_images("entities/turret/idle",Game.player_size)),
            "turret/fire" : Animations(Utils.load_images("entities/turret/fire",Game.player_size), loop=False),
            "bullet/idle" : Animations(Utils.load_images("entities/bullet/idle",Game.bullet_size)),
            "bullet/die" : Animations(Utils.load_images("entities/bullet/die",Game.bullet_size), loop=False),
            "scroll/idle" : Animations(Utils.load_images("entities/scroll/idle",(Game.tile_size, Game.tile_size))),
            "scroll/die" : Animations(Utils.load_images("entities/scroll/die",(Game.tile_size, Game.tile_size)), loop=False),
            "Titlescreen" : Animations(Utils.load_images("Titlescreen", size = (250, 250))),
            "Winscreen" : Animations(Utils.load_images("Winscreen", size = (250, 250))),
            "Controlscreen" : Animations(Utils.load_images("Controlscreen", size = (500, 300))),
            "Defeatscreen" : Animations(Utils.load_images("Defeatscreen", size = (250, 250))),
            "playerstats" : Animations(Utils.load_images("PlayerStats", size = self.player_stats))

        }

        self.isMenuOpen = False
        self.isControlsOpen = True
        #set options for menu
        self.menu = Menu([Options("Difficulty", ["Easy", "Medium", "Hard", "Impossible"], "Easy"), Options("Players", ["1 Player", "2 Players", "3 Players"], "1 Player"), CommandOption("Show Controls", self.ShowControls), CommandOption("Restart", self.Save), CommandOption("Quit", self.Quit)], self.assets["Titlescreen"])
        self.Save(False)
        #creat images,screens and amount (for clouds)
        self.clouds = Clouds(self.assets["clouds"], count = 60)
        self.winscreen = Win(self, self.assets["Winscreen"])
        self.defeatscreen = Win(self, self.assets["Defeatscreen"])
        self.controlscreen = Win(self, self.assets["Controlscreen"])

    #Convert image scale (16) to tile scale. World Coordinates
    def scale(self, value):
        return value * self.tile_size/16

    #prepare tilemap
    def prep_tilemap(self):

        
        delete_keys = []
        delete_list = []

        for i_key in self.tilemap.tilemap.keys():
            i = self.tilemap.tilemap[i_key]
            if i["type"] == "turret":
                xdir = 1 if (i["variant"] == 0 or i["variant"] == 5 or i["variant"] == 6) else -1 if (i["variant"] == 1 or i["variant"] == 4 or i["variant"] == 7) else 0 
                ydir = 1 if (i["variant"] == 3 or i["variant"] == 4 or i["variant"] == 5) else -1 if (i["variant"] == 2 or i["variant"] == 6 or i["variant"] == 7) else 0 
                self.objects.append(Turret(self, (i["pos"][0] * self.tile_size, i["pos"][1] * self.tile_size), self.player_size, self.tile_size, xdir * Game.bullet_speed[self.config.get("Difficulty", "Easy")], ydir * Game.bullet_speed[self.config.get("Difficulty", "Easy")], Game.turret_speed[self.config.get("Difficulty", "Easy")]))
                delete_keys.append(i_key)

            if i["type"] == "scroll":
                self.objects.append(Scroll(self, (i["pos"][0] * self.tile_size, i["pos"][1] * self.tile_size), self.player_size, self.tile_size))
                delete_keys.append(i_key)

        for i in self.tilemap.offgrid_tiles:
            if i["type"] == "turret":
                xdir = 1 if (i["variant"] == 0 or i["variant"] == 5 or i["variant"] == 6) else -1 if (i["variant"] == 1 or i["variant"] == 4 or i["variant"] == 7) else 0 
                ydir = 1 if (i["variant"] == 3 or i["variant"] == 4 or i["variant"] == 5) else -1 if (i["variant"] == 2 or i["variant"] == 6 or i["variant"] == 7) else 0 
                self.objects.append(Turret(self, (i["pos"][0], i["pos"][1]), self.player_size, self.tile_size, xdir * Game.bullet_speed[self.config.get("Difficulty", "Easy")], ydir * Game.bullet_speed[self.config.get("Difficulty", "Easy")], Game.turret_speed[self.config.get("Difficulty", "Easy")]))
                delete_list.append(i)

            if i["type"] == "scroll":
                self.objects.append(Scroll(self, (i["pos"][0], i["pos"][1]), self.player_size, self.tile_size))
                delete_list.append(i)    


        #cleanup
        for key in delete_keys:
            del self.tilemap.tilemap[key]

        for v in delete_list:
            if v in delete_list:
                self.tilemap.offgrid_tiles.remove(v)
            


    def LoadLevel(self):
        self.players = {}
        self.player_screen = {}
        self.objects = []
        for i in range(1, Game.players_num[self.config.get("Players", "1 Player")] + 1):
            self.players[i] = Player(self, i, (self.scale(200 + 10 * i), self.scale(330)), self.player_size, self.tile_size)
            self.player_screen[i] = PlayerStats(self, self.assets["playerstats"], self.assets["scroll/die"], self.players[i] )

        for p in self.players.values():
            p.set_inputmap(self.p_inputs[p.id])

        self.tilemap.load("data/maps/" + Game.level_map[self.config.get("Difficulty", "Easy")])

        self.prep_tilemap()

        self.scroll = [0, 0]
        self.minx = 0
        self.miny = self.scale(550)
        self.finishline = self.scale(1940)
        self.winner = False
        

    def ShowControls(self):
        self.isControlsOpen = True
        self.isMenuOpen = False
        
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
        return self.winner or self.isMenuOpen or self.isControlsOpen


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
                    p.winner = True
            
            # check if all players are either done or dead
            win = True
            for p in self.players.values():
                if not (p.winner or p.dead):
                    win = False
            self.winner = win
            
            #compute the average position of the players
            if (num_players > 0):
                x = x / num_players
                y = y / num_players
                self.scroll[0] += (x - self.display.get_width()/2 - self.scroll[0]) /10
                self.scroll[1] += (y - self.display.get_height()/2 - self.scroll[1]) /10


            render_scroll = (max(int(self.minx), int(self.scroll[0])), min(int(self.scroll[1]), int(self.miny)))
            
            if (not self.isPaused()):
                if (num_players > 0):
                    self.minx += self.scale(Game.xIncx[self.config.get("Difficulty", "Easy")])

            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)

            if (self.isPaused() == False):
                # Get player inputs
                
                for p in self.players.values():
                    if p.dead or p.dying:
                        continue
                    p.get_inputs()

                # Update Players
                for p in self.players.values():
                    if p.dead:
                        continue
                    p.update(self.tilemap) 

                # Update Objects
                for o in self.objects:
                    if o.dead:
                        continue
                    o.update(self.tilemap)
                    #Check Object/Player Collisions
                    for p in self.players.values():
                        if p.dead:
                            continue
                        o.checkCollision(p)
                
            objectset = self.objects
            for o in objectset:
                if o.dead:
                    self.objects.remove(o)
                    continue
                o.render(self.display, render_scroll) 
                
            #Draw the menu under the players
            
            if (self.isPaused()):
                if (self.isMenuOpen):
                    self.menu.draw(self.display)
                elif (self.isControlsOpen):
                    self.controlscreen.draw(self.display)
                elif (self.winner):
                    if any(p.winner == True for p in self.players.values()):
                        self.winscreen.draw(self.display)
                    else:
                        self.defeatscreen.draw(self.display)



            for p in self.players.values():
                if p.dead:
                    continue
                p.render(self.display, render_scroll)

            
            for i in self.players.keys():
                self.player_screen[i].draw(self.display, self.player_screen_pos(i))

            
        # set an event to close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.Quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.isMenuOpen = True if not (self.isMenuOpen or self.isControlsOpen) else False
                    self.isControlsOpen = False

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
            pygame.K_q: "SPECIAL2"
            }
g.p_inputs[2] = {  # Look up direction based on key symbol
            pygame.K_i: "JUMP",
            pygame.K_j: "LEFT",
            pygame.K_l: "RIGHT",
            pygame.K_o: "SPECIAL1",
            pygame.K_u: "SPECIAL2"
            }
g.p_inputs[3] = {  # Look up direction based on key symbol
            pygame.K_UP: "JUMP",
            pygame.K_LEFT: "LEFT",
            pygame.K_RIGHT: "RIGHT",
            pygame.K_RCTRL: "SPECIAL1",
            pygame.K_RSHIFT: "SPECIAL2"
            }
            
g.LoadLevel()

g.run()