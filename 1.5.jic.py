import wx
import time
WIDTH, HEIGHT = 1200, 600
global keys
keys = {83: [False, 0],
        87: [False, 0],
        65: [False, 0],
        68: [False, 0]}
TICKRATE = 17
CLIENT_LOCAL = 0
CLIENT_SHARED = 1
SERVER = 2
velocityCurve = lambda x: min((4*x/9)**2, 7)
filterByAttribute = lambda x, a: filter(lambda z: hasattr(z, x), a)
def converge(f, t, s):
    if f < s:
        return f+s if f+s < s else s
    elif f > s:
        return f-s if f-s > s else s
    return s

class GameObject(object):
    def __init__(self, mode):
        self.mode = mode

class PhysicalObject(GameObject):
    def __init__(self, x, y, width, height, collide = True, mode = CLIENT_SHARED):
        super(PhysicalObject, self).__init__(mode)
        self.coords, self.dimensions, self.collide = [[x, y], [x + width, y + height]], [width, height], collide
    def isTouching(self, compareTo): 
        for c in [0, 1]:
            if compareTo.coords[0][0] < self.coords[c][0] < compareTo.coords[1][0] and compareTo.coords[0][1] < self.coords[c][1] < compareTo.coords[1][1]:
                    return True
        return False
        
class Drawable(PhysicalObject):
    def __init__(self, x, y, width, height, color, border, collide = True, mode = CLIENT_SHARED):
        super(Drawable, self).__init__(x, y, width, height, collide, mode)
        self.color = color
        self.border = border #[color, width] *Temporary
    def draw(self, dc):
        pen = wx.Pen(self.border[0], self.border[1], wx.SOLID)
        dc.SetPen(pen)#.SetJoin(wx.JOIN_MITER))
        dc.SetBrush(wx.Brush(self.color, wx.SOLID))
        
        dc.DrawRectangle(self.coords[0][0]+self.border[1], self.coords[0][1]+self.border[1], self.dimensions[0], self.dimensions[1])
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
        for k in keys.values(): 
            if k[0]:
                k[1] = velocityCurve(k[1])
            else:
                k[1] = converge(k[1], 0, 1)
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
            o.move((lambda x: x.collide == True)(filterByAttribute("coords", self.contents)))
class Moveable(Drawable):
    def __init__(self, x, y, width, height, color, borderColor = None, borderWidth = 2):
        super(Moveable, self).__init__(x, y, width, height, color, [borderColor if borderColor else color, borderWidth])
        self.velocity = [1, 0]
    def move(self, toCheck):
        oldCoords = self.coords
        self.coords = map(sum, zip(self.coords, self.velocity * 2))
        for o in toCheck:
            if self.IsTouching(o):
                self.coords = oldCoords
                break
        return
class Obstacle(Drawable):
    def __init__(self, x, y, width, height, color, ):
        super(Obstacle, self).__init__(x, y, width, height, color, [color, 2])


app = wx.App()
thingy = Window(None, -1, 'Client', WIDTH, HEIGHT)
w,h = thingy.GetSize()
print w, h
thingy.statusbar.SetStatusText(str(w))
thingy.board.contents.append(Drawable(40,(h/2)-30,30,30,"#8F70FF", ["#DDDDDD", 2]))
thingy.board.contents.append(Drawable(w-40-30,(h/2)-30,30,30,"#26FC14", ["#FFFFFF", 2]))
app.MainLoop()
