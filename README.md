# Conway-s_Game_Of_Life

Very slow, naive approach to Conway's Game of Life on ESP32 with MicroPython

It follows the rules of the game as described here: https://en.wikipedia.org/wiki/Conway's_Game_of_Life
and here: http://rosettacode.org/wiki/Conway's_Game_of_Life

At the moment it will recycle after 999 generations, which seems a lot for the size of the board (32x32).

It starts with a randomly generated white noise pattern, which slowly dissolves.

