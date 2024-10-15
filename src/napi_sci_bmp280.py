import time
import socket
from datetime import datetime
from smbus2 import SMBus
import subprocess
from bme280 import BME280
import argparse

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
    return round(temperature, prec), round(pressure, prec), round(humidity, prec)

def get_hostname():
    return socket.gethostname()

def output_influx(temperature, pressure, humidity):
    hostname = get_hostname()
    timestamp = int(time.time() * 1e9)  # InfluxDB expects timestamps in nanoseconds
    influx_line = f"bmp280,host={hostname},temperature={temperature},pressure={pressure},humidity={humidity} {timestamp}"
    return influx_line

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read data from BMP280 sensor.")
    parser.add_argument("--influx-output", action="store_true", help="Output data in InfluxDB line protocol format")
    args = parser.parse_args()

    bus = SMBus(1)
    
    if check_bmp280(bus):
        t, p, h = read_bmp280(bus)
        
        if args.influx_output:
            # Output in InfluxDB format
            influx_data = output_influx(t, p, h)
            print(influx_data)
        else:
            # Default output
            print(f"{t}°C {p}Pa {h}%")
    else:
        print("BMP280 not detected on 0x76")
