# bh1750.py

import time

class BH1750:
    # BH1750 device I2C address
    BH1750_ADDRESS = 0x23

    # Commands for BH1750
    POWER_ON = 0x01
    RESET = 0x07
    CONTINUOUS_HIGH_RES_MODE = 0x10

    def __init__(self, bus, address=BH1750_ADDRESS):
        """
        Initialize the BH1750 sensor with a given SMBus object.
        
        :param bus: An instance of SMBus
        :param address: I2C address of the BH1750 sensor (default: 0x23)
        """
        self.bus = bus
        self.address = address

    def check_device(self):
        """
        Check if the device is available at the I2C address.
        :return: True if device is found, False otherwise
        """
        try:
            self.bus.read_byte(self.address)
            return True
        except Exception as e:
            return False

    def power_on(self):
        """
        Power on the BH1750 sensor.
        """
        self.bus.write_byte(self.address, self.POWER_ON)

    def reset(self):
        """
        Reset the BH1750 sensor.
        """
        self.bus.write_byte(self.address, self.RESET)

    def read_light(self,decimal_places=2):
        """
        Read the light level from the BH1750 sensor.
        :return: Light level in lux
        """
        # Send the command to start measurement
        self.bus.write_byte(self.address, self.CONTINUOUS_HIGH_RES_MODE)
        time.sleep(0.2)  # Give the sensor time to perform the measurement

        # Read two bytes from the sensor
        data = self.bus.read_i2c_block_data(self.address, 0x00, 2)

        # Convert the two bytes into a light level (lux)
        lux = (data[0] << 8 | data[1]) / 1.2
        return round(lux,decimal_places)

