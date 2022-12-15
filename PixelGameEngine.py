import pygame, sys, random, threading, math, os
from PIL import Image
import numpy as np
from collections import Counter
from typing import Callable, Iterable
from pygame.locals import *

class Color:
    WHITE = (255, 255, 255)
    GRAY = (192, 192, 192)
    DARK_GREY = (128, 128, 128)
    VERY_DARK_GRAY = (64, 64, 64)
    RED = (255, 0, 0)
    DARK_RED = (128, 0, 0)
    VERY_DARK_RED = (64, 0, 0)
    YELLOW = (255, 255, 0)
    DARK_YELLOW = (128, 128, 0)
    VERY_DARK_YELLOW = (64, 64, 0)
    ORANGE = (255, 165)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 128, 0)
    VERY_DARK_GREEN = (0, 64, 0)
    CYAN = (0, 255, 255)
    DARK_CYAN = (0, 128, 128)
    VERY_DARK_CYAN = (0, 64, 64)
    BLUE = (0, 0, 255)
    DARK_BLUE = (0, 0, 128)
    VERY_DARK_BLUE = (0, 0, 64)
    MAGENTA = (255, 0, 255)
    DARK_MAGENTA = (128, 0, 128)
    VERY_DARK_MAGENTA = (64, 0, 64)
    BLACK = (0, 0, 0)
    BLANK = (0, 0, 0, 0)

    def fromHex(hex: "RRGGBB(AA)"):
        pass
        
    
class Sprite:
    def __init__(self, imagePath):
        self.imagePath = imagePath
        self.image = Image.open(imagePath)
        self.height = self.image.size[1]
        self.width = self.image.size[0]
        self.loadedImage = self.image.load()
        self.generateArray()

    def generateArray(self):
        data = []
        for x in range(self.width):
            data.append([self.loadedImage[x, y] for y in range(self.height)])
        self.imageArray = data

    def replaceColor(self, color, withColor):
        data = self.image.getdata()
        newData = []
        for item in data:
            if item == color:
                newData.append(withColor)
            else:
                newData.append(item)

        self.image.putdata(newData)
        self.loadedImage = self.image.load()
        self.generateArray()

    def resizeImage(self, scale: float):
        pass
            
        


class PixelEngine:
    LetterWidths = {'a':8, 'b':8, 'c':8, 'd':8, 'e':8, 'f':8, 'g':8, 'h':8, 'i':6, 'j':8, 'k':8, 'l':8, 'm':10, 'n':8, 'o':8, 'p':8, 'q':8, 'r':8, 's':8, 't':10, 'u':8, 'v':10, 'w':10, 'x':8, 'y':10, 'z':8, '`':6, '1':6, '2':8, '3':8, '4':8, '5':8, '6':8, '7':8, '8':8, '9':8, '0':8, '-':6, '=':6, '~':8, '!':6, '@':10, '#':10, '$':10, '%':8, '^':6, '&':10, '*':6, '(':8, ')':8, '_':8, '+':6, '[':4, ']':4, '\\':8, '{':6, '}':6, '|':6, ';':6, "'":6, ':':6, '"':6, ',':6, '.':6, '/':8, '<':4, '>':4, '?':8}
    LetterOffsets = {'a': 0, 'b': 10, 'c': 20, 'd': 30, 'e': 40, 'f': 50, 'g': 60, 'h': 70, 'i': 80, 'j': 88, 'k': 98, 'l': 108, 'm': 118, 'n': 130, 'o': 140, 'p': 150, 'q': 160, 'r': 170, 's': 180, 't': 190, 'u': 202, 'v': 212, 'w': 224, 'x': 236, 'y': 246, 'z': 258, '`': 268, '1': 276, '2': 284, '3': 294, '4': 304, '5': 314, '6': 324, '7': 334, '8': 344, '9': 354, '0': 364, '-': 374, '=': 382, '~': 390, '!': 400, '@': 408, '#': 420, '$': 432, '%': 444, '^': 454, '&': 462, '*': 474, '(': 482, ')': 492, '_': 502, '+': 512, '[': 520, ']': 526, '\\': 532, '{': 542, '}': 550, '|': 558, ';': 566, "'": 574, ':': 582, '"': 590, ',': 598, '.': 606, '/': 614, '<': 624, '>': 630, '?': 636}

    def __init__(self, title, screen_height:int, screen_width:int, pixel_height:int, pixel_width:int, scaleing_factor:float=1, FPS=None, gamma=None):
        pygame.init()
        self.WINDOW_WIDTH = round(screen_width * scaleing_factor)
        self.WINDOW_HEIGHT = round(screen_height * scaleing_factor)
        
        self.PIXEL_HEIGHT = round(pixel_height * scaleing_factor)
        self.PIXEL_WIDTH = round(pixel_width * scaleing_factor)
        
        self.WINDOW_PIXEL_HEIGHT = math.ceil(self.WINDOW_HEIGHT / self.PIXEL_HEIGHT)
        self.WPH = self.WINDOW_PIXEL_HEIGHT
        self.WINDOW_PIXEL_WIDTH = math.ceil(self.WINDOW_WIDTH / self.PIXEL_WIDTH)
        self.WPW = self.WINDOW_PIXEL_WIDTH
        
        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption(title)

        
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.pixels = [[(0, 0, 0) for i in range(self.WINDOW_PIXEL_HEIGHT)] for j in range(self.WINDOW_PIXEL_WIDTH)]

        self.__keydown = False
        self.__isRunning = False
        self.__gamma = gamma
        self.events = {}
        
        self.FPS = FPS
        self.clock = pygame.time.Clock()

    def drawScreen(self, screen):
        for x in range(self.WINDOW_WIDTH):
            for y in range(self.WINDOW_HEIGHT):
                px = math.floor(x / self.PIXEL_WIDTH)
                py = math.floor(y / self.PIXEL_HEIGHT)
                self.WINDOW.set_at((x, y), screen[px][py])

    def Start(self, start: Callable=lambda x:1, update:Callable=lambda x:1, end:Callable=lambda x:1):
        start(self)
        self.__isRunning = True
        self.loop(update, end)
        end(self)
        pygame.quit()
        sys.exit()
        '''
        gl = threading.Thread(target=self.loop, args=(update, end))
        gl.start()
        '''
    
    def loop(self, update, end):
        while self.__isRunning:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == QUIT:
                    end(self)
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP:
                    self.__keydown = False
                elif event.type == KEYDOWN:
                    self.__keydown = True

                    
            self.__isRunning = update(self)

            self.drawScreen(self.pixels)
            pygame.display.update()
            if self.FPS is not None:
                self.clock.tick(self.FPS)

    def isInRange(self, point: Iterable[int]):
        return (point[0] < self.WPW and point[0] >= 0) and (point[1] < self.WPH and point[1] >= 0) 

    def isInRangeXY(self, x: int, y: int):
        return (x < self.WPW and x >= 0) and (y < self.WPH and y >= 0) 
  
    def isKeyDown(self):
        return self.__keydown
    
    def getKeyPressed(self):
        return pygame.key.get_pressed()

    def getKeyDown(self):
        for event in self.events:
            if event.type == KEYDOWN:
                return event.key
        return None

    def clearScreen(self):
        for x in range(self.WPW):
            for y in range(self.WPH):
                self.setPixelXY(x, y, self.BACKGROUND_COLOR)

    def setBackground(self, color: Iterable[int]):
        self.BACKGROUND_COLOR = color
        self.clearScreen()

    def setPixel(self, point: Iterable[int], color: Iterable[int]):
        if self.isInRangeXY(point[0], point[1]):
            if len(color) > 3:
                if color[3] == 255:
                    self.pixels[point[0]][point[1]] = color
                    return
            else:
                self.pixels[point[0]][point[1]] = color
                return
                
            ca = color[:3]
            cb = self.pixels[point[0]][point[1]]
            aa = color[3] / 255
            ab = cb[3] / 255 if len(cb) > 3 else 1
            ao = aa + ab * (1 - aa)
            cb = cb[:3]
            
            
            if self.__gamma is None:
                self.pixels[point[0]][point[1]] = tuple([(ca[i] * aa + cb[i] * ab * (1 - aa)) / ao for i in range(3)]) + (ao,)
            else:
                self.pixels[point[0]][point[1]] = tuple([math.pow((math.pow(ca[i], self.__gamma) * aa + math.pow(cb[i], self.__gamma) * ab * (1 - aa)) / ao, 1 / self.__gamma) for i in range(3)]) + (ao,)

    def setPixelXY(self, x: int, y: int, color: Iterable[int]):
        self.setPixel((x, y), color)
    
    def setThickPixelXY(self, xc: int, yc: int, color: Iterable[int], thickness: int=1):
        if thickness == 1:
            self.setPixelXY(xc, yc, color)
            return
        for x in range(xc - (thickness // 2), xc + math.ceil(thickness / 2)):
            for y in range(yc - (thickness // 2), yc + math.ceil(thickness / 2)):
                self.setPixelXY(x, y, color)
                
    def setThickPixel(self, point: Iterable[int], color: Iterable[int], thickness: int=1):
        self.setThickPixelXY(point[0], point[1], color, thickness)
    
    def drawLine(self, start: Iterable[int], end: Iterable[int], color: Iterable[int], thickness: int=1):

        x0 = round(start[0])
        x1 = round(end[0])
        y0 = round(start[1])
        y1 = round(end[1])
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)


        if dx == 0:
            m = math.inf
        else:
            m = dy / dx
        
        if ((x1 - x0) < 0 or (y1 -y0) < 0):
            if m < 1 and x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                dx = abs(x1 - x0)
                dy = abs(y1 - y0)
            if m > 1 and y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                dx = abs(x1 - x0)
                dy = abs(y1 - y0)

        if dx == 0:
            for y in range(y0, y1 + 1):
                self.setThickPixelXY(x0, y, color, thickness)
            return

        if dy == 0:
            for x in range(x0, x1 + 1):
                self.setThickPixelXY(x, y0, color, thickness)
            return
            
                
        
        flag = True
        
        self.setThickPixelXY(x0, y0, color, thickness)
        
        step = 1
        if x0 > x1 or y0 > y1:
            step = -1
    
        mm = False   
        if m < 1:
            x0, x1, y0, y1 = y0, y1, x0, x1
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            mm = True
            
        p0 = 2 * dx - dy
        x = x0
        y = y0
        
        for i in range(abs(y1 - y0)):
            if flag:
                x_previous = x0
                p_previous = p0
                p = p0
                flag = False
            else:
                x_previous = x
                p_previous = p
                
            if p >= 0:
                x = x + step
    
            p = p_previous + 2 * dx - 2 * dy * (abs(x - x_previous))
            y = y + 1
            
            if mm:
                self.setThickPixelXY(y, x, color, thickness)
            else:
                self.setThickPixelXY(x, y, color, thickness)
            
    def drawLineXY(self, x1: int, y1: int, x2: int, y2: int, color: Iterable[int], thickness: int=1):
        self.drawLine((x1, y1), (x2, y2), color, thickness)

    def drawRect(self, point: Iterable[int], size: Iterable[int], border_color: Iterable[int], border_width: int=1):
        tl = (point[0], point[1])
        tr = (point[0], point[1] + size[1])
        bl = (point[0] + size[0], point[1])
        br = (point[0] + size[0], point[1] + size[1])
        self.drawLine(tl, tr, border_color, border_width)
        self.drawLine(tr, br, border_color, border_width)
        self.drawLine(bl, br, border_color, border_width)
        self.drawLine(tl, bl, border_color, border_width)

    def drawRectXY(self, x: int, y: int, width: int, height: int, border_color: Iterable[int], border_width: int=1):
        self.drawRect((x, y), (width, height), border_color, border_width)

    def fillRect(self, point: Iterable[int], size: Iterable[int], color: Iterable[int], border_color: Iterable[int]=(0, 0, 0), border_width: int=0):
        for x in range(point[0], point[0] + size[0]):
            for y in range(point[1], point[1] + size[1]):
                if self.isInRangeXY(x, y):
                        self.setPixel((x, y), color)
        self.drawRect(point, size, border_color, border_width)

    def fillRectXY(self, x: int, y: int, width: int, height: int, color: Iterable[int], border_color: Iterable[int]=(0, 0, 0), border_width: int=0):
        for x1 in range(x, x + width):
            for y1 in range(y, y + height):
                if self.isInRangeXY(x1, y1):
                        self.setPixel((x1, y1), color)
        self.drawRect((x, y), (width, height), border_color, border_width)
        
    def drawCircle(self, center: Iterable[int], radius: int, color: Iterable[int], thickness: int=1):
        x = radius
        y = 0

        self.setThickPixelXY(center[0] + x, center[1] + y, color, thickness)

        if radius > 0:
            self.setThickPixelXY(center[0] - x, center[1] + y, color, thickness)
            self.setThickPixelXY(center[0] + y, center[1] + x, color, thickness)
            self.setThickPixelXY(center[0] + y, center[1] - x, color, thickness)


        P = 1 - radius
        
        while x > y:
            y += 1
            
            if P <= 0:
                P = P + 2 * y + 1
            else:        
                x -= 1
                P = P + 2 * y - 2 * x + 1

            if x < y:
                break
            
            self.setThickPixelXY(x + center[0], y + center[1], color, thickness)
            self.setThickPixelXY(-x + center[0], y + center[1], color, thickness)
            self.setThickPixelXY(x + center[0], -y + center[1], color, thickness)
            self.setThickPixelXY(-x + center[0], -y + center[1], color, thickness)

            if x != y:
                self.setThickPixelXY(y + center[0], x + center[1], color, thickness)
                self.setThickPixelXY(-y + center[0], x + center[1], color, thickness)
                self.setThickPixelXY(y + center[0], -x + center[1], color, thickness)
                self.setThickPixelXY(-y + center[0], -x + center[1], color, thickness)

    def drawCircleXY(self, x: int, y: int, radius: int, color: Iterable[int], thickness: int=1):
        self.drawCircle((x, y), radius, color, thickness)
    
    def fillCircle(self, center: Iterable[int], radius: int, color: Iterable[int], border_color: Iterable[int], border_width: int = 0):
        for x in range(center[0] - radius, center[0] + radius + 1):
            for y in range(center[1] - radius, center[1] + radius + 1):
                if ((x - center[0]) ** 2 + (y - center[1]) ** 2) < (radius ** 2):
                    if self.isInRangeXY(x, y):
                        self.setPixelXY(x, y, color)
        self.drawCircle(center, radius, border_color, border_width)

    def fillCircleXY(self, x: int, y: int, radius: int, color: Iterable[int], border_color: Iterable[int], border_width: int = 0):
        self.fillCircle((x, y), radius, color, border_color, border_width)

    def drawPolygon(self, color: Iterable[int], *corners: Iterable[int], thickness: int=1):
        if len(corners) < 1:
            return
        for i in range(len(corners)):
            self.drawLine(corners[i - 1], corners[i], color, thickness)

    def fillPolygon(self, color: Iterable[int], *corners: Iterable[int], border_color: Iterable[int]=(0, 0, 0), border_width: int=0):
        def getLineEdges(start, end):
            x0 = round(start[0])
            x1 = round(end[0])
            y0 = round(start[1])
            y1 = round(end[1])
            
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)

            points = []


            if dx == 0:
                m = math.inf
            else:
                m = dy / dx
            
            if ((x1 - x0) < 0 or (y1 -y0) < 0):
                if m < 1 and x0 > x1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                    dx = abs(x1 - x0)
                    dy = abs(y1 - y0)
                if m > 1 and y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                    dx = abs(x1 - x0)
                    dy = abs(y1 - y0)

            if dx == 0:
                for y in range(y0, y1 + 1):
                    points.append((x0, y))
                points.append((x1, y1))
                return points

            if dy == 0:
                return [(x0, y0), (x1, y1)]
                
            
            flag = True
            
            step = 1
            if x0 > x1 or y0 > y1:
                step = -1
        
            mm = False   
            if m < 1:
                x0, x1, y0, y1 = y0, y1, x0, x1
                dx = abs(x1 - x0)
                dy = abs(y1 - y0)
                mm = True

            
                
            p0 = 2 * dx - dy
            x = x0
            y = y0
            
            for i in range(abs(y1 - y0)):
                if flag:
                    x_previous = x0
                    p_previous = p0
                    p = p0
                    flag = False
                else:
                    x_previous = x
                    p_previous = p
                    
                if p >= 0:
                    x = x + step
        
                p = p_previous + 2 * dx - 2 * dy * (abs(x - x_previous))
                y = y + 1
                
                if mm:
                    if x != x_previous:
                        points.append((y, x))
                else:
                    points.append((x, y))

            return points
        def getPolygonEdges(*points):
            if len(points) < 1:
                return []
            edges = []
            for i in range(len(points)):
                edges.extend(getLineEdges(points[i - 1], points[i]))
            for point in corners:
                edges.append(point)
            return edges

        edges = getPolygonEdges(*corners)
		#print(dict(Counter([item for item in list(map(lambda point: point if point[1] == 15 else None, edges)) if item is not None])))
        minx = min(map(lambda x: x[0], corners))
        maxx = max(map(lambda x: x[0], corners))
        miny = min(map(lambda x: x[1], corners))
        maxy = max(map(lambda x: x[1], corners))
        for y in range(miny + 1, maxy):
            inside = False
            for x in range(minx, maxx):
                if (x, y) in edges:
                    if edges.count((x, y)) & 1 == 1:
                        inside = not inside
                if inside:
                    self.setPixel((x, y), color)
        
        if border_width > 0:
            self.drawPolygon(border_color, *corners, thickness=border_width)
        else:
            self.drawPolygon(color, *corners, thickness=border_width)
        #for point in edges:
        #    self.setPixel(point, (0, 255, 0))
        #for point in corners:
        #    self.setPixel(point, (0, 0, 255))
        return

    def drawBezierCurve(self, color: Iterable[int], *points: Iterable[int], thickness: int=1, accuracy: int=10000):
        Ubound = len(points) - 1
        binom = lambda n, k: math.factorial(n) / (math.factorial(k) * (math.factorial(n - k)))
        fbezier = lambda t, x_or_y: sum([binom(Ubound, n) * (1 - t)**(Ubound - n) * (t**n) * (points[n + 0][x_or_y]) for n in range(0, Ubound + 1)])
        Vbezier = lambda t: list((fbezier(t, 0), fbezier(t, 1)))

        edges = set()
        for t in range(0, accuracy + 1):
            p = tuple(map(round, Vbezier(t / accuracy)))
            edges.add(p)
        
        for point in edges:
            self.setThickPixel(point, color, thickness)

    def drawFunction(self, function: Callable, color: Iterable[int], thickness: int=1, minX=None, maxX=None, minY=None, maxY=None):
        for x in range(0 if minX is None else minX, (self.WPW if maxX is None else maxX) + 1):
            ys = function(x)
            if hasattr(ys, '__iter__'):
                for y in ys:
                    if y >= (0 if minY is None else minY) and y < ((self.WPH + 1) if maxY is None else maxY):
                        self.setThickPixelXY(x, round(y), color, thickness)
            else:
                if y >= (0 if minY is None else minY) and y < ((self.WPH + 1) if maxY is None else maxY):
                    self.setThickPixelXY(x, round(ys), color, thickness)

    def drawString(self, string: str, point: Iterable[int], color: Iterable[int], scale: float=1):
        text = Sprite('Font.png')
        if color != (0, 0, 0, 255):
            text.replaceColor((0, 0, 0, 255), color)
        letterOffset = 0
        lineOffset = 0
        for letter in string.lower():
            if letter in self.LetterWidths.keys():
                self.drawPartialSprite(text, (point[0] + letterOffset, point[1] + lineOffset), self.LetterOffsets[letter], 0, self.LetterWidths[letter], 10)
                letterOffset += self.LetterWidths[letter] + 2
            else:
                if letter == ' ':
                    letterOffset += 4
                if letter == '\n':
                    lineOffset += 12
                    letterOffset = 0

    def drawSprite(self, sprite: Sprite, point: Iterable[int], scale: float=1):
        spriteArray = sprite.imageArray
        for y in range(sprite.height):
            for x in range(sprite.width):
                self.setPixelXY(x + point[0], y + point[1], spriteArray[x][y])
    
    def drawPartialSprite(self, sprite: Sprite, startingPoint: Iterable[int], ox: int, oy:int, w: int, h: int, scale: float=1):
        spriteArray = sprite.imageArray
        for y in range(h):
            for x in range(w):
                self.setPixelXY(x + startingPoint[0], y + startingPoint[1], spriteArray[x + ox][y + oy])
    # TODO text, sprite, color class
        