import sys
import pygame


from entities import PhyisicsEntity,Player
from utils import Utils
from utils import Animations
from tilemap import Tilemap
from clouds import Clouds


class Game:

    Resolution = (1920, 1080)


    def __init__(self):

        #name the screen
        print("Hi, im initializing") 

        pygame.init()
        
        pygame.display.set_caption("plat former")
        #creating the screen and setting the size
        # consider 1920x1080
        self.screen = pygame.display.set_mode(Game.Resolution)

        self.display = pygame.Surface((Game.Resolution[0]/3, Game.Resolution[1]/3))
        #setting framerate
        self.clock = pygame.time.Clock()

        self.movement = [False,False]

        self.assets = {
            "decor" : Utils.load_images("tiles/decor"),
            "grass" : Utils.load_images("tiles/grass"),
            "large_decor" : Utils.load_images("tiles/large_decor"),
            "stone" : Utils.load_images("tiles/stone"),
            "player" : Utils.load_image("entities/player.png"),
            "clouds": Utils.load_images("clouds"),
            "player/idle" : Animations(Utils.load_images("entities/player/idle"), img_dur=6),
            "player/run" : Animations(Utils.load_images("entities/player/run"), img_dur=4),
            "player/jump" : Animations(Utils.load_images("entities/player/jump")),
            "player/slide" : Animations(Utils.load_images("entities/player/slide")),
            "player/wall_slide" : Animations(Utils.load_images("entities/player/wall_slide"))
        }

        self.clouds = Clouds(self.assets["clouds"], count = 16)
        
        self.players = {}
        for i in range(1,2):
            self.players[i] = Player(self, (50 + 10 * i, 50), (8, 15))
        
        self.scroll = [0, 0]

        self.tilemap = Tilemap(self, tile_size=16)


    def run (self):
        #game loop
        while True:
            self.display.fill((0,0,80))


            x = 0
            y = 0
            for p in self.players.values():
                x += p.rect().centerx
                y += p.rect().centery
            
            #compute the average position of the players
            x = x / len(self.players)
            y = y / len(self.players)


            self.scroll[0] += (x - self.display.get_width()/2 - self.scroll[0]) /10
            self.scroll[1] += (y - self.display.get_height()/2 - self.scroll[1]) /10

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)

            for p in self.players.values():
                p.get_inputs() #,(self.movement[1] - self.movement[0],0))

            for p in self.players.values():
                p.update(self.tilemap) #,(self.movement[1] - self.movement[0],0))

            for p in self.players.values():
                p.render(self.display, render_scroll)

            
        # set an event to close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.on_key_press(event.key, event.mod)
                if event.type == pygame.KEYUP:
                    self.on_key_release(event.key, event.mod) 
                
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
p1_inputs = {  # Look up direction based on key symbol
            pygame.K_w: "JUMP",
            pygame.K_s: "CROUCH",
            pygame.K_a: "LEFT",
            pygame.K_d: "RIGHT",
            pygame.K_e: "SPECIAL1",
            pygame.K_r: "BLOCK",
            pygame.K_q: "SPECIAL2",
            pygame.K_z: "ATTACK1",
            pygame.K_x: "ATTACK2",
            pygame.K_c: "ATTACK3"
            }
p2_inputs = {  # Look up direction based on key symbol
            pygame.K_i: "JUMP",
            pygame.K_k: "CROUCH",
            pygame.K_j: "LEFT",
            pygame.K_l: "RIGHT",
            pygame.K_u: "SPECIAL1",
            pygame.K_p: "BLOCK",
            pygame.K_o: "SPECIAL2",
            pygame.K_m: "ATTACK1",
            pygame.K_COMMA: "ATTACK2",
            pygame.K_PERIOD: "ATTACK3"
            }

g.players[1].set_inputmap(p1_inputs)
#g.players[2].set_inputmap(p2_inputs)

g.run()