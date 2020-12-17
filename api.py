from flask import Flask
from flask_cors import CORS
from tree import RGBXmasTree
from time import sleep
from utils import hexStringToColor, timingDelay

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

yellow = hexStringToColor('ffff00')
blue = hexStringToColor('0000ff')
red = hexStringToColor('ff0000')
green = hexStringToColor('01FF00')

tree = RGBXmasTree()
tree.brightness = 0.04

def runColor(color):
    tree.bottomToTop(color)
    sleep(timingDelay)
    tree.topRow(color)
    sleep(timingDelay)
    tree.middleRow(color)
    sleep(timingDelay)
    tree.bottomRow(color)
    sleep(2)
    tree.off()

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/tree/demo', methods=['POST'])
def demo():
    tree.off()
    tree.brightness = 0.05
    tree.bottomToTop(yellow)
    tree.bottomToTop(blue)
    tree.bottomToTop(yellow)
    tree.off()
    return "demo ran"

@app.route('/ping', methods=['GET'])
def ping():
    return "pong"

@app.route('/tree/yellow', methods=['POST'])
def turnYellow():
    runColor(yellow)
    return "yellow"

@app.route('/tree/blue', methods=['POST'])
def turnBlue():
    runColor(blue)
    return "blue"

@app.route('/tree/red', methods=['POST'])
def turnRed():
    runColor(red)
    return "red"

@app.route('/tree/green', methods=['POST'])
def turnGreen():
    runColor(green)
    return "green"

@app.route('/tree/twinkle', methods=['POST'])
def twinkle():
    tree.twinkle()
    tree.off()
    return "twinkle"

@app.route('/tree/off', methods=['POST'])
def turnOff():
    tree.off()
    return "off"

@app.route('/tree/christmas', methods=['POST'])
def christmas():
    for x in range(10):
        tree.alternateColours(red, green)
        sleep(timingDelay)
        tree.alternateColours(green, red)
        sleep(timingDelay)
    tree.off()
    return 'done'

@app.route('/tree/color-wheel', methods=['POST'])
def colourWheel():
    tree.hueCycle()
    tree.off()
    return 'done'

app.run()