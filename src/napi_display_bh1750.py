# main.py

import time
from PIL import Image, ImageDraw, ImageFont
import spidev
import SSD1306
from bh1750 import BH1750
from smbus2 import SMBus

# Инициализация OLED дисплея
SPI_PORT = 2
SPI_DEVICE = 0

rstpin = 7  # GPIO2_A7
rstchip = "/dev/gpiochip2"
dcpin = 9  # GPIO2_B1
dcchip = "/dev/gpiochip2"

spi = spidev.SpiDev()
spi.open(SPI_PORT, SPI_DEVICE)
spi.max_speed_hz = 8000000
disp = SSD1306.SSD1306_128_64(rstpin=rstpin, rstchip=rstchip, dcpin=dcpin, dcchip=dcchip, spi=spi)

disp.begin()
disp.clear()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

#i2c line 1
bus = SMBus(1)
d_step=10
d_cell=20


while True:
    draw.rectangle((0, 0, width, height), fill=255)

    # Create an instance of SMBus
    bus = SMBus(1)

    # Create an instance of the BH1750 sensor, passing the SMBus object
    sensor = BH1750(bus)

    if sensor.check_device():
       sensor.power_on()
       sensor.reset()
       light_level = sensor.read_light(decimal_places=2)

       # Отображение данных на экране
       draw.text((0, d_cell), f"lux={light_level} lux", font=font, fill=0)
    else:
       draw.text((0, 10), f"ERROR:BMP280 is not detected", font=font, fill=0)
       print(f"BMP280 reading ERROR")


    disp.ShowImage(disp.getbuffer(image))
    time.sleep(0.5)
