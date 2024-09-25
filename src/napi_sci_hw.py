# napi_sci_hw.py

import time
from datetime import datetime
import subprocess

def read_hw():
    cmd = "hwclock -r"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    dt = datetime.fromisoformat(result.stdout.rstrip())
    return dt.date(), dt.time().replace(microsecond=0)

def pin_set(gpiochip, pin, value):
    cmd = f"gpioset -t 0 -c {gpiochip} {pin}={value}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def user_led_on():
    return pin_set(gpiochip='gpiochip0', pin=16, value=1)

def user_led_off():
    return pin_set(gpiochip='gpiochip0', pin=16, value=0)

def get_led_status():
    return get_pin_status(gpiochip='gpiochip0', pin=16)

# Сокращенная версия user_led_sw
def user_led_sw():
    user_led_off() if get_led_status() == 1 else user_led_on()

def relay_on():
    return pin_set(gpiochip='gpiochip2', pin=14, value=1)

def relay_off():
    return pin_set(gpiochip='gpiochip2', pin=14, value=0)

def get_relay_status():
    return get_pin_status(gpiochip='gpiochip2', pin=14)

def relay_sw():
    if get_relay_status() == 1:
        relay_off()
    else:
        relay_on()

def get_sw_status():
    return get_pin_status(gpiochip='gpiochip0', pin=15)

def get_pin_status(gpiochip, pin):
    cmd = f"gpioget --numeric -a -c {gpiochip} {pin}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return int(result.stdout)
