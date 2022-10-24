
# Darts Scoring Algorithm - www.101computing.net/darts-scorign-algorithm

import turtle
import random
import math
from enum import Enum

class Ring(Enum):
    MISS = 0
    SINGLE = 1
    DOUBLE = 2
    TRIPPLE = 3
    SINGLE_BULL = 25 
    DOUBLE_BULL = 50 


def drawLayer(radius, color1, color2):
    angle = 18
    initialAngle = angle
    myPen.penup()
    myPen.setheading(180)
    myPen.goto(0, radius)
    myPen.circle(radius, angle//2)  # move along arc
    myPen.pendown()
    i = 0

    while i <= 20:
        myPen.begin_fill()
        myPen.circle(radius, angle)  # move along arc
        myPen.left(90)
        myPen.forward(radius)  # turtle now at centre
        myPen.left(180-initialAngle)
        myPen.forward(radius)  # back on edge of circle
        myPen.left(90)
        myPen.speed(0)
        angle = initialAngle*2  # moves turtle to begin next pie shape
        i = i + 1
        if i % 2 == 0:
            # this conditional creates the alernating pattern
            myPen.fillcolor(color1)
        else:
            myPen.fillcolor(color2)
        myPen.end_fill()


def drawTarget():
    drawLayer(288, "#FF0000", "#099909")
    drawLayer(268, "#111111", "#FFFFAA")
    drawLayer(168, "#FF0000", "#099909")
    drawLayer(148, "#111111", "#FFFFAA")

    # Outer Bull
    myPen.fillcolor("#099909")
    myPen.penup()
    myPen.setheading(180)
    myPen.goto(0, 40)
    myPen.begin_fill()
    myPen.pendown()
    myPen.circle(40)
    myPen.end_fill()

    # Bull's Eye
    myPen.fillcolor("#FF0000")
    myPen.penup()
    myPen.setheading(180)
    myPen.goto(0, 20)
    myPen.begin_fill()
    myPen.pendown()
    myPen.circle(20)
    myPen.end_fill()


def drawCross(color, size, x, y):
    myPen.pensize(3)
    myPen.color(color)
    myPen.penup()
    myPen.goto(x-size, y-size)
    myPen.pendown()
    myPen.goto(x+size, y+size)
    myPen.penup()
    myPen.goto(x-size, y+size)
    myPen.pendown()
    myPen.goto(x+size, y-size)


def writeScore(text):
    myPen.penup()
    myPen.goto(-80, 170)
    myPen.color("#000000")
    myPen.write(text, False, "Left", "16")

def dart(x,y):
    drawCross("#00FFFF", 10, x, y)
    # print("HIT: "+ str(x) +" / "+ str(y))
    calculateScore(x,y)
    myPen.penup()
    myPen.goto(-300, -300)
    myPen.getscreen().update()

def getRing(x, y):
    dist = math.sqrt(x*x + y*y)
    # print(f"Distance: {dist}")
    r = Ring.MISS
    if(dist < 20):
        r = Ring.DOUBLE_BULL
    if(dist >= 20 and dist < 40):
        r = Ring.SINGLE_BULL
    if(dist >= 40 and dist < 148):
        r = Ring.SINGLE
    if(dist >= 148 and dist < 168):
        r = Ring.TRIPPLE 
    if(dist >= 168 and dist < 268):
        r = Ring.SINGLE
    if(dist >= 268 and dist < 288):
        r = Ring.DOUBLE
    # print(f"Ring: {r} -- {r.value}")
    return(r)

def getPts(ring, angle):
    if(ring == Ring.DOUBLE_BULL or ring == Ring.SINGLE_BULL):
        score = ring.value
    else:
        pts = 0
        if(angle >=  351 or (angle >= 0 and angle < 9)):
            pts = 6
        if(angle >=  9 and angle < 27):
            pts = 13
        if(angle >=  27 and angle < 45):
            pts = 4
        if(angle >=  45 and angle < 63):
            pts = 18
        if(angle >=  63 and angle < 81):
            pts = 1
        if(angle >=  81 and angle < 99):
            pts = 20
        if(angle >=  99 and angle < 117):
            pts = 5
        if(angle >=  117 and angle < 135):
            pts = 12
        if(angle >=  135 and angle < 153):
            pts = 9
        if(angle >=  153 and angle < 171):
            pts = 14
        if(angle >=  171 and angle < 189):
            pts = 11
        if(angle >=  189 and angle < 207):
            pts = 8
        if(angle >=  207 and angle < 225):
            pts = 16
        if(angle >=  225 and angle < 243):
            pts = 7
        if(angle >=  243 and angle < 261):
            pts = 19
        if(angle >=  261 and angle < 279):
            pts = 3
        if(angle >=  279 and angle < 297):
            pts = 17
        if(angle >=  297 and angle < 315):
            pts = 2
        if(angle >=  315 and angle < 333):
            pts = 15
        if(angle >=  333 and angle < 351):
            pts = 10
        score = pts * ring.value

    print(f"Score: {score}")
    writeScore("Your Score: + " + str(score))
    return(score)

def getAngle(x, y):
    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle += 360
    # print(f"Angle: {angle}")
    return(angle)


def calculateScore(arrowx, arrowy):
    score = 0
    distance = 0
    ring = getRing(arrowx, arrowy)
    angle= getAngle(arrowx, arrowy)
    getPts(ring, angle)

    return score


##########################################
#        MAIN PROGRAM STARTS HERE        #
##########################################
myPen = turtle.Turtle()
myPen._tracer(0)
myPen.speed(0)
myPen.color("#FF0000")

myPen.shape('arrow')
myPen.pensize(1)
myPen.pencolor('red')

drawTarget()
# Shooting the arrow
arrowx = random.randint(-150, 150)
arrowy = random.randint(-150, 150)
drawCross("#FFFFFF", 10, arrowx, arrowy)

# Calculate and display score
# score = calculateScore(arrowx, arrowy)
# writeScore("Your Score: + " + str(score))



# Hide the pen
myPen.penup()
myPen.goto(-300, -300)
sc = myPen.getscreen()
sc.update()
sc.onclick(dart)
sc.mainloop()