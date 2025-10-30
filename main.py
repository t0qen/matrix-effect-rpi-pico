"""

****** PROJECT DETAILS ********
Create Matrix rain like cmatrix on a tiny screen controlled by a Rpi Pico.

"""


# librairies
from machine import Pin, I2C
from picobricks import SSD1306_I2C
import time
import random

# pins
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

# const vars
WIDTH = 128
HEIGHT = 64
CHAR_WIDTH = 8
CHAR_HEIGHT = 8
COLS = WIDTH // CHAR_WIDTH
# may influence fps and drops's spe
UPDATE_DELAY = 0.005

# we'll pick random value between these int to determinate current drop lenght
DROPS_MIN_LENGHT = 1
DROPS_MAX_LENGHT = 6

drops = [random.randint(-(int(HEIGHT/2)), 0) for _ in range(COLS)] 
current_tail_lenght = [random.randint(DROPS_MIN_LENGHT + 1, DROPS_MAX_LENGHT) for _ in range(COLS)]

# head and tail have different character sets
head_chars = ["*"]
tail_chars = list("abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*(){}[];:/?\|+<>")


while True:
    # clear the screen
    oled.fill(0)
    #shuffle(drops_preset)

    
    for i in range(COLS / 2):
        # get horizontal position of cols, depends on CHAR_WIDTH
        x = i * CHAR_WIDTH * 2
        # get vertical position of current drop stored in drops[]
        y = drops[i] * CHAR_HEIGHT
        
        # show head
        oled.text(random.choice(head_chars), x, y)
        
        for a in range(DROPS_MIN_LENGHT, current_tail_lenght[i]):
            tail_y = y - a * CHAR_HEIGHT
            oled.text(random.choice(tail_chars), x, tail_y)

            
        # increase current drop's lenght
        drops[i] += 1

        # if current drop touches edge of the screen
        if drops[i] * CHAR_HEIGHT > (HEIGHT + DROPS_MAX_LENGHT * CHAR_HEIGHT):
            # reset current drop, multiple of CHAR_HEIGHT
            drops[i] = random.randint(-int(HEIGHT/8), 0) * CHAR_HEIGHT
            current_tail_lenght[i] = random.randint(DROPS_MIN_LENGHT + 1, DROPS_MAX_LENGHT)


    # finally show result by updating screen
    oled.show()
    time.sleep(UPDATE_DELAY)



