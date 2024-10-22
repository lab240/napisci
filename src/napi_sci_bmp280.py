"""

This script reads bmp280 sensor and 
outputs result in human format or
in influx format for write to influx database (--influx-output)

This is part of telegraf config to exec this script

[[inputs.exec]]
  commands = ["python3 /path/this_script --influx-output"]
  timeout = "5s"
  data_format = "influx"
"""

"""

For correct work, you need packages installed

pip3 install smbus2
pip3 install pimoroni-bme280
"""

import argparse
import socket
import time
from smbus2 import SMBus
from bme280 import BME280  # Using the bme280 library for the sensor

def check_bmp280(bus, address=0x76):
    """
    Check if the BMP280 sensor is available on the I2C bus.
    
    :param bus: I2C bus instance
    :param address: Sensor's I2C address (default 0x76)
    :return: True if the sensor is found, False otherwise
    """
    try:
        bus.write_quick(address)
        return True
    except OSError:
        return False

def read_bmp280(bus, address=0x76, prec=2):
    """
    Read temperature, pressure, and humidity data from the BMP280/BME280 sensor.
    
    :param bus: I2C bus instance
    :param address: Sensor's I2C address (default 0x76)
    :param prec: Number of decimal places for rounding the results
    :return: Rounded temperature, pressure, and humidity values
    """
    bme280 = BME280(i2c_dev=bus)
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    return round(temperature, prec), round(pressure, prec), round(humidity, prec)

def output_influx(hostname, sensor_name, temperature, pressure, humidity, multiplier=100):
    """
    Output sensor data in InfluxDB line protocol format.

    :param hostname: Hostname of the system
    :param sensor_name: Name of the sensor
    :param temperature: Measured temperature in degrees Celsius
    :param pressure: Measured pressure in Pascals
    :param humidity: Measured humidity in percentage
    :param multiplier: Multiplier for converting to integer values
    """
    timestamp = int(time.time() * 1e9)

    # Convert values to integers using the multiplier
    temperature = int(temperature * multiplier)
    pressure = int(pressure * multiplier)
    humidity = int(humidity * multiplier)

    # Output data in InfluxDB format with 'multiplier' as a tag
    print(f"{sensor_name},hostname={hostname},name={sensor_name},multiplier={multiplier} "
          f"bmp280_temp={temperature},bmp280_pressure={pressure},bmp280_humidity={humidity} {timestamp}")

def main():
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description='BMP280 sensor reader')
    parser.add_argument('--influx-output', action='store_true', 
                        help='Output data in InfluxDB line protocol format')
    parser.add_argument('--loop', action='store_true', 
                        help='Continuously output sensor data every second')
    parser.add_argument('--decimal-places', type=int, default=2,
                        help='Number of decimal places for sensor data output')
    parser.add_argument('--multiplier', type=int, default=100,
                        help='Multiplier for integer output in InfluxDB format')

    args = parser.parse_args()

    # Get the hostname of the system
    hostname = socket.gethostname()

    # Create an instance of SMBus
    bus = SMBus(1)

    # Check if the BMP280 sensor is available
    if check_bmp280(bus):
        while True:
            # Read data from the BMP280 sensor
            temperature, pressure, humidity = read_bmp280(bus, prec=args.decimal_places)

            if args.influx_output:
                # Output data in InfluxDB format
                output_influx(hostname, "bmp280", temperature, pressure, humidity, args.multiplier)
            else:
                # Standard output with the specified number of decimal places
                print(f"Temperature: {temperature:.{args.decimal_places}f} °C, "
                      f"Pressure: {pressure:.{args.decimal_places}f} Pa, "
                      f"Humidity: {humidity:.{args.decimal_places}f} %")

            if not args.loop:
                break

            time.sleep(1)  # Delay of 1 second before the next reading
    else:
        print(f"Sensor not found at address 0x76!")

    # Close the SMBus connection
    bus.close()


if __name__ == "__main__":
    main()
