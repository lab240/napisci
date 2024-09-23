# Napi Sci

## Плата для тестов и обучения Linux

![](images/napi-sci1.jpg)


## Блоки платы

![](images/napi-sci-blocks.jpg)

## Готовые прошивки

Прошивка на основе NapiLinux с настроенными драйверами 

- https://download.napilinux.ru/linuximg/napilinux/napi-sci/

## Демо-скрипты

- napi_sci_hw.py - небольшая библиотека для чтения\записи GPIO b RTC
- SSD1306.py - библиотека для дисплея Napi Sci
- napi_display_demo.py - скрипт, опрашивает датчик, RTC, GPIO и выводит информацию на дисплей.

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

### Модули платы Napi Sci


