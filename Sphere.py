#-------------------------------------------------------------------------#
# Sphere.py - Definition of the "Sphere" class.                           #
#                                                                         #
#-------------------------------------------------------------------------#
# Author - M. Berry                                                       #
# Date   - Nov. 2023                                                      #
#-------------------------------------------------------------------------#

# import the graphics module
from graphic2 import *


# define the Sphere class
class SphereClass:

    # define the class' constructor function  
    def __init__(self):
        # set the class variables
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.radius = 5
        self.back_colour = (WHITE)
        self.x = randint(1, SCREEN_WIDTH)
        self.y = randint(1, SCREEN_HEIGHT)
        self.fill = False
        

    # define colour setter
    def set_colour(self, colour):
        # check colour parameter type and set RGB colour appropriately
        if isinstance(colour, str):
           RGB_colour = colour_lookup(colour)
        else:
           RGB_colour = colour
        self.colour = RGB_colour


    # define radius setter
    def set_radius(self, radius):
        self.radius = radius


    # define background colour setter
    def set_back_colour(self, back_colour):
        # check colour parameter type and set RGB colour appropriately
        if isinstance(back_colour, str):
           RGB_colour = colour_lookup(back_colour)
        else:
           RGB_colour = back_colour
        self.back_colour = RGB_colour


    # define x setter
    def set_x(self, x):
        self.x = x


    # define y setter
    def set_y(self, y):
        self.y = y


    # define fill setter
    def set_fill(self, fill):
        self.fill = fill


    # define colour getter
    def get_colour(self):
        return self.colour


    # define radius getter
    def get_radius(self):
        return self.radius


    # define background colour getter
    def get_back_colour(self):
        return self.back_colour

        
    # define x getter
    def get_x(self):
        return self.x


    # define y getter
    def get_y(self):
        return self.y


    # define fill getter
    def get_fill(self):
        return self.fill

    
    # define show function
    def show(self):
        # draw the circle
        if self.fill:
            drawball(self.x, self.y, self.radius, self.colour)
        else:
            drawcircle(self.x, self.y, self.radius, self.colour)

    
    # define hide function
    def hide(self):
        # draw the circle in the background colour
        if self.fill:
            drawball(self.x, self.y, self.radius, self.back_colour)
        else:
            drawcircle(self.x, self.y, self.radius, self.back_colour)

