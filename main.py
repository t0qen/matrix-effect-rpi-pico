"""

****** PROJECT DETAILS ********
Create Matrix effect like cmatrix on a tiny screen controlled by a Rpi Pico.


======= SCREEN COMMANDS =======

oled.fill(0) Fill with color
oled.blit(fb2, 0, 0) Show buffer
oled.show() Actualize
oled.pixel(x, y, 0) Show a pixel
oled.scroll(speed,0) ??
oled.text("string", x, y)

oled.poweroff()     # power off the oled, pixels persist in memory
oled.poweron()      # power on the oled, pixels redrawn
oled.contrast(0)    # dim
oled.contrast(255)  # bright
oled.invert(1)      # oled inverted
oled.invert(0)      # oled normal
oled.rotate(True)   # rotate 180 degrees
oled.rotate(False)  # rotate 0 degrees
oled.show()         # write the contents of the FrameBuffer to oled memory

oled.fill(0)                         # fill entire screen with colour=0
oled.pixel(0, 10)                    # get pixel at x=0, y=10
oled.pixel(0, 10, 1)                 # set pixel at x=0, y=10 to colour=1
oled.hline(0, 8, 4, 1)               # draw horizontal line x=0, y=8, width=4, colour=1
oled.vline(0, 8, 4, 1)               # draw vertical line x=0, y=8, height=4, colour=1
oled.line(0, 0, 127, 63, 1)          # draw a line from 0,0 to 127,63
oled.rect(10, 10, 107, 43, 1)        # draw a rectangle outline 10,10 to 117,53, colour=1
oled.fill_rect(10, 10, 107, 43, 1)   # draw a solid rectangle 10,10 to 117,53, colour=1
oled.text('Hello World', 0, 0, 1)    # draw some text at x=0, y=0, colour=1
oled.scroll(20, 0)                   # scroll 20 pixels to the right


+++++++ USEFUL DATA +++++++

     ←--------------- 128px ---------------→

 ↑   #######################################
 |   #######################################
 |   #######################################
64px #######################################
 |   #######################################
 |   #######################################
 ↓   #######################################

how many vertical characters : 8
 \_ horizontal : 16

"""

# librairies
from machine import Pin, I2C
from picobricks import SSD1306_I2C
import time, random

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
UPDATE_DELAY = 0.05

# we'll pick random value between these int to determinate current drop lenght
DROPS_MIN_LENGHT = 1
DROPS_MAX_LENGHT = 5

# drops is a list that contains every vertical positions of every droplets
# vertical position can vary from 0 to 63 (since height is 64)
drops = [random.randint(0, HEIGHT - 1) for _ in range(COLS)] 

# head and tail have different character sets
head_chars = ["*"]
tail_chars = list("abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*(){}[];:/?\|+<>")

while True:
    # clear the screen
    oled.fill(0)

    for i in range(COLS):
        # get horizontal position of cols, depends on CHAR_WIDTH
        x = i * CHAR_WIDTH
        # get vertical position of current drop stored in drops[]
        y = drops[i] * CHAR_HEIGHT
        
        # show head
        oled.text(random.choice(head_chars), x, y)

        # increase current drop's lenght
        drops[i] += 1

        # if current drop touches edge of the screen
        if drops[i] * CHAR_HEIGHT > (HEIGHT + DROPS_MAX_LENGHT * CHAR_HEIGHT):
            # reset current drop, multiple of CHAR_HEIGHT
            drops[i] = n = random.randint(0, 4) * CHAR_HEIGHT


    # finally show result by updating screen
    oled.show()
    time.sleep(UPDATE_DELAY)


