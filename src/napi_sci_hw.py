# napi_sci_hw.py

import time
from datetime import datetime
from smbus2 import SMBus
import subprocess

bus = SMBus(1)

SHT30_ADDR = 0x45

def read_hw():
    cmd = "hwclock -r"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    dt = datetime.fromisoformat(result.stdout.rstrip())
    return dt.date(), dt.time().replace(microsecond=0)

def read_sht30(addr, prec=2):
    bus.write_i2c_block_data(addr, 0x2C, [0x06])
    time.sleep(0.1)
    data = bus.read_i2c_block_data(addr, 0x00, 6)
    ctemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    return round(ctemp, prec), round(humidity, prec)

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