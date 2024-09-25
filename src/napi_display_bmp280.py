# main.py

import time
from PIL import Image, ImageDraw, ImageFont
import spidev
import SSD1306
import napi_sci_bmp280 as bmp280  # Импортируем наш модуль с новым названием
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
d_cell=0


while True:
    draw.rectangle((0, 0, width, height), fill=255)

    # Системная информация
    if bmp280.check_bmp280(bus):
       temp, pressure, humidity = bmp280.read_bmp280(bus,2)
       # Отображение данных на экране
       d_cell=0
       draw.text((0, d_cell), f"Temperature={temp} C", font=font, fill=0)
       d_cell=d_cell+d_step
       draw.text((0, d_cell), f"Pressure={pressure}i hPa", font=font, fill=0)
       d_cell=d_cell+d_step
       draw.text((0, d_cell), f"Humidity={humidity} %", font=font, fill=0)
       print(f"{temp:05.2f}°C {pressure:05.2f}hPa {humidity:05.2f}%")
    else:
       draw.text((0, 10), f"ERROR:BMP280 is not detected", font=font, fill=0)
       print(f"BMP280 reading ERROR")


    disp.ShowImage(disp.getbuffer(image))
    time.sleep(0.5)
