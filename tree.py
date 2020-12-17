from gpiozero import SPIDevice, SourceMixin
from colorzero import Color, Hue
from statistics import mean
from time import sleep
from utils import randomColor
import random

class Pixel:
    def __init__(self, parent, index):
        self.parent = parent
        self.index = index

    @property
    def value(self):
        return self.parent.value[self.index]

    @value.setter
    def value(self, value):
        new_parent_value = list(self.parent.value)
        new_parent_value[self.index] = value
        self.parent.value = tuple(new_parent_value)

    @property
    def color(self):
        return Color(*self.value)

    @color.setter
    def color(self, c):
        r, g, b = c
        self.value = (r, g, b)

    def on(self):
        self.value = (1, 1, 1)

    def off(self):
        self.value = (0, 0, 0)


class RGBXmasTree(SourceMixin, SPIDevice):
    def __init__(self, pixels=25, brightness=0.5, mosi_pin=12, clock_pin=25, *args, **kwargs):
        super(RGBXmasTree, self).__init__(mosi_pin=mosi_pin, clock_pin=clock_pin, *args, **kwargs)
        self._all = [Pixel(parent=self, index=i) for i in range(pixels)]
        self._value = [(0, 0, 0)] * pixels
        self.brightness = brightness
        self.off()

    def __len__(self):
        return len(self._all)

    def __getitem__(self, index):
        return self._all[index]

    def __iter__(self):
        return iter(self._all)

    @property
    def color(self):
        average_r = mean(pixel.color[0] for pixel in self)
        average_g = mean(pixel.color[1] for pixel in self)
        average_b = mean(pixel.color[2] for pixel in self)
        return Color(average_r, average_g, average_b)

    @color.setter
    def color(self, c):
        r, g, b = c
        self.value = ((r, g, b),) * len(self)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        max_brightness = 31
        self._brightness_bits = int(brightness * max_brightness)
        self._brightness = brightness
        self.value = self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        start_of_frame = [0]*4
        end_of_frame = [0]*5
                     # SSSBBBBB (start, brightness)
        brightness = 0b11100000 | self._brightness_bits
        pixels = [[int(255*v) for v in p] for p in value]
        pixels = [[brightness, b, g, r] for r, g, b in pixels]
        pixels = [i for p in pixels for i in p]
        data = start_of_frame + pixels + end_of_frame
        self._spi.transfer(data)
        self._value = value

    def on(self):
        self.value = ((1, 1, 1),) * len(self)

    def off(self):
        self.value = ((0, 0, 0),) * len(self)

    def close(self):
        super(RGBXmasTree, self).close()
        
    def setByIndicies(self, indicies, color):
        new_value = list(self.value)
        for index in indicies:
            new_value[index] = color
        self.value = tuple(new_value)
        
    def bottomRow(self, color):
        indicies = [0, 6, 7, 12, 15, 16, 19, 24]
        self.setByIndicies(indicies, color)
                
    def middleRow(self, color):
        indicies = [1, 5, 8, 11, 14, 17, 20, 23]
        self.setByIndicies(indicies, color)
                        
    def topRow(self, color):
        indicies = [2, 4, 9, 10, 13, 18, 21, 22]
        self.setByIndicies(indicies, color)    
                        
    def star(self, color):
        indicies = [3]
        self.setByIndicies(indicies, color)
        
    def bottomToTop(self, color):
        delay = 1
        self.off()
        self.bottomRow(color)
        sleep(delay)
        self.bottomRow((0,0,0))
        self.middleRow(color)
        sleep(delay)
        self.middleRow((0,0,0))
        self.topRow(color)
        sleep(delay)
        self.topRow((0,0,0))
        self.star(color)
        sleep(delay)

    def twinkle(self):
      for pixel in self:
        pixel.color = randomColor()

      for x in range(50):
        pixel = random.choice(self)
        pixel.color = randomColor()
        sleep(0.2)

if __name__ == '__main__':
    tree = RGBXmasTree()
    tree.on()
