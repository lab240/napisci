# napi_sci_sht30.py

import time
from datetime import datetime
from smbus2 import SMBus
import subprocess

SHT30ADDR=0x45

def check_sht30(bus,address=0x45):
    try:
        bus.write_quick(address)
        return True
    except OSError:
        return False

def read_sht30(bus,addr, prec=2):
    bus.write_i2c_block_data(addr, 0x2C, [0x06])
    time.sleep(0.1)
    data = bus.read_i2c_block_data(addr, 0x00, 6)
    ctemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    return round(ctemp, prec), round(humidity, prec)

if __name__ == "__main__":
    if check_sht30():
        (t,h)=read_sht30(SHT30ADDR)
        print(f"{t}°C {h}%")
    else:
        print(f"SHT30 not detected on 0x{SHT30ADDR:x}")

