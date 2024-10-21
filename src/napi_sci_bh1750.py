# main.py

import argparse
import socket
import time
from smbus2 import SMBus
from bh1750 import BH1750  # Импортируем класс BH1750 из файла bh1750.py

def output_influx(hostname, sensor_name, light_level, multiplier=100):
    """
    Output sensor data in InfluxDB format with timestamp.

    :param hostname: Name of the host system
    :param sensor_name: Name of the sensor
    :param light_level: Measured light level in lux
    :param multiplier: Value to multiply by to get integer
    """
    # Get the current timestamp in nanoseconds
    timestamp = int(time.time() * 1e9)

    # Convert light level to integer by multiplying
    light_level = int(light_level * multiplier)

    # Output in InfluxDB line protocol format
    print(f"{sensor_name},hostname={hostname},name={sensor_name},multiplier={multiplier} {sensor_name}={light_level} {timestamp}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='BH1750 light sensor reader')
    parser.add_argument('--influx-output', action='store_true', 
                        help='Output in InfluxDB line protocol format')
    parser.add_argument('--loop', action='store_true', 
                        help='Continuously output sensor data every second')
    parser.add_argument('--decimal-places', type=int, default=2,
                        help='Number of decimal places for the light level value in normal output')
    parser.add_argument('--multiplier', type=int, default=100,
                        help='Multiplier for integer format in InfluxDB output')

    args = parser.parse_args()

    # Get the hostname of the system
    hostname = socket.gethostname()

    # Create an instance of SMBus
    bus = SMBus(1)

    # Create an instance of the BH1750 sensor, passing the SMBus object
    sensor = BH1750(bus)

    if sensor.check_device():
        sensor.power_on()
        sensor.reset()

        # Loop to continuously read sensor data if --loop is provided
        while True:
            # Read the light level from the sensor
            light_level = sensor.read_light()

            if args.influx_output:
                # Use the separate function to output in InfluxDB format
                output_influx(hostname, "bh1750", light_level, args.multiplier)
            else:
                # Output light level with specified decimal places
                print(f"Light level: {light_level:.{args.decimal_places}f} lux")

            if not args.loop:
                break

            time.sleep(1)  # Delay for 1 second before the next reading
    else:
        print(f"Device not found at address 0x{sensor.address:X}!")

    # Close the SMBus connection
    bus.close()


if __name__ == "__main__":
    main()
