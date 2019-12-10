from gpiozero import Button, LED, Buzzer
import time
import random
import smbus


I2C_ADDR  = 0x27 
LCD_WIDTH = 16   
LCD_CHR = 1 
LCD_CMD = 0 
LCD_LINE_1 = 0x80 
LCD_LINE_2 = 0xC0 
LCD_LINE_3 = 0x94 
LCD_LINE_4 = 0xD4 
LCD_BACKLIGHT  = 0x08
ENABLE = 0b00000100
E_PULSE = 0.0005
E_DELAY = 0.0005
bus = smbus.SMBus(1)
def lcd_init():
  lcd_byte(0x33,LCD_CMD) 
  lcd_byte(0x32,LCD_CMD) 
  lcd_byte(0x06,LCD_CMD) 
  lcd_byte(0x0C,LCD_CMD) 
  lcd_byte(0x28,LCD_CMD) 
  lcd_byte(0x01,LCD_CMD) 
  time.sleep(E_DELAY)
def lcd_byte(bits, mode):
  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)
def lcd_toggle_enable(bits):
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)
def lcd_string(message,line):
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    
led = LED(6)
led2 = LED(26)

buzzer = Buzzer(5)

player_1 = Button(13)
player_2 = Button(19)

timee = random.uniform(5, 10)

led.toggle()
led2.toggle()

lcd_init()

lcd_string("PREPARENSE         <",LCD_LINE_1)
lcd_string("!!!!!!!!!!        <",LCD_LINE_2)

time.sleep(timee)

lcd_string("YAAAAAAAAA         <",LCD_LINE_1)
lcd_string("!!!!!!!!!!        <",LCD_LINE_2)

buzzer.on()

time.sleep(0.5)

buzzer.off()

while True:
    if player_1.is_pressed:
        led.toggle()
        lcd_string("HA GANADO EL",LCD_LINE_1)
        lcd_string("JUGADOR 1!!!!!!!!!!        <",LCD_LINE_2)
        break
    if player_2.is_pressed:
        led2.toggle()
        lcd_string("HA GANADO EL",LCD_LINE_1)
        lcd_string("JUGADOR 2!!!!!!!!!!        <",LCD_LINE_2)
        break

