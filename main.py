import Tkinter

players = []

mainWin = Tkinter.Tk()
mainWin.wm_title("Game Name")
mainWin.resizable(width=False, height=False)
canvas = Tkinter.Canvas(mainWin, width=1200, height=600, background="white")

class player:
    def __init__(this, x, y, width, height, name, color):
        this.name = name
        this.x, this.y = x, y
        this.width, this.height = width, height
        this.color = color
        this.onGround = False
        this.velX, this.velY = 0,0
        y2 = this.y + this.height
        x2 = this.x + this.width
        this.item = canvas.create_rectangle(this.x,this.y,x2,y2, fill=this.color)
    def update(self):
        
        self.x += self.velX
        self.y += self.velY
        self.velY += 0.1
        
        col = testCollide(self,arr=objects)
        
        self.x += col['x']
        self.y += col['y']
        
        
        if col['y'] < 0:
            self.velY = 0
        y2 = self.y + self.height
        x2 = self.x + self.width
        
        self.x = int(self.x*1000)/1000
        self.y = int(self.y*1000)/1000
        
        canvas.coords(self.item,self.x, self.y,x2,y2)
class object:
    def __init__(this, x, y, width, height, color):
        this.x, this.y = x, y
        this.width, this.height = width, height
        this.color = color
        this.velX, this.velY = 0,0
        y2 = this.y + this.height
        x2 = this.x + this.width
        this.item = canvas.create_rectangle(this.x,this.y,x2,y2, fill=this.color)
        
p1 = player(0,0,20,20,'sadfas','red')
objects = []
objects.append(object(0,int(canvas['height'])-20,int(canvas['width']),20,'#000000'))

def testCollide(obj,arr=None,obj2=None):
    xchange = 0
    ychange = 0
    L = obj.x
    T = obj.y
    R = obj.x + obj.width
    B = obj.y + obj.height
    
    if isinstance(arr,list):
        for i in range(0,len(arr)):
            L2 = arr[i].x
            T2 = arr[i].y
            R2 = arr[i].x + arr[i].width
            B2 = arr[i].y + arr[i].height
            
            betweenX = (L < R2 and R > L2);
            betweenY = (B > T2 and T < B2);
            
            B_T2 = (B > T2 and T < T2)#Bottom Top
            T_B2 = (T < B2 and B > B2)#Top Bottom
        
            R_L2 = (R > L2 and L < L2)#Right Left
            L_R2 = (L < R2 and R > R2)#Left Right
            
            if (betweenX and B_T2 and not(R_L2 or L_R2)):#Bottom Top Detection
                ychange += B - T2
            elif (betweenX and T_B2 and not(R_L2 or L_R2)):#Top Bottom Detection
                ychange -= B2 - T;
        
            elif (betweenY and R_L2 and not(B_T2 or T_B2)):
                xchange += R - L2
            elif (betweenY and L_R2 and not(B_T2 or T_B2)):
                xchange += L - R2
            if ((T-obj.velY < T2 and B-obj.velY > T2)):
                ychange = T2 - B
    elif obj2 != None:
        L2 = obj2.x
        T2 = obj2.y
        R2 = obj2.x + obj2.width
        B2 = obj2.y + obj2.height
        betweenX = (L < R2 and R > L2);
        betweenY = (B > T2 and T < B2);
        
        B_T2 = (B > T2 and T < T2)#Bottom Top
        T_B2 = (T < B2 and B > B2)#Top Bottom
    
        R_L2 = (R > L2 and L < L2)#Right Left
        L_R2 = (L < R2 and R > R2)#Left Right
        
        if (betweenX and B_T2 and not(R_L2 or L_R2)):#Bottom Top Detection
            ychange += B - T2
        if (betweenX and T_B2 and not(R_L2 or L_R2)):#Top Bottom Detection
            ychange -= B2 - T;
    
        if (betweenY and R_L2 and not(B_T2 or T_B2)):
            xchange += R - L2
        if (betweenY and L_R2 and not(B_T2 or T_B2)):
            xchange += L - R2
    return {'x':xchange,'y':ychange}
def updateWin():
    p1.update()    
    canvas.pack()
    canvas.after(1,updateWin)
def main(ip='127.0.0.1',port=5200,name="Anon"):
    #players.append(); 
    updateWin()
    mainWin.mainloop()
main()