# main.py

import time
from PIL import Image, ImageDraw, ImageFont
import spidev
import SSD1306
import napi_sci_hw as hw  # Импортируем наш модуль с новым названием
import napi_sci_sht30 as sht30  # Импортируем наш модуль с новым названием
import subprocess
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

bus=SMBus(1)

while True:
    draw.rectangle((0, 0, width, height), fill=255)

    # Системная информация
    cmd = "ip -4 addr show dev end0 | awk '/inet/ {print $2}' | cut -d'/' -f1"
    IP = "IP:" + subprocess.check_output(cmd, shell=True).decode('utf-8')

    hw_date, hw_time = hw.read_hw()
    # Отображение данных на экране
    draw.text((0, 0), IP, font=font, fill=0)
    draw.text((0, 10), f"HWDate:{hw_date}", font=font, fill=0)
    draw.text((0, 20), f"HWTime:{hw_time}", font=font, fill=0)
    
    if sht30.check_sht30(bus):
        temp, humidity = sht30.read_sht30(bus,0x45)
        draw.text((0, 30), f"Temp:{temp}, Hum: {humidity}", font=font, fill=0)
    else:
        draw.text((0, 30), f"ERROR reading", font=font, fill=0)


    hw.user_led_sw()
    hw.relay_sw()

    draw.text((0, 40), f"LED: {hw.get_led_status()}, RELAY: {hw.get_relay_status()}", font=font, fill=0)
    draw.text((0, 50), f"USER SW: {hw.get_sw_status()}", font=font, fill=0)

    disp.ShowImage(disp.getbuffer(image))
    print(f"HWTime:{hw_time}: Temp:{temp}, Hum: {humidity}") 
    time.sleep(0.5)
