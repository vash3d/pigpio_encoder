# Rotary encoder class based on pigpio library
# version: 0.2.2

import pigpio
import time

# States
DT1 = 'D' # DT is high
DT0 = 'd' # DT is low
CLK1 = 'C' # CLK is high
CLK0 = 'c' # CLK is low

# State sequences
SEQUENCE_UP = DT1 + CLK1 + DT0 + CLK0
SEQUENCE_DOWN = CLK1 + DT1 + CLK0 + DT0


class Rotary:

    sequence = ''

    # Default values for the rotary encoder
    min = 0
    max = 100
    scale = 1
    debounce = 300
    _counter = 0
    last_counter = 0
    rotary_callback = None

    # Default values for the switch
    sw_debounce = 300
    long_press_opt = False
    sw_short_callback = None
    sw_long_callback = None
    wait_time = time.time()
    long = False

    def __init__(self, clk=None, dt=None, sw=None):
        if not clk or not dt:
            raise BaseException("CLK and DT pin must be specified!")
        self.clk = clk
        self.dt = dt
        self.clk_input = pigpio.pi()
        self.dt_input = pigpio.pi()
        self.clk_input.set_glitch_filter(self.clk, self.debounce)
        self.dt_input.set_glitch_filter(self.dt, self.debounce)
        if sw is not None:
            self.sw = sw
            self.sw_input = pigpio.pi()
            self.sw_input.set_pull_up_down(self.sw, pigpio.PUD_UP)
            self.sw_input.set_glitch_filter(self.sw, self.sw_debounce)
        self.setup_pigpio_callbacks()

    def setup_pigpio_callbacks(self):
        self.clk_falling = self.clk_input.callback(self.clk, pigpio.FALLING_EDGE, self.clk_fall)
        self.clk_rising = self.clk_input.callback(self.clk, pigpio.RISING_EDGE, self.clk_rise)
        self.dt_falling = self.dt_input.callback(self.dt, pigpio.FALLING_EDGE, self.dt_fall)
        self.dt_rising = self.dt_input.callback(self.dt, pigpio.RISING_EDGE, self.dt_rise)
        self.sw_falling = self.sw_input.callback(self.sw, pigpio.FALLING_EDGE, self.sw_fall)
        self.sw_rising = self.sw_input.callback(self.sw, pigpio.RISING_EDGE, self.sw_rise)

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value):
        if self._counter != value:
            self._counter = value
            self.rotary_callback(self._counter)

    def clk_fall(self, gpio, level, tick):
        if len(self.sequence) > 2:
            self.sequence = ''
        self.sequence += CLK1

    def clk_rise(self, gpio, level, tick):
        self.sequence += CLK0
        if self.sequence == SEQUENCE_UP:
            if self.counter < self.max:
                self.counter += self.scale
            self.sequence = ''

    def dt_fall(self, gpio, level, tick):
        if len(self.sequence) > 2:
            self.sequence = ''
        self.sequence += DT1

    def dt_rise(self, gpio, level, tick):
        self.sequence += DT0
        if self.sequence == SEQUENCE_DOWN:
            if self.counter > self.min:
                self.counter -= self.scale
            self.sequence = ''

    def sw_rise(self, gpio, level, tick):
        if self.long_press_opt:
            if not self.long:
                self.short_press()

    def sw_fall(self, gpio, level, tick):
        if self.long_press_opt:
            self.long = False
            press_time = time.time()
            while self.sw_input.read(self.sw) == 0:
                self.wait_time = time.time()
                time.sleep(0.1)
                if self.wait_time - press_time > 1.5:
                    self.long_press()
                    self.long = True
                    break
        else:
            self.short_press()

    def setup_rotary(self, **kwargs):
        if 'min' in kwargs:
            self.min = kwargs['min']
            self.counter = self.min
            self.last_counter = self.min
        if 'max' in kwargs:
            self.max = kwargs['max']
        if 'scale' in kwargs:
            self.scale = kwargs['scale']
        if 'debounce' in kwargs:
            self.debounce = kwargs['debounce']
            self.clk_input.set_glitch_filter(self.clk, self.debounce)
            self.dt_input.set_glitch_filter(self.dt, self.debounce)
        if 'rotary_callback' in kwargs:
            self.rotary_callback = kwargs['rotary_callback']

    def setup_switch(self, **kwargs):
        if 'debounce' in kwargs:
            self.sw_debounce = kwargs['debounce']
        if 'long_press' in kwargs:
            self.long_press_opt = kwargs['long_press']
        if 'sw_short_callback' in kwargs:
            self.sw_short_callback = kwargs['sw_short_callback']
        if 'sw_long_callback' in kwargs:
            self.sw_long_callback = kwargs['sw_long_callback']

    def watch(self):
        """
        Do not use! It will eat 100% CPU time on one core.
        """
        while True:
            if self.counter != self.last_counter:
                self.last_counter = self.counter
                self.rotary_callback(self.counter)

    def short_press(self):
        self.sw_short_callback()

    def long_press(self):
        self.sw_long_callback()
