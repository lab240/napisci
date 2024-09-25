# napi_sci_bmp280.py

import time
from datetime import datetime
from smbus2 import SMBus
import subprocess
from bme280 import BME280

def check_bmp280(bus, address=0x76):
    try:
        bus.write_quick(address)
        return True
    except OSError:
        return False

def read_bmp280(bus, prec=2):
    bme280 = BME280(i2c_dev=bus)
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    return round(temperature,prec), round(pressure,prec), round(humidity,prec)


if __name__ == "__main__":
    bus = SMBus(1)
    if check_bmp280(bus):
        (t,p,h)=read_bmp280(bus)
        print(f"{t}°C {p}Pa {h}%")
    else:
        print(f"BMP280 not detected on 0x76")
