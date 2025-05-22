#-------------------------------------------------------------------------#
# graphic2.py - MDHS implementation of graphics commands                  #
#               for use by students, using PyGame                         #
#-------------------------------------------------------------------------#
# Author - M. Berry                                                       #
# Date   - Sept. 1/2023                                                   #
#-------------------------------------------------------------------------#
# Input  - parameters for various graphics functions                      #
# Output - various graphics shapes                                        #
#-------------------------------------------------------------------------#

# import the PyGame and other modules
import pygame
import math
from time import *
from random import *


# import pygame.locals for easier
# access to key coordinates
from pygame.locals import *


# set screen dimensions, text font and line thickness
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400
LINE_THICKNESS = 1


# define colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
LIME = (191,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (128,0,128)
SILVER = (192,192,192)
GREY = (128,128,128)
MAROON = (128,0,0)
OLIVE = (128,128,0)
GREEN = (0,255,0)
PURPLE = (255,0,255)
PINK = (255,192,203)
TEAL = (0,128,128)
BROWN = (150,75,0)
ORANGE = (255,69,0)
NAVY = (0,0,128)


# define a function to initialise the PyGame screen
def setscreen():
    # allow the PyGame screen to be accessed globally
    global DISPLAY
    DISPLAY = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
    cls()


# define a function to clear the screen
def cls():
    # force PyGame to internally interact with the OS
    pygame.event.pump()

    DISPLAY.fill(WHITE)
    pygame.display.update()


# define a function to change the background colour
def background(colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()

    DISPLAY.fill(colour)
    pygame.display.update()


# colour lookup function to convert string colours to tuples
def colour_lookup(colour):
    if colour.upper() == "BLACK":
        return (0,0,0)
    elif colour.upper() == "WHITE":
        return (255,255,255)
    elif colour.upper() == "RED":
        return (255,0,0)
    elif colour.upper() == "LIME":
        return (191,255,0)
    elif colour.upper() == "BLUE":
        return (0,0,255)
    elif colour.upper() == "YELLOW":
        return (255,255,0)
    elif colour.upper() == "CYAN":
        return (0,255,255)
    elif colour.upper() == "MAGENTA":
        return (128,0,128)
    elif colour.upper() == "SILVER":
        return (192,192,192)
    elif colour.upper() == "GREY":
        return (128,128,128)
    elif colour.upper() == "MAROON":
        return (128,0,0)
    elif colour.upper() == "OLIVE":
        return (128,128,0)
    elif colour.upper() == "GREEN":
        return (0,255,0)
    elif colour.upper() == "PURPLE":
        return (255,0,255)
    elif colour.upper() == "PINK":
        return (255,192,203)
    elif colour.upper() == "TEAL":
        return (0,128,128)
    elif colour.upper() == "BROWN":
        return (150,75,0)
    elif colour.upper() == "ORANGE":
        return (255,69,0)
    elif colour.upper() == "NAVY":
        return (0,0,128)
    else:
        return (0,0,0)


# draw a circle outline
def drawcircle(x, y, radius, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()

    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # draw the circle   
    pygame.draw.circle(DISPLAY, RGB_colour, (x, SCREEN_HEIGHT - y), radius, LINE_THICKNESS)
    pygame.display.update()

    
# draw a filled circle    
def drawball(x, y, radius, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()
    
    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # draw the circle   
    pygame.draw.circle(DISPLAY, RGB_colour, (x, SCREEN_HEIGHT - y), radius)
    pygame.display.update()


# draw an unfilled oval    
def drawoval(x, y, x_radius, y_radius, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()
    
    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # draw the oval
    pygame.draw.ellipse(DISPLAY, RGB_colour, (x - x_radius, SCREEN_HEIGHT - y - y_radius, 2 * x_radius, 2 * y_radius), LINE_THICKNESS)
    pygame.display.update()

    
# draw a filled oval    
def drawfilloval(x, y, x_radius, y_radius, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()
    
    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # draw the oval
    pygame.draw.ellipse(DISPLAY, RGB_colour, (x - x_radius, SCREEN_HEIGHT - y - y_radius, 2 * x_radius, 2 * y_radius))
    pygame.display.update()


# draw a box
def drawbox(x_bottom_left, y_bottom_left, x_top_right, y_top_right, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()
    
    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # draw the box
    pygame.draw.rect(DISPLAY, RGB_colour, (x_bottom_left, SCREEN_HEIGHT - y_top_right, x_top_right - x_bottom_left, y_top_right - y_bottom_left), LINE_THICKNESS)
    pygame.display.update()


# draw a filled box
def drawfillbox(x_bottom_left, y_bottom_left, x_top_right, y_top_right, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()
    
    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # draw the box
    pygame.draw.rect(DISPLAY, RGB_colour, (x_bottom_left, SCREEN_HEIGHT - y_top_right, x_top_right - x_bottom_left, y_top_right - y_bottom_left))
    pygame.display.update()

# draw a line
def drawline(x1, y1, x2, y2, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()
    
    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # draw the line
    pygame.draw.line(DISPLAY, RGB_colour, (x1, SCREEN_HEIGHT - y1), (x2, SCREEN_HEIGHT - y2))
    pygame.display.update()


# draw a dot
def drawdot(x, y, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()
    
    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # draw the dot    
    pygame.draw.circle(DISPLAY, RGB_colour, (x, SCREEN_HEIGHT - y), 1)
    pygame.display.update()


# draw an arc
def drawarc(x, y, x_radius, y_radius, start_angle, end_angle, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()
    
    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # draw the arc    
    pygame.draw.arc(DISPLAY, RGB_colour, (x - x_radius, SCREEN_HEIGHT - y - y_radius, 2 * x_radius, 2 * y_radius), math.radians(start_angle), math.radians(end_angle), LINE_THICKNESS)
    pygame.display.update()


# draw a triangle
def drawtriangle(x1, y1, x2, y2, x3, y3, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()
    
    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # draw the triangle    
    pygame.draw.polygon(DISPLAY, RGB_colour, ((x1, SCREEN_HEIGHT - y1), (x2, SCREEN_HEIGHT - y2), (x3, SCREEN_HEIGHT - y3)))
    pygame.display.update()

    
# draw a quadrilateral
def drawquad(x1, y1, x2, y2, x3, y3, x4, y4, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()
    
    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # draw the quadrilateral
    pygame.draw.polygon(DISPLAY, RGB_colour, ((x1, SCREEN_HEIGHT - y1), (x2, SCREEN_HEIGHT - y2), (x3, SCREEN_HEIGHT - y3), (x4, SCREEN_HEIGHT - y4)))
    pygame.display.update()


# define a function to print a message on the screen
def drawstring(message, x, y, colour):
    # force PyGame to internally interact with the OS
    pygame.event.pump()
    
    # check colour parameter type and set RGB colour appropriately
    if isinstance(colour, str):
        RGB_colour = colour_lookup(colour)
    else:
        RGB_colour = colour

    # print the message
    pygame.font.init()
    TEXT_FONT = pygame.font.SysFont("Courier New", 10)

    image = TEXT_FONT.render(message, True, RGB_colour)
    DISPLAY.blit(image, (x, SCREEN_HEIGHT - y))
    pygame.display.update()


# define a function to check for key-pressed events
def hasch():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return True

    
# define a function to allow PyGame window to close
def endscreen():
    run = True  # flag to continue loop

    while run:  # loop to await close button press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()




