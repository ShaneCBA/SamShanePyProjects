import wx
import time
from math import copysign
from operator import mul
from functools import partial
WIDTH, HEIGHT = 1200, 600
global keys
keys = {83: [False, 0],
        87: [False, 0],
        65: [False, 0],
        68: [False, 0]}
FRICTION = 1
TICKRATE = 17
CLIENT_LOCAL = 0
CLIENT_SHARED = 1
SERVER = 2
velocityCurve = lambda x: copysign(min((4*x/17)**2, 7),x)
filterByAttribute = lambda x, a: filter(lambda z: hasattr(z, x), a)
def converge(f, t, s):
    if f < t:
        return f+s if f+s < t else t
    elif f > t:
        return f-s if f-s > t else t
    return t
def diverge(f, a, s):
    if f < t:
        return f - s
    return f + s
deAccel = partial(converge, t = 0, s = FRICTION)

class GameObject(object):
    def __init__(self, mode):
        self.mode = mode

class PhysicalObject(GameObject):
    def __init__(self, x, y, width, height, collide = True, mode = CLIENT_SHARED):
        super(PhysicalObject, self).__init__(mode)
        self.coords, self.dimensions, self.collide = [x, y, x + width, y + height], [width, height], collide
    def isTouching(self, compareTo):
        if self == compareTo:
            return False
        for c in [0, 1]:
            return self.coords[0] < compareTo.coords[0] + compareTo.dimensions[0] and self.coords[0] + self.dimensions[0] > compareTo.coords[0] and self.coords[1] < compareTo.coords[1] + compareTo.dimensions[1] and self.coords[1] + self.dimensions[1] > compareTo.coords[1]
        
class Drawable(PhysicalObject):
    def __init__(self, x, y, width, height, color, border, collide = True, mode = CLIENT_SHARED):
        super(Drawable, self).__init__(x, y, width, height, collide, mode)
        self.color = color
        self.border = border #[color, width] *Temporary
    def draw(self, dc):
        pen = wx.Pen(self.border[0], self.border[1], wx.SOLID)
        dc.SetPen(pen)#.SetJoin(wx.JOIN_MITER))
        dc.SetBrush(wx.Brush(self.color, wx.SOLID))
        dc.DrawRectangle(self.coords[0]+self.border[1], self.coords[1]+self.border[1], self.dimensions[0], self.dimensions[1])
class Window(wx.Frame):
    def __init__(self, parent, id, title, x, y):
        wx.Frame.__init__(self, parent, id, title, size=(x, y),  style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('0')
        self.board = Board(self)
        self.SetBackgroundColour("#2A4152")#00F9FF
        self.Centre()
        self.Show(True)

class Board(wx.Panel):
    TIMER_ID = 42
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        
        self.timer = wx.Timer(self,  Board.TIMER_ID)
        self.timer.Start(TICKRATE)
        self.Bind(wx.EVT_TIMER, self.onTimer, id=Board.TIMER_ID)
        
       # wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        self.contents = []
        self.Bind(wx.EVT_PAINT, self.drawObjects)
        
        self.Bind(wx.EVT_KEY_DOWN , self.keyDown)
        self.Bind(wx.EVT_KEY_UP , self.keyUp)
        
        self.player = self.addObject(Moveable(10, 10, 10, 10, 'red'))  
    def onTimer(self, event):
        self.GetEventHandler().ProcessEvent(wx.PaintEvent( ))
        for k in keys: 
            if keys[k][0]:
                keys[k][1] += 1
            else:
                keys[k][1] = 0
        self.moveObjects()
    def addObject(self, toAdd):
        self.contents.append(toAdd)  
        return self.contents[-1]
    
    def keyDown(self,event):
        keys[event.GetKeyCode()][0] = True
    
    def keyUp(self,event):
        keys[event.GetKeyCode()][0] = False
    def drawObjects(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        for o in filterByAttribute("color", self.contents):
            o.draw(dc)
    def moveObjects(self):
        for o in filterByAttribute("velocity", self.contents):
            o.move(filterByAttribute("collide", self.contents))
class Moveable(Drawable):
    def __init__(self, x, y, width, height, color, borderColor = None, borderWidth = 2):
        super(Moveable, self).__init__(x, y, width, height, color, [borderColor if borderColor else color, borderWidth])
        self.velocity = [0, 0]
    def move(self, toCheck):
        self.updateVelocity()
        #print self.velocity
        #print self.coords
        self.coords = map(sum, zip(self.coords, self.velocity))
        if toCheck:
            for o in toCheck:
                if self.isTouching(o):
                    #print self.velocity
                    self.velocity = map(lambda x: copysign(abs(x) * 2 + 2, x), self.velocity)
                    #print self.velocity
                    self.move(toCheck)
                    break
        return
    def updateVelocity(self):
        self.velocity[0] = velocityCurve(keys[68][1] - keys[65][1]) if keys[68][0] or keys[65][0] else deAccel(self.velocity[0])
        self.velocity[1] = velocityCurve(keys[83][1] - keys[87][1]) if keys[83][0] or keys[87][0] else deAccel(self.velocity[1])
class Obstacle(Drawable):
    def __init__(self, x, y, width, height, color, border = None):
        super(Obstacle, self).__init__(x, y, width, height, color, border if border else [color, 2])


app = wx.App()
thingy = Window(None, -1, 'Client', WIDTH, HEIGHT)
w,h = thingy.GetSize()
thingy.statusbar.SetStatusText(str(w))
thingy.board.addObject(Obstacle(40,(h/2)-30,30,30,"#8F70FF", ["#DDDDDD", 2]))
thingy.board.addObject(Obstacle(w-40-30,(h/2)-30,30,30,"#26FC14", ["#FFFFFF", 2]))
app.MainLoop()
