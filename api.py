from flask import Flask
from flask_cors import CORS
from tree import RGBXmasTree
from time import sleep
from utils import hexStringToColor

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


yellow = hexStringToColor('ffff00')
blue = hexStringToColor('0000ff')
red = hexStringToColor('ff0000')
green = hexStringToColor('01FF00')

tree = RGBXmasTree()
def off():
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
    tree.bottomToTop(yellow)
    tree.off()
    return "yellow"

@app.route('/tree/blue', methods=['POST'])
def turnBlue():
    tree.bottomToTop(blue)
    tree.off()
    return "blue"

@app.route('/tree/red', methods=['POST'])
def turnRed():
    tree.bottomToTop(red)
    tree.off()
    return "red"

@app.route('/tree/green', methods=['POST'])
def turnGreen():
    tree.bottomToTop(green)
    tree.off()
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

app.run()