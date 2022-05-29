import gpio
from adafruit_servokit import ServoKit
#Initialize the kit
kit = ServoKit(channels=16)
gpio.set_mode(gpio.BOARD)
gpio.setup(7, gpio.OUT)
gpio.setup(8, gpio.OUT)


def test_camera():
    pass


def test_servos():
    pass


def test_screen():
    pass
  

def move_board(direction):
    if direction == 'up':
        kit.servo[0].angle = 95
        kit.servo[1].angle = 90
    elif direction == 'down':
        kit.servo[0].angle = 90
        kit.servo[1].angle = 95
    elif direction == 'left':
        kit.servo[0].angle = -95
        kit.servo[1].angle = 90
    elif direction == 'right':
        kit.servo[0].angle = 90
        kit.servo[1].angle = -95
    elif direction == 'stop':
        kit.servo[0].angle = 90
        kit.servo[1].angle = 90
    
    
def connect():
    pass


def record_video():
    pass