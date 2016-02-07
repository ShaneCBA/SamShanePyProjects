import wx
import time

WIDTH, HEIGHT = 1225, 650
global keys
keys = {83:False,87:False,65:False,68:False}
framerefresh = 17
class GameObject(object):
    def __init__(self, x, y, width, height):
        self.coords, self.dimensions = [x, y], [width, height]
    def isTouching(self, compareTo): 
        if self == compareTo:
            return False
        for c in [0, 1]:
            return self.coords[0] < (compareTo.coords[0] + compareTo.dimensions[0]) and (self.coords[0] + self.dimensions[0]) > compareTo.coords[0] and self.coords[1] < (compareTo.coords[1] + compareTo.dimensions[1]) and (self.coords[1] + self.dimensions[1]) > compareTo.coords[1]
        
class Drawable(GameObject):
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
    def addObject(self, toAdd):
        self.contents.append(toAdd)  
        return self.contents[-1]
    
    def keyDown(self,event):
        keys[event.GetKeyCode()] = True
    
    def keyUp(self,event):
        keys[event.GetKeyCode()] = False
        
    def drawObjects(self, event):
        dc = wx.BufferedPaintDC(self)
        filtered = filter(lambda x: hasattr(x, "color"), self.contents)
        dc.SetBackground(wx.Brush("#2A4152", wx.SOLID))
        dc.Clear()
        for o in range(len(filtered)):
            filtered[o].draw(dc)
        dc.Refresh()
class Moveable(Drawable):
    def __init__(self, x, y, width, height, color, borderColor = "#FFFFFF", borderWidth = 2):
        super(Moveable, self).__init__(x, y, width, height, color, [borderColor if borderColor else color, borderWidth])
        self.velocity = [1, 0]
    def move(self):
        #self.coords = map(sum, zip(move * 2, self.coords))                    
        
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
                print "True"
        return 0
class Obstacle(Drawable):
    def __init__(self, x, y, width, height, color, borderColor="#EEEEEE", borderWidth=2):
        super(Obstacle, self).__init__(x, y, width, height, color, [borderColor, borderWidth])
class Rocket(Moveable):
    def __init__(self,x,y,width,height,color):
        super(Rocket, self).__init__(x,y,width,height,color)

app = wx.App(redirect=False)
thingy = Window(None, -1, 'Client', WIDTH, HEIGHT)
w,h = thingy.GetSize()
obstacles=[]
thingy.statusbar.SetStatusText(str(w))
obstacles.append(thingy.board.addObject(Obstacle(60,180,20,240,"#A13437")))
obstacles.append(thingy.board.addObject(Obstacle(1120,180,20,240,"#238C6F")))
thingy.board.addObject(Moveable(1166,0,30,30,"#35D4A8"))
app.MainLoop()
