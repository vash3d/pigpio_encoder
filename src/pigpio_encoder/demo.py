from pigpio_encoder.rotary import Rotary


def rotary_callback(counter):
    print("General rotation")
    print("Counter value: ", counter)


def sw_short():
    print("Switch pressed")


def up_callback(counter):
    print("Up rotation")
    print("Counter value: ", counter)


def down_callback(counter):
    print("Down rotation")
    print("Counter value: ", counter)


def demo():
    my_rotary = Rotary(clk_gpio=13, dt_gpio=19, sw_gpio=26)
    my_rotary.setup_rotary(
            rotary_callback=rotary_callback,
            up_callback=up_callback,
            down_callback=down_callback,
            )
    my_rotary.setup_switch(sw_short_callback=sw_short)

    my_rotary.watch()


if __name__ == '__main__':
    demo()
