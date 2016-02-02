import wx
import random
nop = 1

class Drawable(object):
    def __init__(self, color, outline):
        self.color, self.outline = color, outline
        
class GameObject(object):
    def __init__(self, x, y, width, height):
        self.coords, self.velocity = [[x, y], [x + width, y + height]], [0, 0]
    def isTouching(self, compareTo):
        inside = [0, 0]
        for c in [0, 1]:
            for i in range(len(self.coords)):
                if  compareTo.coords[0][c] < self.coords[i][c] < compareTo.coords[1][c]:
                    inside[c] = self.coords[i][c] - compareTo.coords[i][c]
        return inside
        
class Thing(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(600, 600))
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('0')
        self.board = Board(self)
        self.Centre()
        self.Show(True)

class Board(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)

class Obstacle(GameObject, Drawable):
    def __init__(self, x, y, width, height, color, outline = None):
        super(self, GameObject).__init__(x, y, width, height)
        super(self, Drawable).__init__(color, outline if outline else color)
        self.color = color

app = wx.App()
Thing(None, -1, 'Client')
app.MainLoop()
