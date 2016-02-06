import wx
import time

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
        #print pen.GetJoin()
        dc.SetPen(pen)#.SetJoin(wx.JOIN_MITER))
        dc.SetBrush(wx.Brush(self.color, wx.SOLID))
        dc.DrawRectangle(self.coords[0][0]+self.border[1], self.coords[0][1]+self.border[1], self.dimensions[0], self.dimensions[1])
        """print self.color
        print self.coords
        print self.dimensions
        print ''
        print ''"""
class Window(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1200, 600),  style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
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
        self.timer.Start(10)
        self.Bind(wx.EVT_TIMER, self.onTimer, id=Board.TIMER_ID)
        
       # wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        self.contents = []
        self.Bind(wx.EVT_PAINT, self.drawObjects)
        
        self.Bind(wx.EVT_KEY_DOWN , self.onChar)
        self.player = self.addObject(Moveable(10, 10, 10, 10, 'red'))  
    def onTimer(self, event):
        self.GetEventHandler().ProcessEvent(wx.PaintEvent( ))
        thingy.Refresh
    def addObject(self, toAdd):
        self.contents.append(toAdd)  
        return self.contents[-1]
    def onChar(self, event):
        keycode = event.GetKeyCode()
        self.player.move({ 83: (-5, 0)
                          ,87: (5, 0)
                          ,65: (0, -5)
                          ,68: (0, 5)}[keycode])
        '''if keycode in [83,wx.WXK_DOWN]:
#            self.player.move((5, 0))
            print "Down"
        if keycode in [87,wx.WXK_UP]:
            print "Up"
        if keycode in [65,wx.WXK_LEFT]:
            print "Left"
        if keycode in [68,wx.WXK_RIGHT]:
            print "Right"'''
    def drawObjects(self, event):
        dc = wx.PaintDC(self)
        
        filtered = filter(lambda x: hasattr(x, "color"), self.contents)
        for o in range(len(filtered)):
            filtered[o].draw(dc)

class Moveable(Drawable):
    def __init__(self, x, y, width, height, color, borderColor = None, borderWidth = 2):
        super(Moveable, self).__init__(x, y, width, height, color, [borderColor if borderColor else color, borderWidth])
        self.velocity = [1, 0]
    def move(self, move):
        #self.coords = map(sum, zip(move * 2, self.coords))
        x,y = self.coords[0]
        x2,y2 = self.coords[1]
        self.coords=[[x+move[0],y+move[1]],[x2+move[0],y2+move[1]]]
        print self.color
        #print self.coords[0]
        return 0
class Obstacle(Drawable):
    def __init__(self, x, y, width, height, color):
        super(Obstacle, self).__init__(x, y, width, height, color, [color, 2])


app = wx.App()
thingy = Window(None, -1, 'Client')
w,h = thingy.GetSize()
thingy.statusbar.SetStatusText(str(w))
thingy.board.contents.append(Drawable(40,(h/2)-30,30,30,"#8F70FF", ["#DDDDDD", 2]))
thingy.board.contents.append(Drawable(w-40-30,(h/2)-30,30,30,"#26FC14", ["#FFFFFF", 2]))
app.MainLoop()
