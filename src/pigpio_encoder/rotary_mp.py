from machine import Pin
import time

# Rotary encoder FSM transition table (index = (prev_state << 2) + curr_state)
# Values: +1 (CW step), -1 (CCW step), 0 (no step)
_STATE_TRANSITION_TABLE = [
    0,  -1,  1,  0,
    1,   0,  0, -1,
   -1,   0,  0,  1,
    0,   1, -1,  0
]

class Rotary:
    def __init__(self, clk_gpio, dt_gpio, sw_gpio=None):
        if clk_gpio is None or dt_gpio is None:
            raise ValueError("clk_gpio and dt_gpio must be specified")

        self.clk_gpio = clk_gpio
        self.dt_gpio = dt_gpio
        self.sw_gpio = sw_gpio

        self.min = 0
        self.max = 100
        self.scale = 1
        self.debounce = 300  # debounce not used in this implementation but preserved

        self._counter = self.min
        self.last_counter = self.min

        self.rotary_callback = None
        self.up_callback = None
        self.down_callback = None

        self.sw_short_callback = None
        self.sw_long_callback = None
        self.long_press_opt = False
        self.long = False
        self.sw_debounce = None

        # Initialize pins
        self.clk_pin = Pin(self.clk_gpio, Pin.IN, Pin.PULL_UP)
        self.dt_pin = Pin(self.dt_gpio, Pin.IN, Pin.PULL_UP)
        if self.sw_gpio is not None:
            self.sw_pin = Pin(self.sw_gpio, Pin.IN, Pin.PULL_UP)
        else:
            self.sw_pin = None

        # Initialize the FSM state: 2 bits = (clk << 1) | dt
        self.prev_state = (self.clk_pin.value() << 1) | self.dt_pin.value()

        # Setup interrupts
        self.clk_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._pin_changed)
        self.dt_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._pin_changed)

        if self.sw_pin is not None:
            self.sw_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._sw_gpio_call)
        
    @property
    def counter(self):
        return self._counter
    
    @counter.setter
    def counter(self, value):
        clamped_value = max(self.min, min(self.max, value))
        if clamped_value != self._counter:
            self._counter = clamped_value
            if self.rotary_callback:
                self.rotary_callback(self._counter)
    
    def _pin_changed(self, pin):
        current_state = (self.clk_pin.value() << 1) | self.dt_pin.value()
        index = (self.prev_state << 2) | current_state
        delta = _STATE_TRANSITION_TABLE[index]
        self.prev_state = current_state
        
        if delta == 1:
            if self.counter + self.scale <= self.max:
                self.counter += self.scale
                if self.up_callback:
                    self.up_callback(self._counter)
        elif delta == -1:
            if self.counter - self.scale >= self.min:
                self.counter -= self.scale
                if self.down_callback:
                    self.down_callback(self._counter)
    
    def _sw_gpio_call(self, pin):
        val = pin.value()
        if val == 0:  # button pressed
            self._sw_gpio_fall()
        else:  # button released
            self._sw_gpio_rise()
    
    def _sw_gpio_rise(self):
        if self.long_press_opt:
            if not self.long:
                self.short_press()
    
    def _sw_gpio_fall(self):
        if self.long_press_opt:
            self.long = False
            start_time = time.ticks_ms()
            while self.sw_pin.value() == 0:
                time.sleep(0.01)
                elapsed = time.ticks_diff(time.ticks_ms(), start_time)
                if elapsed > 1500:  # long press threshold 1.5 seconds
                    self.long_press()
                    self.long = True
                    break
            # If comes here and long == False, treat as short press on release
            if not self.long:
                self.short_press()
        else:
            self.short_press()

    def short_press(self):
        if self.sw_short_callback:
            self.sw_short_callback()

    def long_press(self):
        if self.sw_long_callback:
            self.sw_long_callback()
    
    def setup_rotary(self, rotary_callback=None, up_callback=None, down_callback=None,
                     min=None, max=None, scale=None, debounce=None):
        if rotary_callback:
            self.rotary_callback = rotary_callback
        if up_callback:
            self.up_callback = up_callback
        if down_callback:
            self.down_callback = down_callback
        if min is not None:
            self.min = min
            self.counter = self.min
            self.last_counter = self.min
        if max is not None:
            self.max = max
        if scale is not None:
            self.scale = scale
        if debounce is not None:
            self.debounce = debounce
    
    def setup_switch(self, sw_short_callback=None, sw_long_callback=None,
                     debounce=None, long_press=None):
        if sw_short_callback is not None:
            self.sw_short_callback = sw_short_callback
        if sw_long_callback is not None:
            self.sw_long_callback = sw_long_callback
        if debounce is not None:
            self.sw_debounce = debounce  # Not used here, placeholder for future debounce logic
        if long_press is not None:
            self.long_press_opt = long_press
    
    @staticmethod
    def watch():
        while True:
            time.sleep(10)

