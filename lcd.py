#!/usr/bin/python
 
import RPi.GPIO as GPIO
import time

# GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
LCD_LED = 15

LCD_WIDTH = 16 # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

E_PULSE = 0.00005
E_DELAY = 0.00005


def init():

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LCD_E, GPIO.OUT)  # E
	GPIO.setup(LCD_RS, GPIO.OUT) # RS
	GPIO.setup(LCD_D4, GPIO.OUT) # DB4
	GPIO.setup(LCD_D5, GPIO.OUT) # DB5
	GPIO.setup(LCD_D6, GPIO.OUT) # DB6
	GPIO.setup(LCD_D7, GPIO.OUT) # DB7
	GPIO.setup(LCD_LED, GPIO.OUT) # Backlight

	clear()


def clear():
	""" reset LCD """

	lcd_byte(0x33,LCD_CMD)
	lcd_byte(0x32,LCD_CMD)
	lcd_byte(0x28,LCD_CMD)
	lcd_byte(0x0C,LCD_CMD)
	lcd_byte(0x06,LCD_CMD)
	lcd_byte(0x01,LCD_CMD)


def message(text):
	""" Shows text """

	time.sleep(0.01)
	lines = text.split('\n')
	lcd_byte(LCD_LINE_1, LCD_CMD)
	lcd_string(lines[0])
	if len(lines) > 1:
		lcd_byte(LCD_LINE_2, LCD_CMD)
		lcd_string(lines[1])


def backlight(enable):
	""" Switch LCD backlight on/off"""

	if GPIO.input(LCD_LED) != enable:
		GPIO.output(LCD_LED, enable)


def lcd_string(message):
	message = message.ljust(LCD_WIDTH," ")  

	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR) 


def lcd_byte(bits, mode):
	GPIO.output(LCD_RS, mode) # RS
 
	# High bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits&0x10==0x10:
		GPIO.output(LCD_D4, True)
	if bits&0x20==0x20:
		GPIO.output(LCD_D5, True)
	if bits&0x40==0x40:
		GPIO.output(LCD_D6, True)
	if bits&0x80==0x80:
		GPIO.output(LCD_D7, True)
 
	time.sleep(E_DELAY)    
	GPIO.output(LCD_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, False)  
	time.sleep(E_DELAY)      

	# Low bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits&0x01==0x01:
		GPIO.output(LCD_D4, True)
	if bits&0x02==0x02:
		GPIO.output(LCD_D5, True)
	if bits&0x04==0x04:
		GPIO.output(LCD_D6, True)
	if bits&0x08==0x08:
		GPIO.output(LCD_D7, True)

	time.sleep(E_DELAY)    
	GPIO.output(LCD_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, False)  
	time.sleep(E_DELAY)   


def main():

	GPIO.setwarnings(False)
	init()
	message("Raspberry Pi 321\nTest 1234567890.")


if __name__ == '__main__':
	main()
