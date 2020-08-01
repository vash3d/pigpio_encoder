import unittest
from unittest.mock import patch, Mock

import sys
sys.modules['pigpio'] = 'huhu'

from pigpio_encoder import Rotary

class TestSetupSimple(unittest.TestCase):

    @patch('pigpio_encoder.pigpio')
    def test(self, pigpio):

        def rotary_callback(counter):
            print("Counter value: ", counter)

        def sw_short():
            print("Switch pressed")

        my_rotary = Rotary(clk_gpio=27, dt_gpio=22, sw_gpio=17)
        my_rotary.setup_rotary(rotary_callback=rotary_callback)
        my_rotary.setup_switch(sw_short_callback=sw_short)


class TestSetupAll(unittest.TestCase):

    @patch('pigpio_encoder.pigpio')
    def test(self, pigpio):
        def rotary_callback(counter):
            print("Counter value: ", counter)

        def sw_short(self):
            print("Switch short press")

        def sw_long(self):
            print("Switch long press")

        my_rotary = Rotary(clk_gpio=27, dt_gpio=22, sw_gpio=17)
        my_rotary.setup_rotary(min=10, max=300, scale=5, debounce=200, rotary_callback=rotary_callback)
        my_rotary.setup_switch(debounce=200, long_press=True, sw_short_callback=sw_short, sw_long_callback=sw_long)


if __name__ == '__main__':
    unittest.main()
