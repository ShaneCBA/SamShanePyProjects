import wx
import time
from math import copysign
from operator import mul
from functools import partial
WIDTH, HEIGHT = 1250, 600
global keys
keys = {83:False,87:False,65:False,68:False}
class GameObject(object):
    def __init__(self, x, y, width, height):
        self.coords, self.dimensions = [[x, y], [x + width, y + height]], [width, height]
    def isTouching(self, compareTo): 
        for c in [0, 1]:
            if compareTo.coords[0][0] < self.coords[c][0] < compareTo.coords[1][0] and compareTo.coords[0][1] < self.coords[c][1] < compareTo.coords[1][1]:
                    return True
        return False
        
class Drawable(GameObject):
    def __init__(self, x, y, width, height, color, border):
        super(Drawable, self).__init__(x, y, width, height)
        self.color = color
        self.border = border #[color, width] *Temporary
    def draw(self, dc):
        pen = wx.Pen(self.border[0], self.border[1], wx.SOLID)
        dc.SetPen(pen)#.SetJoin(wx.JOIN_MITER))
        dc.SetBrush(wx.Brush(self.color, wx.SOLID))
        dc.DrawRectangle(self.coords[0][0]+self.border[1], self.coords[0][1]+self.border[1], self.dimensions[0]-self.border[1], self.dimensions[1]-self.border[1])
class Window(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1200, 650),  style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
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
        self.timer.Start(25)
        self.Bind(wx.EVT_TIMER, self.onTimer, id=Board.TIMER_ID)
        
       #wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        self.contents = []
        self.Bind(wx.EVT_PAINT, self.drawObjects)
        self.SetBackgroundColour("#2A4152")#00F9FF
        
        self.Bind(wx.EVT_KEY_DOWN , self.keyDown)
        self.Bind(wx.EVT_KEY_UP , self.keyUp)
        
        self.player = self.addObject(Moveable(0, 0, 30, 30, "#D9756D", "#DDDDDD", 2))  
    def onTimer(self, event):
        self.GetEventHandler().ProcessEvent(wx.PaintEvent( ))
        self.player.move()
        self.Refresh()
    def addObject(self, toAdd):
        self.contents.append(toAdd)  
        return self.contents[-1]
    
    def keyDown(self,event):
        keys[event.GetKeyCode()] = True
    
    def keyUp(self,event):
        keys[event.GetKeyCode()] = False
        
    def drawObjects(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        filtered = filter(lambda x: hasattr(x, "color"), self.contents)
        for o in range(len(filtered)):
            filtered[o].draw(dc)
class Moveable(Drawable):
    def __init__(self, x, y, width, height, color, borderColor = "#FFFFFF", borderWidth = 2):
        super(Moveable, self).__init__(x, y, width, height, color, [borderColor if borderColor else color, borderWidth])
        self.velocity = [1, 0]
    def move(self):
        #self.coords = map(sum, zip(move * 2, self.coords))
        velX = self.velocity[0]
        velY = self.velocity[1]
        
        if (velX > 0):
            self.velocity[0] -=1
        if (velX < 0):
            self.velocity[0] +=1
        if (velY > 0):
            self.velocity[1] -=1
        if (velY < 0):
            self.velocity[1] +=1
            
        if(keys[87]):#UP
            self.velocity[1] = -10
            
        if(keys[83]):#DOWN
            self.velocity[1] = 10
        
        if(keys[65]):#LEFT
            self.velocity[0] = -10
            
        if(keys[68]):#RIGHT
            self.velocity[0] = 10
        
        x,y = self.coords[0]
        x2,y2 = self.coords[1]
        
        self.coords[0][0] = self.coords[0][0] + self.velocity[0]
        self.coords[0][1] = self.coords[0][1] + self.velocity[1]
        self.coords[1][0] = self.coords[1][0] + self.velocity[0]
        self.coords[1][1] = self.coords[1][1] + self.velocity[1]
        return 0
class Obstacle(Drawable):
    def __init__(self, x, y, width, height, color, borderColor="#EEEEEE", borderWidth=2):
        super(Obstacle, self).__init__(x, y, width, height, color, [borderColor, borderWidth])


app = wx.App()
thingy = Window(None, -1, 'Client')
w,h = thingy.GetSize()
thingy.statusbar.SetStatusText(str(w))
thingy.board.addObject(Obstacle(60,180,20,240,"#A13437"))
thingy.board.addObject(Obstacle(1120,180,20,240,"#238C6F"))
thingy.board.addObject(Moveable(1166,0,30,30,"#35D4A8"))
app.MainLoop()
