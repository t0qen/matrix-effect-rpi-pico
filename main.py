"""
****** PROJECT DETAILS ********
Create Matrix rain like cmatrix on a tiny screen controlled by a Rpi Pico.

"""

from machine import Pin, I2C
from picobricks import SSD1306_I2C
import time
import random

i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

WIDTH = 128
HEIGHT = 64
CHAR_WIDTH = 8
CHAR_HEIGHT = 8
COLS = WIDTH // CHAR_WIDTH
UPDATE_DELAY = 0.001
DROPS_MIN_LENGHT = 1
DROPS_MAX_LENGHT = 4

head_chars = ["*"]
tail_chars = list("abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*(){}[];:/?\|+<>")

def shuffle(lst):
    n = len(lst)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]

drops = list(range(-16, 0, 2))
shuffle(drops)

current_new_coord = list(range(-16, 0, 2))
shuffle(current_new_coord)

current_tail_lenght = [random.randint(DROPS_MIN_LENGHT + 1, DROPS_MAX_LENGHT) for _ in range(COLS)]

oled.contrast(0)

while True:
    oled.fill(0)
    
    for i in range(COLS / 2):
        x = i * CHAR_WIDTH * 2
        y = drops[i] * CHAR_HEIGHT
        
        oled.text(random.choice(head_chars), x, y)
        
        for a in range(DROPS_MIN_LENGHT, current_tail_lenght[i]):
            tail_y = y - a * CHAR_HEIGHT
            oled.text(random.choice(tail_chars), x, tail_y)

        drops[i] += 1

        if drops[i] * CHAR_HEIGHT > (HEIGHT + DROPS_MAX_LENGHT * CHAR_HEIGHT):
            drops[i] = current_new_coord[i] 
            current_tail_lenght[i] = random.randint(DROPS_MIN_LENGHT + 1, DROPS_MAX_LENGHT)

    oled.show()
    time.sleep(UPDATE_DELAY)