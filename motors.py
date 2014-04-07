import RPi.GPIO as gpio

# Setup

a_en = 7
a_in1 = 13
a_in2 = 15

b_en = 12
b_in1 = 18
b_in2 = 22

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(a_en, gpio.OUT)
gpio.setup(a_in1, gpio.OUT)
gpio.setup(a_in2, gpio.OUT)
gpio.setup(b_en, gpio.OUT)
gpio.setup(b_in1, gpio.OUT)
gpio.setup(b_in2, gpio.OUT)

# Have the in pins be off initially
gpio.output(a_in1, False)
gpio.output(a_in2, False)
gpio.output(b_in1, False)
gpio.output(b_in2, False)
gpio.output(a_en, False)
gpio.output(b_en, False)

def moveA(forward):
	gpio.output(a_in1, forward)
	gpio.output(a_in2, not forward)

def moveB(forward):
	gpio.output(b_in1, forward)
	gpio.output(b_in2, not forward)

def onA():
	gpio.output(a_en, True)
	
def offA():
	gpio.output(a_en, False)
	gpio.output(a_in1, False)
	gpio.output(a_in2, False)
	
def onB():
	gpio.output(b_en, True)

def offB():
	gpio.output(b_en, False)
	gpio.output(b_in1, False)
	gpio.output(b_in2, False)
