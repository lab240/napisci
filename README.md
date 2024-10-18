# Napi Sci

## Плата для тестов и обучения Linux

![](images/napi-sci1.jpg)


## Блоки платы

![](images/napi-sci-blocks.jpg)

## Hardware

- Gerber: **/hardware/napisci-gerber/**
- BOM: **/hardware/bom/**
- Схемы: **/hardware/schematics/**
- Step file: **/hardware/step**

- Гербер платы расширения для Napi-C \ NapiSci: **/hardware/hat-gerber**
- Гербер модульного датчика ModBusRTU на основе WemosD1(Esp8266) mini: **/hardware/modbusrtusensor-gerber**

## Software (OS)

Прошивка на основе NapiLinux с настроенными драйверами 

- https://download.napilinux.ru/linuximg/napilinux/napi-sci/

## Опрос модулей и демо-скрипты

- napi_sci_hw.py - небольшая библиотека для чтения\записи GPIO b RTC
- SSD1306.py - библиотека для дисплея Napi Sci
- **napi_display_demo.py** - скрипт, опрашивает датчик, RTC, GPIO и выводит информацию на дисплей.

Необходимые библиотеки:

- smbus2  `pip3 install smbus2`


### Дисплей

Дисплей подключен на интерфейс SPI2. Для его функционирования необходимо подключить оверлей `rk3308-spi2-spidev` и убрать оверлеи для uart1, uart2.

Скрипт, выводящий на дисплей
- IP адрес
- Время и дату с RTC
- Значение датчика SHT30
- Состояние реле и переключателя 


### Цифровые датчики i2c и часы RTC 

Датчики и часы функционируют на шине i2c1. Отдельный оверлей для датчиков подключать не нужно, для часов необходимо подключить `rk3308-i2c1-ds3231`

- Прочитать датчик SHT30 (python)

```python

def read_sht30(addr,prec=2):
    bus.write_i2c_block_data(0x45, 0x2C, [0x06])
    time.sleep(0.1)
    data = bus.read_i2c_block_data(0x45, 0x00, 6)
    ctemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    ctemp_r=round(ctemp,prec)
    humidity_r=round(humidity,prec)
    #print(f"TEMP={ctemp}C, HUM={humidity}%")
    return ctemp_r,humidity_r

```

- Прочитать время из RTC

```bash
root@napi-rk3308b-s:~# hwclock -r
2024-09-20 11:22:48.492633+00:00
root@napi-rk3308b-s:~# 
```
- Записать в RTC время из системы 

```bash
root@napi-rk3308b-s:~# hwclock -w
root@napi-rk3308b-s:~# 

```

### Светодиод и Реле

Светодиод `user_led` подключен на `GPIO0_C0`(чип 0, номер 16(C)+0)
- Включить: 
  
```bash
  gpioset -t 0 -c gpiochip0 16=1

```

- Выключить: 
  
```bash
gpioset -t 0 -c gpiochip0 16=0
```

- Прочитать статус: 
  
```bash
gpioget -a  -c gpiochip0 16
```

Реле подключено на `GPIO2_B6` (чип 2, номер 8(B)+6)
- Включить: 

```bash
gpioset -t 0 -c gpiochip2 14=1
```

- Выключить: 
  
```bash
gpioset -t 0 -c gpiochip2 14=0
```

- Прочитать статус: 

```bash
gpioget -a  -c gpiochip2 14` 
```

>:fire: Статус реле задублирован на светодиод `rel_on`

### Переключатель

Переключатель `user_sw` подключен на `GPIO0_B7`
- Прочитать статус: 
  
```bash
gpioget -a -c gpiochip0 15`
```
 
### Файл оверлеев

Так должен выглядеть файл оверлеев

/etc/boot/uEnv.txt

```bash
verbosity=7
fdtfile=rk3308-rock-pi-s.dtb
console=ttyS0,115200n8
overlays=rk3308-spi2-spidev rk3308-uart3 rk3308-i2c1-ds3231 rk3308-usb-pcie-modem rk3308-usb20-host
kernelimg=Image
extraargs=

```

## Модули платы Napi Sci

1. SOM: Napi Classic: https://napiworld.ru/docs/napi-intro

2. Модуль датчика температуры И влажности SHT30 https://www.ozon.ru/product/arduino-modul-datchika-temperatury-i-vlazhnosti-sht30-304991562/

3. Дисплей https://aliexpress.ru/item/1005001579646238.html?spm=a2g2w.orderdetail.0.0.6ecd4aa6RNanS8&sku_id=12000016669307265

4. Преобразователь CP2102 https://aliexpress.ru/item/1005005837335497.html?spm=a2g2w.orderdetail.0.0.7eb64aa6yfJxpS&sku_id=12000034526403863

5. Модуль TTL в RS485 https://aliexpress.ru/item/1005003562173643.html?spm=a2g2w.orderdetail.0.0.20844aa6VHveHE&sku_id=12000026294112900

6. Модуль часов DS1307 И EEPROM https://www.ozon.ru/product/arduino-s02-rtc-i2c-modul-chasov-ds1307-i-eeprom-297880356/

7. Понижающий преобразователь напряжения LM2596S (DC-DC) https://www.ozon.ru/product/ponizhayushchiy-preobrazovatel-napryazheniya-lm2596s-dc-dc-reguliruemyy-572441082/

## Видео

Короткое видео работы скрипта

https://www.youtube.com/shorts/lHa_7yFC25k

или

https://t.me/napiworld/61


