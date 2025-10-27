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
import time

# pin initialization
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

# vars
HORIZ_LENGHT = 128
VERT_LENGHT = 64
CHARA_SIZE_Y = 7 # vertical lenght of a character
CHARA_SIZE_X = 7 # horizontal lenght of a character
NB_COL = 16 # how many colones are there : 1, 2, ...
NB_LINES = 8 # how many lines are there : 1, 2, ...

def make_droplet(line, col, lenght):
    y = int(col * (HORIZ_LENGHT / NB_COL)) # determinate y coord of chosen col
    x = line # begin at 0
    for i in range(lenght):
        write_chara("1", x, y)
        y = y + 1 + CHARA_SIZE_Y
        update_screen()

        time.sleep(0.5)

    # where we will remove a chara
    y1 = int(col * (HORIZ_LENGHT / NB_COL))
    x1 = line
    # where we will write a new chara
    y2 = int(lenght * (HORIZ_LENGHT / NB_COL)) + 1 + CHARA_SIZE_Y
    x2 = line 
    for i in range(NB_COL):
        write_chara("1", x2, y2)
        y2 = y2 + 1 + CHARA_SIZE_Y
        print("y2 ", y2)
        oled.fill_rect(x1, y1, 8, 8, 0)
        y1 = y1 + 1 + CHARA_SIZE_Y
        print("y1 ", y1)
        update_screen()
        time.sleep(0.5)

def update_droplets():
    pass

def write_chara(text, line, col):
    oled.text(text, line, col)

def update_screen():
    oled.show()


make_droplet(0, 1, 6)

update_screen()
#
























