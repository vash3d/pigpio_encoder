# Pigpio Encoder

###### Version: 0.1.0 - First Release


#### Python module for the KY040 rotary encoder.
This module has been developed for quickly interface a rotary encoder with Raspberry Pi.
It's based on the [pigpio library](http://abyz.me.uk/rpi/pigpio/python.html) (cause it proved to be faster than rpi.GPIO or gpiozero libraries) so you need to install pigpio library and run pigpio daemon before starting your script.

## Features
- Easy to setup callback functions for the Rotary Encoder and the Switch.
- The Rotary Encoder has customizable min and max values (default 0-100).
- The Rotary Encoder increase/decrease value is customizable (default 1).
- The Switch can be activated or not.
- The Switch can have two different functions for short press or long press.
- Both Rotary and Switch have a customizable debounce value (default 300ms)

## Installation
- Install the pigpio library *(check [pigpio documentation](http://abyz.me.uk/rpi/pigpio/download.html) for alternative installation method)*
 - `sudo apt-get update`
 - `sudo apt-get install pigpio python-pigpio python3-pigpio`
- Install the pigpio_encoder library
 - `pip install pigpio_encoder` (consider add --user option)
- start pigpio daemon
 - `sudo pigpiod`

## How to use
- import the module
<<<<<<< HEAD
    ```python
    from pigpio_encoder import pigpio_encoder
    ```
=======
```python
from pigpio_encoder import pigpio_encoder
```
>>>>>>> d236de85d8f5255bb2faace96627157fdc5cdefa
- create a callback function for the Rotary Encoder.
    > You must pass a positional argument to retrieve the counter value.

    ```python
    def rotary_callback(counter):
        # some action with counter...
    ```
- create callbacks functions for the Switch
    > If you intend to use the switch you must create at least the "short press" callback. The "long press" callback is necessary if you want to use that feature.

    ```python
    def sw_short_callback():
        # some action...
    ```
    ```python
    def sw_long_callback():
        # some action...
      ```
- create the rotary object
    > here you setup the pin number as keyword argument. If you don't pass the switch parameter the switch won't be activated. You must use BCM numbering.

    ```python
    my_rotary = pigpio_encoder.Rotary(clk=pin, dt=pin, sw=pin)
    ```
- setup the rotary encoder
    > here you can setup min and max values for the encoder, the increase/decrease value, a debouce value (default 300ms) and the callback function.

    ```python
    my_rotary.setup_rotary(min=min_value, max=max__value, scale=scale_value, debounce=debounce_value, rotary_callback=rotary_callback)
    ```
- setup the switch
    > if you have specified the switch pin when creating the encoder object, here you can setup the debounce value, the long press option and the callbacks.

    ```python
    my_rotary.setup_switch(debounce=debounce_value, long_press=True, sw_short_callback=sw_short_callback, sw_long_callback=sw_long_callback)
    ```

- start the listener
    ```python
    my_rotary.watch()
    ```

___
#### Basic example using default values
```python
from pigpio_encoder import pigpio_encoder

def rotary_callback(counter):
    print("Counter value: ", counter)

def sw_short():
    print("Switch pressed")

my_rotary = pigpio_encoder.Rotary(clk=27, dt=22, sw=17)
my_rotary.setup_rotary(rotary_callback=rotary_callback)
my_rotary.setup_switch(sw_short_callback=sw_short)

my_rotary.watch()

```
___

#### Example using all the Features
```python
from pigpio_encoder import pigpio_encoder

def rotary_callback(counter):
    print("Counter value: ", counter)

def sw_short():
    print("Switch short press")

def sw_long():
    print("Switch long press")

my_rotary = pigpio_encoder.Rotary(clk=27, dt=22, sw=17)
my_rotary.setup_rotary(min=10, max=300, scale=5, debounce=200, rotary_callback=rotary_callback)
my_rotary.setup_switch(debounce=200, long_press=True, sw_short_callback=sw_short, sw_long_callback=sw_long)

my_rotary.watch()

```
