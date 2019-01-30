# Rotary encoder class based on pigpio library
# version: 0.1.1

import pigpio
import time


class Rotary:

	# Set the sequence for CW and CCW
	sequence = []
	sequence_up = ['dt1', 'clk1', 'dt0', 'clk0']
	sequence_down = ['clk1', 'dt1', 'clk0', 'dt0']

	# Default values for the rotary encoder
	min = 0
	max = 100
	scale = 1
	debounce = 300
	counter = 0
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

		def clk_fall(gpio, level, tick):
			if len(self.sequence) > 2:
				self.sequence.clear()
			self.sequence.append('clk1')

		def clk_rise(gpio, level, tick):
			self.sequence.append('clk0')
			if self.sequence == self.sequence_up:
				if self.counter < self.max:
					self.counter += self.scale
				self.sequence.clear()

		def dt_fall(gpio, level, tick):
			if len(self.sequence) > 2:
				self.sequence.clear()
			self.sequence.append('dt1')

		def dt_rise(gpio, level, tick):
			self.sequence.append('dt0')
			if self.sequence == self.sequence_down:
				if self.counter > self.min:
					self.counter -= self.scale
				self.sequence.clear()

		def sw_rise(gpio, level, tick):
			if self.long_press_opt:
				if not self.long:
					self.short_press()

		def sw_fall(gpio, level, tick):
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


		self.clk_falling = self.clk_input.callback(self.clk, pigpio.FALLING_EDGE, clk_fall)
		self.clk_rising = self.clk_input.callback(self.clk, pigpio.RISING_EDGE, clk_rise)
		self.dt_falling = self.dt_input.callback(self.dt, pigpio.FALLING_EDGE, dt_fall)
		self.dt_rising = self.dt_input.callback(self.dt, pigpio.RISING_EDGE, dt_rise)
		self.sw_falling = self.sw_input.callback(self.sw, pigpio.FALLING_EDGE, sw_fall)
		self.sw_rising = self.sw_input.callback(self.sw, pigpio.RISING_EDGE, sw_rise)


	def setup_rotary(self, **kwargs):
		if 'min' in kwargs:
			self.min = kwargs['min']
			self.counter = self.min
			self.last_counter = self.min
		if 'max' in kwargs:
			self.max = kwargs['max']
		if 'scale' in kwargs:
			self.scale = kwargs['scale']
		if 'debouce' in kwargs:
			self.debounce = kwargs['debouce']
			self.clk_input.set_glitch_filter(self.clk, self.debounce)
			self.dt_input.set_glitch_filter(self.dt, self.debounce)
		if 'rotary_callback' in kwargs:
			self.rotary_callback = kwargs['rotary_callback']

	def setup_switch(self, **kwargs):
		if 'debounce' in kwargs:
			self.sw_debounce = kwargs['debouce']
		if 'long_press' in kwargs:
			self.long_press_opt = kwargs['long_press']
		if 'sw_short_callback' in kwargs:
			self.sw_short_callback = kwargs['sw_short_callback']
		if 'sw_long_callback' in kwargs:
			self.sw_long_callback = kwargs['sw_long_callback']

	def watch(self):
		# self.callback = callback
		while True:
			if self.counter != self.last_counter:
				self.last_counter = self.counter
				self.rotary_callback(self.counter)

	def short_press(self):
		self.sw_short_callback()

	def long_press(self):
		self.sw_long_callback()
