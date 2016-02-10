import wx
import time
import thread
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
TICKRATE = 10
CLIENT_LOCAL = 0
CLIENT_SHARED = 1
SERVER = 2
fireCodes = {wx.WXK_LEFT: 1,
             wx.WXK_RIGHT: 0,
             wx.WXK_UP: 3,
             wx.WXK_DOWN: 2}
fireDirections = [[1, 0], [-1, 0], [0, 1], [0, -1]]

velocityCurve = lambda x: copysign(min((4*x/13)**2, 7),x)
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
        self.die = False
    def kill(self):
        self.die = True

class PhysicalObject(GameObject):
    def __init__(self, x, y, width, height, collide = True, mode = CLIENT_SHARED):
        super(PhysicalObject, self).__init__(mode)
        self.coords, self.dimensions, self.collide = [x, y, x + width, y + height], [width, height], collide
    def isTouching(self, compareTo):
        if self == compareTo:
            return False
        return self.coords[0] < compareTo.coords[2] and self.coords[2] > compareTo.coords[0] and self.coords[1] < compareTo.coords[3] and self.coords[3] > compareTo.coords[1]
        
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
        self.contents = []
        self.Bind(wx.EVT_PAINT, self.drawObjects)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_KEY_DOWN , self.keyDown)
        self.Bind(wx.EVT_KEY_UP , self.keyUp)
        self.onSize(None)
        self.timer = wx.Timer(self,  Board.TIMER_ID)
        self.timer.Start(TICKRATE)
        self.Bind(wx.EVT_TIMER, self.onTimer, id=Board.TIMER_ID)
        self.rocket = None
        self.player = self.addObject(Moveable(0, 0, 30, 30, "#D9756D", "#DDDDDD", 2))
    def onSize(self, event):
        size = self.ClientSize
        self.buffer = wx.EmptyBitmap(*size)
    def onTimer(self, event):
        for o in filter(lambda x: x.die == True, self.contents):
            if o == self.rocket:
                self.rocket = None
            self.contents.remove(o)

        for k in keys: 
            if keys[k][0]:
                keys[k][1] += 1
            else:
                keys[k][1] = 0
        self.moveObjects()
        self.Refresh(eraseBackground=False)
        self.Update()
    def addObject(self, toAdd):
        self.contents.append(toAdd)  
        return self.contents[-1]
    
    def keyDown(self,event):
        if event.GetKeyCode() in keys:
            keys[event.GetKeyCode()][0] = True
        if event.GetKeyCode() in fireCodes:
            if self.rocket == None:
                self.rocket = self.addObject(Rocket(self.player.coords[0] + self.player.dimensions[0] / 2, self.player.coords[1] + self.player.dimensions[1] / 2, fireCodes[event.GetKeyCode()], CLIENT_SHARED))
    def keyUp(self,event):
        if event.GetKeyCode() in keys:
            keys[event.GetKeyCode()][0] = False
    def drawObjects(self, event):
        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)
        dc.Clear()
        dc.SetBackground(wx.Brush("#2A4152", wx.SOLID))
        for o in filterByAttribute("color", self.contents):
            o.draw(dc)
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("#2A4152", wx.SOLID))
        dc.DrawBitmap(self.buffer, 0, 0)
        dc.SetBackground(wx.Brush("#2A4152", wx.SOLID))
    def moveObjects(self):
        for o in filterByAttribute("velocity", self.contents):
            o.move(filterByAttribute("collide", self.contents), self.player)
class Moveable(Drawable):
    def __init__(self, x, y, width, height, color, borderColor = None, borderWidth = 2, mode = CLIENT_SHARED):
        super(Moveable, self).__init__(x, y, width, height, color, [borderColor if borderColor else color, borderWidth], mode)
        self.velocity = [0, 0]
    def move(self, toCheck, player):
        self.updateVelocity()
        oldCoords = self.coords[:]
        self.coords = map(sum, zip(self.coords, self.velocity * 2))
        if toCheck:
            for o in toCheck:
                while self.isTouching(o) and type(o) != Rocket:
                    self.velocity = map(partial(converge, t=0, s=0.2), self.velocity)
                    self.coords = oldCoords[:]
                    self.coords = map(sum, zip(self.coords, self.velocity * 2))
        return
    def updateVelocity(self):
        self.velocity[0] = velocityCurve(keys[68][1] - keys[65][1]) if keys[68][0] or keys[65][0] else deAccel(self.velocity[0])
        self.velocity[1] = velocityCurve(keys[83][1] - keys[87][1]) if keys[83][0] or keys[87][0] else deAccel(self.velocity[1])
class Obstacle(Drawable):
    def __init__(self, x, y, width, height, color, border = None):
        super(Obstacle, self).__init__(x, y, width, height, color, border if border else [color, 2])


class Rocket(Moveable):
    def __init__(self, x, y, direction, mode = CLIENT_SHARED):
        super(Rocket, self).__init__(x, y, 3, 3, 'red', mode = mode)
        self.direction = direction
        self.alive = 0
    def move(self, toCheck, player):
        self.alive += 1
        if self.alive > 180:
            self.kill()
        self.coords = map(sum, zip(self.coords, map(lambda x: apply(mul, x), zip(fireDirections[self.direction], [9] * 2)) * 2))
        if toCheck:
            for o in toCheck:
                if o != player and self.isTouching(o):
                    self.kill()
                    break
app = wx.App()
appWindow = Window(None, -1, 'Client', WIDTH, HEIGHT)
w,h = appWindow.GetSize()
appWindow.statusbar.SetStatusText(str(w))
appWindow.board.addObject(Obstacle(60,180,20,240,color="#A13437"))
appWindow.board.addObject(Obstacle(1120,180,20,240,color="#238C6F"))
app.MainLoop()
