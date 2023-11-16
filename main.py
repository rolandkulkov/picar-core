from flask import Flask, jsonify
import RPi.GPIO as gpio
import time

app = Flask(__name__)

PIN_LEFT =  26
PIN_RIGHT = 16
PIN_ENGINE_ON = 20
PIN_ENGINE_OFF = 21

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(PIN_ENGINE_OFF, gpio.OUT)
    gpio.setup(PIN_ENGINE_ON, gpio.OUT)
    gpio.setup(PIN_LEFT, gpio.OUT)
    gpio.setup(PIN_RIGHT, gpio.OUT)

init()

def cleanup():
    gpio.cleanup()

@app.route('/forward', methods=['GET'])
def api_forward():
    gpio.output(21, False)
    gpio.output(20, True)
    cleanup()
    return '', 200

@app.route('/backwards', methods=['GET'])
def api_backwards():
    gpio.output(21, True)
    gpio.output(20, False)
    cleanup()
    return '', 200

@app.route('/right', methods=['GET'])
def api_right():
    gpio.output(16, True)
    gpio.output(26, False)
    gpio.output(21, False)
    gpio.output(20, False)
    cleanup()
    return '', 200

@app.route('/left', methods=['GET'])
def api_left():
    gpio.output(16, False)
    gpio.output(26, True)
    gpio.output(21, False)
    gpio.output(20, False)
    cleanup()
    return '', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
