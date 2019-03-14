from __future__ import division
from tkinter import Tk, Canvas, Label
from tkinter import *
from math import sin, cos, radians, degrees
from datetime import datetime
from datetime import time, date
import time
from time import *


from sympy import sin, cos, tan, asin, acos, atan, symbols, solve, sympify, pprint, pretty
from sympy import pi, Eq, Function, exp, simplify, solveset, S
from sympy.abc import x, theta
from sympy.solvers import solve
from sympy import Symbol
x = Symbol('x')
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)

from sympy import init_printing
init_printing()

# import colorama for green red coloring 
from colorama import Fore, Back, Style 


def retPrint(self):
    print("RETPRINT")
    

# store xy pairs for points
class point():
    x = 0
    y = 0

    # basic math to make our life easier
    from math import sin, cos, radians
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return point(x, y)
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return point(x, y)
    def __str__(self):
        return '[x:{0}, y:{1}]'.format(self.x, self.y)

    # create point from center and vector
    # vector has length and angle in rad
    def offsetByVector(self, angle, length):
        from math import sin, cos, radians
        x = int(cos(angle) * length) + self.x
        y = int(sin(angle) * length) + self.y
        return point(x, y)

    
        
# controls clock hands in circle
class hands():
    # release tkinter!
    root = Tk()


    
    # hand id strings
    longHand = ""
    shortHand = ""
    secondHand = ""
    
    # circle clock corners
    corner1 = point(10, 10)
    corner2 = point(210, 210)
    
    # find midpoint to get the center of the clock
    def centerPoint(self):
        from math import sin, cos, radians
        x = (self.corner1.x + self.corner2.x)/2
        y = (self.corner1.y + self.corner2.y)/2
        return point(x, y)

    # updating clock method
    def updateClock(self, canvas, startTime, pEllapsedTime):
        from datetime import datetime
        
        # init setup tkinter text labels
        self.v = StringVar()
        self.secwv = StringVar()
        self.minwv = StringVar()
        self.hrswv = StringVar()
        # time label
        vwid = Label(canvas, textvariable = self.v, fg='black')
        vwid.pack()
        # sec label
        secwid = Label(canvas, textvariable = self.secwv, fg='black')
        secwid.pack()
        # min label
        minwid = Label(canvas, textvariable = self.minwv, fg='black')
        minwid.pack()
        # hour label
        hrswid = Label(canvas, textvariable = self.hrswv, fg='black')
        hrswid.pack()
        # create widgets
        canvas.create_window(110, 250, window=vwid)   
        canvas.create_window(110, 270, window=secwid)
        canvas.create_window(110, 290, window=minwid)
        canvas.create_window(110, 310, window=hrswid)


        
        # init clock hand
        def initHand(hand, color, width):
            if hand == "":
                hand = canvas.create_line(0,0,0,0,\
                                         fill = color, width = width, capstyle = "round")
                canvas.pack()
            return hand
        # update all tk control names to be the same as prev
        shortHand = self.shortHand = initHand(self.shortHand, "grey", 2)
        longHand = self.longHand = initHand(self.longHand, "black", 4)
        secHand = self.secondHand = initHand(self.secondHand, "red", 1)

        utime = datetime.now()

        """
        time 06:45:15
        utime.hour = 6
        utime.minute = 45
        utime.second = 15
        
        hourAngle = ((6 * 30) + (30 * (45/60)))
        = (180 + (30 * 0.75))
        = (210 + 22.5)
        = 232.5 degrees

        minuteAngle = ((45 * 6) + (6 * (45/60)))
        = (270 + (6 * 0.75))
        = (270 + 4.5)
        = 274.5 degrees

        secondAngle = (15 * 6)
        = 90 degrees

        """
        
        # extra additions to angles to account for magic

        from math import sin, cos, radians

        hourAngle = ((utime.hour * 30.0) + (30.0 * (utime.minute/60.0)))
        minuteAngle = ((utime.minute * 6.0) + (6.0 * (utime.minute/60.0)))
        secondAngle = (utime.second * 6)

        def drawHand(Hand, angle, length):
            # offset by 90 deg so 0 at top
            angle -= 90.0

            rads = radians(angle)
            center = self.centerPoint()
            endPoint = center.offsetByVector(rads, length)
            canvas.coords(Hand, center.x, center.y, endPoint.x, endPoint.y)

        drawHand(longHand, hourAngle, 50)
        drawHand(shortHand, minuteAngle, 80)
        drawHand(secHand, secondAngle, 90)



        # time printing stuff
        import time
        from math import sin, cos, radians
        currTime = int(round(time.time() * 1))
        ellapsedTime = int(currTime)-int(startTime)


        # all the tkinter text display
        if True:
            
            ellapsedMin = ellapsedTime/60
            ellapsedHour = ellapsedTime/3600

            # angular velocity
            solsec = (((pi/30)*(int(ellapsedTime))))
            solmin = ((2*pi/3600)*(int(ellapsedTime)))
            solhrs = ((2*pi/43200)*(int(ellapsedTime)))
            # linear velocity v=w*r (r = hand length)
            vsolsec = 90*solsec
            vsolmin = 80*solmin
            vsolhrs = 50*solhrs

            self.secwv.set("Seconds: w=" + str(round(solsec.evalf(),4)) + " rad/s  v=" + str(round(vsolsec.evalf(),4)) + "m/s")
            self.minwv.set("Minutes: w=" + str(round(solmin.evalf(),4)) + " rad/s  v=" + str(round(vsolmin.evalf(),4)) + "m/s")
            self.hrswv.set("Hours: w=" + str(round(solhrs.evalf(),4)) + " rad/s  v=" + str(round(vsolhrs.evalf(),4)) + "m/s")
            
            self.v.set("Ellapsed seconds: " + str(ellapsedTime) + "  Time: " + str(utime.hour) + ":" + str(utime.minute) + ":" + str(utime.second))
        
            
       # wait 100 mili then recall
        rotate = lambda: self.updateClock(canvas, startTime, pEllapsedTime)

            
        pEllapsedTime = ellapsedTime

        canvas.after(100, rotate)
        

  


    def run(self):
        self.root.bind('<q>', exit)
        self.root.bind('<Return>', retPrint)
        self.root.mainloop()

    def __init__(self):
        canvas = Canvas(self.root, width=220, height=330)

        # get corners
        corner1 = self.corner1
        corner2 = self.corner2


       

        canvas.create_oval(corner1.x, corner1.y, corner2.x, corner2.y, \
                           fill = "white", width = 3)
        center = self.centerPoint()

        
        canvas.pack()
        self.root.wm_title("Clock")

        # get start time and save it
        import time
        startTime = int(round(time.time() * 1))

    
        # prepare for main loop
        self.updateClock(canvas,startTime,0)

def main():
    sHand = hands()
    sHand.run()


main()
   
        



