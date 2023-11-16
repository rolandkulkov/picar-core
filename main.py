from flask import Flask, render_template
from flask_socketio import SocketIO

import RPi.GPIO as gpio
import time
import atexit
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)

# Define GPIO pins
LEFT_FORWARD_PIN = 21
RIGHT_FORWARD_PIN = 20
LEFT_BACKWARD_PIN = 26
RIGHT_BACKWARD_PIN = 16

# Define sleep duration
SLEEP_DURATION = 0.2

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(LEFT_FORWARD_PIN, gpio.OUT)
    gpio.setup(RIGHT_FORWARD_PIN, gpio.OUT)
    gpio.setup(LEFT_BACKWARD_PIN, gpio.OUT)
    gpio.setup(RIGHT_BACKWARD_PIN, gpio.OUT)

def cleanup():
    gpio.cleanup()

def move_pins(left_forward, right_forward, left_backward, right_backward):
    gpio.output(LEFT_FORWARD_PIN, left_forward)
    gpio.output(RIGHT_FORWARD_PIN, right_forward)
    gpio.output(LEFT_BACKWARD_PIN, left_backward)
    gpio.output(RIGHT_BACKWARD_PIN, right_backward)

def move_and_cleanup(left_forward, right_forward, left_backward, right_backward):
    move_pins(left_forward, right_forward, left_backward, right_backward)
    time.sleep(SLEEP_DURATION)

@socketio.on('control')
def handle_control(data):
    direction = data['direction']
    init()

    if direction == 'forward':
        move_and_cleanup(False, True, False, True)
    elif direction == 'backward':
        move_and_cleanup(True, False, True, False)
    elif direction == 'right':
        move_and_cleanup(False, False, False, True)
    elif direction == 'left':
        move_and_cleanup(False, True, True, False)

    cleanup()

if __name__ == '__main__':
    atexit.register(cleanup)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
