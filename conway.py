# Conway's Game of Life draft
#
# by: nebelgrau77 
#  
# as described here: https://en.wikipedia.org/wiki/Conway's_Game_of_Life
#
# written for ESP32 boards: will not run on ESP8266 due to memory constraints
#
# simple algorithm used for calculation of neighbours at the borders of the field
# cells beyond the array boundaries are considered to be 0 (no wrapping)
# 
# currenty will restart after 1000 generations
# 

from machine import Pin, SPI, I2C
import ssd1306, uos

import tinypico as TinyPICO
from micropython_dotstar import DotStar

# switch off the APA LED on the TinyPICO
# to be omitted for other ESP32 boards

spi = SPI(sck = Pin(TinyPICO.DOTSTAR_CLK), mosi = Pin(TinyPICO.DOTSTAR_DATA), miso = Pin(TinyPICO.SPI_MISO))
dotstar = DotStar(spi, 1, brightness = 0)
TinyPICO.set_dotstar_power(False)

# display setup

i2c = I2C(scl=Pin(21), sda=Pin(22))
oled = ssd1306.SSD1306_I2C(128,32,i2c,0x3c)

# helper functions

def randomcell():
    '''generate random 1s and 0s'''
    return uos.urandom(1)[0]%2

def evo(cell, neighbors):
    '''generate the new cell based on its neighbors and the cell's initial state'''
    
    new_cell = 0
    if cell == 1:
        if neighbors in [2,3]:
            new_cell = 1 # lives        
    else:
        if neighbors == 3:
            new_cell = 1 # it takes three to give birth        
    return new_cell    


def matrix_evo(matrix, size):
    #returns a new matrix calculated according to the rules of the Game of Life
    new_matrix = [[0 for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            neighbors = 0 
            for n in [-1,0,1]:
                for m in [-1,0,1]:
                    if x + n < 0 or y + m < 0 or x + n > size - 1 or y + m > size - 1 or m == n == 0:
                        pass
                    else:
                        neighbors = neighbors + matrix[x+n][y+m]
                    
                    cell = matrix[x][y]
                    new_cell = evo(cell, neighbors)
            new_matrix[x][y] = new_cell
    return new_matrix


def display_matrix(matrix, size):
    '''prepare the matrix to be displayed'''
    for x in range(size):
        for y in range(size):
            oled.pixel(x,y,matrix[x][y])
    


def display_info(gen):
    oled.text("GameOfLife", 48, 0,1)
    oled.fill_rect(64,25,64,8,0) # clean up the counter
    oled.text("Gen:   {:03d}".format(gen), 48,25,1)


# clean up the screen

oled.fill(0)
oled.show()

while True:

    gen = 0
    
    # first matrix
    matrix = [[randomcell() for _ in range(32)] for _ in range(32)]

    display_info(gen)

    display_matrix(matrix,32)

    oled.show()

    while gen < 1000:
        
        gen = gen + 1
        
        matrix = matrix_evo(matrix,64)

        display_matrix(matrix,64)
        
        display_info(gen)

        oled.show()
