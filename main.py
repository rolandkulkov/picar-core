import RPi.GPIO as gpio
import time
import atexit
from threading import Thread
import tornado.web
import tornado.websocket
import time

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
    #cleanup()

def api_forward():
    move_and_cleanup(False, False, False, True)

def api_backwards():
    move_and_cleanup(False, False, True, False)

def api_right():
    move_and_cleanup(False, False, False, True)

def api_left():
    move_and_cleanup(False, True, False, False)

def exit_handler():
    cleanup()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        print("open success")
        # timer that sends data to the front end once per second
        self.timer = tornado.ioloop.PeriodicCallback(self.send_data, 1000)
        self.timer.start()

    def on_close(self):
        self.timer.stop()

    def send_data(self):
        # send the current time to the front end
        self.write_message('Now is' + str(time.time()))
    def on_message(self, message):
        if message == 'left':
            api_left()
        else:
         self.write_message(f"Received: {message}")

application = tornado.web.Application([
    (r'/', WebSocketHandler),
])

if _name_ == '__main__':
    atexit.register(exit_handler)
    application.listen(3001)
    tornado.ioloop.IOLoop.instance().start()