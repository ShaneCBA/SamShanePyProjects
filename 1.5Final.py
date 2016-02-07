import wx
import time
from math import copysign
from operator import mul
from functools import partial

WIDTH, HEIGHT = 1205, 650

keys = {83:False,
        87:False,
        65:False,
        68:False}

fireCodes = {wx.WXK_LEFT: 1,
             wx.WXK_RIGHT: 0,
             wx.WXK_UP: 2,
             wx.WXK_DOWN: 3}
fireDirections = [[1, 0], [-1, 0], [0, 1], [0, -1]]

velocityCurve = lambda x: copysign(min((4*x/17)**2, 7),x)
filterByAttribute = lambda x, a: filter(lambda z: hasattr(z, x), a)

CLIENT_LOCAL = 0
CLIENT_SHARED = 1

framerefresh = 17

class GameObject(object):
    def __init__(self, mode):
        self.mode = mode
        self.die = True
    def kill(self):
        self.die = False
        
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
    def __init__(self, x, y, width, height, color, border):
        super(Drawable, self).__init__(x, y, width, height)
        self.color = color
        self.border = border #[color, width] *Temporary
    def draw(self, dc):
        pen = wx.Pen(self.border[0], self.border[1], wx.SOLID)
        dc.SetPen(pen)#.SetJoin(wx.JOIN_MITER))
        dc.SetBrush(wx.Brush(self.color, wx.SOLID))
        dc.DrawRectangle(self.coords[0]+self.border[1], self.coords[1]+self.border[1], self.dimensions[0]-self.border[1], self.dimensions[1]-self.border[1])
        
class Window(wx.Frame):
    def __init__(self, parent, id, title, width, height):
        wx.Frame.__init__(self, parent, id, title, size=(width, height),  style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
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
        self.timer.Start(framerefresh)
        self.Bind(wx.EVT_TIMER, self.onTimer, id=Board.TIMER_ID)
        
       #wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        self.contents = []
        self.Bind(wx.EVT_PAINT, self.drawObjects)
        self.SetBackgroundColour("#2A4152")#00F9FF
        
        self.Bind(wx.EVT_KEY_DOWN , self.keyDown)
        self.Bind(wx.EVT_KEY_UP , self.keyUp)
        
        self.player = self.addObject(Moveable(0, 0, 30, 30, "#D9756D", "#DDDDDD", 2))  
        self.Refresh()
    def onTimer(self, event):
        self.GetEventHandler().ProcessEvent(wx.PaintEvent( ))
        self.player.move()
        self.moveObjects()
    def addObject(self, toAdd):
        self.contents.append(toAdd)  
        return self.contents[-1]
            
    def keyDown(self,event):
        if event.GetKeyCode() in keys:
            keys[event.GetKeyCode()] = True
        if event.GetKeyCode() in fireCodes:
            print "rocket"
            rx = self.player.coords[0] + ((self.player.dimensions[0] / 2) * fireDirections[fireCodes[event.GetKeyCode()]][0])
            ry = self.player.coords[1] + ((self.player.dimensions[1] / 2) * fireDirections[fireCodes[event.GetKeyCode()]][1])
            print fireCodes[event.GetKeyCode()]
            self.addObject(Rocket(rx, ry, "#FF00FF", fireCodes[event.GetKeyCode()]))#self,x,y,color,direction
            print "rocket2"
    def keyUp(self,event):
        if event.GetKeyCode() in keys:
            keys[event.GetKeyCode()] = False
    def drawObjects(self, event):
        dc = wx.BufferedPaintDC(self)
        filtered = filter(lambda x: hasattr(x, "color"), self.contents)
        dc.SetBackground(wx.Brush("#2A4152", wx.SOLID))
        dc.Clear()
        for o in self.contents:
            o.draw(dc)
        dc.Refresh()
    def moveObjects(self):
        for o in filterByAttribute("velocity", self.contents):
            o.move(filterByAttribute("collide", self.contents))
class Moveable(Drawable):
    def __init__(self, x, y, width, height, color, borderColor = "#FFFFFF", borderWidth = 2):
        super(Moveable, self).__init__(x, y, width, height, color, [borderColor if borderColor else color, borderWidth])
        self.velocity = [0, 0]
    def move(self,toCheck=None):
        #self.coords = map(sum, zip(move * 2, self.coords))   
        oldPos = self.coords  [:]              
        if toCheck == None:
            toCheck = obstacles
        velX = self.velocity[0]
        velY = self.velocity[1]
        
        if (velX > 0):self.velocity[0] -=1
        if (velX < 0):self.velocity[0] +=1
        if (velY > 0):self.velocity[1] -=1
        if (velY < 0):self.velocity[1] +=1
            
        if(keys[87]):self.velocity[1] = -10#UP
        if(keys[83]):self.velocity[1] = 10#DOWN
        if(keys[65]):self.velocity[0] = -10#LEFT
        if(keys[68]):self.velocity[0] = 10#RIGHT
        
        self.coords[0] = self.coords[0] + self.velocity[0]
        self.coords[1] = self.coords[1] + self.velocity[1]
        
        for o in range(len(obstacles)):
            if self.isTouching(obstacles[o]):
                obj = obstacles[o]
                x1 = (self.coords[0] < obj.coords[0]) and ((self.coords[0]+self.dimensions[0]) > obj.coords[0])
                x2 = (self.coords[0] < (obj.coords[0] + obj.dimensions[0])) and ((self.coords[0]+self.dimensions[0]) > (obj.coords[0] + obj.dimensions[0]))
                y1 = (self.coords[1] < obj.coords[1]) and ((self.coords[1]+self.dimensions[1]) > obj.coords[1])
                y2 = (self.coords[1] < (obj.coords[1] + obj.dimensions[1])) and ((self.coords[1]+self.dimensions[1]) > (obj.coords[1] + obj.dimensions[1]))
                while (self.coords[1] < obj.coords[1]) and ((self.coords[1]+self.dimensions[1]) > obj.coords[1]):# |;
                    self.coords[1] -= 1
                while (self.coords[1] < (obj.coords[1] + obj.dimensions[1])) and ((self.coords[1]+self.dimensions[1]) > (obj.coords[1] + obj.dimensions[1])):# ;|
                    self.coords[1] += 1
                while (self.coords[0] < obj.coords[0]) and ((self.coords[0]+self.dimensions[0]) > obj.coords[0]):# |;
                    self.coords[0] -= 1
                while (self.coords[0] < (obj.coords[0] + obj.dimensions[0])) and ((self.coords[0]+self.dimensions[0]) > (obj.coords[0] + obj.dimensions[0])):# ;|
                    self.coords[0] += 1
        return 0
class Obstacle(Drawable):
    def __init__(self, x, y, width, height, color, borderColor="#EEEEEE", borderWidth=2):
        super(Obstacle, self).__init__(x, y, width, height, color, [borderColor, borderWidth])
class Rocket(Moveable):
    mode = CLIENT_SHARED
    def __init__(self,x,y,color,direction):
        super(Rocket, self).__init__(x,y,3,3,color,CLIENT_SHARED)#self, x, y, width, height, color, borderColor = "#FFFFFF", borderWidth = 2
        print 'gottablast'
        self.direction = direction
        self.velocity[0] = fireDirections[self.direction][0]*7
        self.velocity[1] = fireDirections[self.direction][1]*7
    def move(self, toCheck=None):
        if toCheck == None:
            toCheck = obstacles
        #self.coords = map(sum, zip(self.coords, map(mul, zip(fireDirections[self.direction], [velocityCurve(4)] * 2))))
        self.coords[0] += self.velocity[0]
        self.coords[1] += self.velocity[1]
        if toCheck:
            for o in toCheck:
                if self.isTouching(o):
                    print 'eh'
                    self.kill()
                    break
app = wx.App(redirect=False)
thingy = Window(None, -1, 'Client', WIDTH, HEIGHT)

obstacles=[]

thingy.statusbar.SetStatusText(str(WIDTH))

obstacles.append(thingy.board.addObject(Obstacle(60,180,20,240,"#A13437")))
obstacles.append(thingy.board.addObject(Obstacle(1120,180,20,240,"#238C6F")))
thingy.board.addObject(Moveable(1166,0,30,30,"#35D4A8"))
app.MainLoop()
