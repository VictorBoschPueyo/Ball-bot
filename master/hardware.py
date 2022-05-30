from adafruit_servokit import ServoKit


#Initialize the kit
kit = ServoKit(channels=8)

def move_board(direction):
    if direction == 'up':
        kit.servo[0].angle = 98
        kit.servo[1].angle = 80
    elif direction == 'down':
        kit.servo[0].angle = 98
        kit.servo[1].angle = 120
    elif direction == 'left':
        kit.servo[0].angle = 120
        kit.servo[1].angle = 98
    elif direction == 'right':
        kit.servo[0].angle = 80
        kit.servo[1].angle = 98
    elif direction == 'stop':
        kit.servo[0].angle = 98
        kit.servo[1].angle = 98
