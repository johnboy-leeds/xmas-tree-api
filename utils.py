import random

timingDelay = 0.35

def randomColor():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)

def hexStringToColor(hex):
  if len(hex) == 3:
    redPart = hex[0:1] + hex[0:1]
    greenPart = hex[1:1] + hex[1:1]
    bluePart = hex[2:1] + hex[2:1]
  else:
    redPart = hex[0:2]
    greenPart = hex[2:4]
    bluePart = hex[-2:]
    
  percent = 1/255
  return (int(redPart, 16) * percent, int(greenPart, 16) * percent, int(bluePart, 16) * percent)