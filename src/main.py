from pigpio_encoder import Rotary

def rotary_callback(counter):
    print("Counter value: ", counter)

def sw_short():
    print("Switch pressed")

def up_callback():
    print("Up rotation")

def down_callback():
    print("Down rotation")

my_rotary = Rotary(clk_gpio=27, dt_gpio=22, sw_gpio=17)
my_rotary.setup_rotary(
        rotary_callback=rotary_callback,
        up_callback=up_callback,
        down_callback=down_callback,
        )
my_rotary.setup_switch(sw_short_callback=sw_short)

my_rotary.watch()

