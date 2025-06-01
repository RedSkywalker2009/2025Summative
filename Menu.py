import pygame

class Menu:

    def __init__ (self, options):
        self.fontsize = 32
        self.font = pygame.font.SysFont('segoeuiblack', self.fontsize)
        self.options = options
        self.selected = options[0]


    def draw (self, screen):
        j = 0
        for i in self.options:
            i.draw(screen, (0,j), self.font, (255, 255, 255) if i == self.selected else None )
            j = j + (self.fontsize + 2)
    
    def on_key_press(self, symbol: int, mod: int) -> bool:
        
        selectedIndex = self.options.index(self.selected)

        if (symbol == pygame.K_s) or (symbol == pygame.K_DOWN):
            selectedIndex += 1
        elif (symbol == pygame.K_w) or (symbol == pygame.K_UP):
            selectedIndex -= 1
        else:
            self.selected.on_key_press(symbol, mod)

        selectedIndex = max(0, min(selectedIndex, len(self.options) - 1))
        self.selected = self.options[selectedIndex]

        return


class Options:

    def __init__(self, name, options, value):
        self.name = name
        self.options = options
        self.value = value

    def draw (self, screen:pygame.Surface, pos, font:pygame.font, colour = None):
        colour = colour if not colour == None else (55,55,55)
        if colour == (255,255,255):
            screen.blit(font.render(self.name + ("" if self.value is None else (", " + self.value)), True, colour), pos)
        else:
            screen.blit(font.render((self.name), True, colour), pos)


    def on_key_press(self, symbol: int, mod: int) -> bool:
        
        selectedValueIndex = self.options.index(self.value)

        if (symbol == pygame.K_d) or (symbol == pygame.K_RIGHT):
            selectedValueIndex += 1
        elif (symbol == pygame.K_a) or (symbol == pygame.K_LEFT):
            selectedValueIndex -= 1

        if selectedValueIndex >= len(self.options):
            selectedValueIndex = 0
        elif selectedValueIndex < 0:
            selectedValueIndex = len(self.options) - 1
        self.value = self.options[selectedValueIndex]



class CommandOption(Options):
     def __init__(self, name, command):
         super().__init__(name, None, None)
         self.command = command   


     def on_key_press(self, symbol: int, mod: int) -> bool:
        
        if (symbol == pygame.K_RETURN or symbol == pygame.K_SPACE):
            self.command()

class Win:

    def __init__ (self, game):
        self.fontsize = 32
        self.font = pygame.font.SysFont('segoeuiblack', self.fontsize)
        self.game = game


    def draw (self, screen):
        screen.blit(self.font.render(("winner"), True, (0,0,0)), (0,0))

    
    
