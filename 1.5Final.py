import wx
import time
class GameObject(object):
    def __init__(self, x, y, width, height):
        self.coords, self.velocity, self.dimensions = [[x, y], [x + width, y + height]], [0, 0], [width, height]
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
        #print pen.GetJoin()
        dc.SetPen(pen)#.SetJoin(wx.JOIN_MITER))
        dc.SetBrush(wx.Brush(self.color, wx.SOLID))
        dc.DrawRectangle(self.coords[0][0]+self.border[1], self.coords[0][1]+self.border[1], self.dimensions[0], self.dimensions[1])
        
class Window(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1200, 600),  style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('0')
        self.board = Board(self)
        self.SetBackgroundColour("#00F9FF")
        self.Centre()
        self.Show(True)

class Board(wx.Panel):
    TIMER_ID = 42
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        self.timer = wx.Timer(self,  Board.TIMER_ID)
        self.timer.Start(500)
        self.Bind(wx.EVT_TIMER, self.onTimer, id=Board.TIMER_ID)
        
       # wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        self.contents = []
        self.Bind(wx.EVT_PAINT, self.drawObjects)
    def onTimer(self, event):
        #print "1"
        nope=1
    def addObject(self, toAdd):
        self.contents.append(toAdd)
    def drawObjects(self, event):
        dc = wx.PaintDC(self)
        filtered = filter(lambda x: hasattr(x, "color"), self.contents)
        for o in range(len(filtered)):
            filtered[o].draw(dc)
class Obstacle(Drawable):
    def __init__(self, x, y, width, height, color):
        super(Obstacle, self).__init__(x, y, width, height, color)


app = wx.App()
thingy = Window(None, -1, 'Client')
w,h = thingy.GetSize()
thingy.statusbar.SetStatusText(str(w))
thingy.board.contents.append(Drawable(40,(h/2)-30,30,30,"#CD00FF", ["#BB00EE", 2]))
thingy.board.contents.append(Drawable(w-40-30,(h/2)-30,30,30,"#44FF00", ["#22DD00", 2]))
app.MainLoop()
