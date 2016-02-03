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
    def __init__(self, x, y, width, height, color):
        super(Drawable, self).__init__(x, y, width, height)
        self.color = color
    def draw(self, dc):
        dc.SetPen(wx.Pen(self.color, 4))
        dc.DrawRectangle(self.coords[0][0], self.coords[0][1], self.dimensions[0], self.dimensions[1])
        
class Window(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(600, 600))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('0')
        self.board = Board(self)
        self.Centre()
        self.Show(True)

class Board(wx.Panel):
    def __init__(self, parent):
        self.timer = wx.Timer(self, self.onTimer)
        self.timer.Start(500)
        self.Bind(wx.EVT_TIMER, self.timer, self.onTimer)
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        self.contents = []
        self.Bind(wx.EVT_PAINT, self.drawObjects)
    def onTimer(self, event):
        print "1"
    def addObject(self, toAdd):
        self.contents.append(toAdd)
    def drawObjects(self, event):
        dc = wx.PaintDC(self)
        for o in filter(lambda x: hasattr(x, "color"), self.contents):
            o.draw(dc)

class Obstacle(Drawable):
    def __init__(self, x, y, width, height, color):
        super(Obstacle, self).__init__(x, y, width, height, color)

app = wx.App()
Window(None, -1, 'Client')
app.MainLoop()
