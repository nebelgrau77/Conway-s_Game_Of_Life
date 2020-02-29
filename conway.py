'''Conway's Game of Life draft'''

from machine import Pin, SPI, I2C
import ssd1306, uos

import tinypico as TinyPICO
from micropython_dotstar import DotStar

# switch off the APA LED

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
    '''generate the new cell based on it's neighbors and the cell's initial state'''
    
    new_cell = 0
    if cell == 1:
        if neighbors in [2,3]:
            new_cell = 1 # lives        
    else:
        if neighbors == 3:
            new_cell = 1 # it takes three to give birth        
    return new_cell    


def matrix_evo(matrix, size):
    '''returns a new matrix calculated according to the rules of the Game of Life'''
    new_matrix = []
    for x in range(size):
        for y in range(size):
            items = []
            for n in [-1,0,1]:
                for m in [-1,0,1]:
                    if x + n < 0 or y + m < 0 or x + n > size - 1 or y + m > size - 1 or m == n == 0:
                        items.append(0)
                    else:
                        items.append(matrix[x+n][y+m])
                    cell = matrix[x][y]
                    neighbors = sum(items)
                    new_cell = evo(cell, neighbors)
            new_matrix.append((x,y,new_cell))
    return new_matrix


def matrix_update(matrix, new_matrix):
    '''update the previous matrix'''
    for item in new_matrix:
        matrix[item[0]][item[1]] = item[2]
    return matrix


def display_matrix(matrix, size):
    for x in range(size):
        for y in range(size):
            oled.pixel(x,y,matrix[x][y])
    oled.show()




# first matrix

matrix = [[randomcell() for _ in range(32)] for _ in range(32)]

# clean up the screen
oled.show()

display_matrix(matrix,32)


while True:
    new_matrix = matrix_evo(matrix,32)
    
    matrix = matrix_update(matrix, new_matrix)
    
    display_matrix(matrix,32)
    
