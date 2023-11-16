from flask import Flask, jsonify
import RPi.GPIO as gpio
import time

app = Flask(__name__)

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(21, gpio.OUT)
    gpio.setup(20, gpio.OUT)
    gpio.setup(26, gpio.OUT)
    gpio.setup(16, gpio.OUT)

def cleanup():
    gpio.cleanup()

@app.route('/forward', methods=['GET'])
def api_forward():
    init()
    gpio.output(21, False)
    gpio.output(20, True)
    time.sleep(0.1)  # You can adjust the sleep duration if needed
    cleanup()
    return '', 200

@app.route('/backwards', methods=['GET'])
def api_backwards():
    init()
    gpio.output(21, True)
    gpio.output(20, False)
    time.sleep(0.2)
    cleanup()
    return jsonify({"status": "success", "message": "Moved backwards"})

@app.route('/right', methods=['GET'])
def api_right():
    init()
    gpio.output(16, True)
    gpio.output(26, False)
    gpio.output(21, False)
    gpio.output(20, False)
    time.sleep(0.2)
    cleanup()
    return jsonify({"status": "success", "message": "Turned right"})

@app.route('/left', methods=['GET'])
def api_left():
    init()
    gpio.output(16, False)
    gpio.output(26, True)
    gpio.output(21, False)
    gpio.output(20, False)
    time.sleep(0.2)
    cleanup()
    return jsonify({"status": "success", "message": "Turned left"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
