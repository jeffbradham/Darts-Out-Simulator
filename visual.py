
# Darts Scoring Algorithm - www.101computing.net/darts-scorign-algorithm

import turtle
import random
import math
import time


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
    myPen.penup()
    myPen.goto(-300, -300)
    myPen.getscreen().update()


def calculateScore(arrowx, arrowy):
    score = 0
    distance = 0
    # Add code here using Pythagoras formula to calculate the distance to the centre.
    # distance = ....

    # Use SOCATOA to calculate the angle matching the arrow position
    angle = math.degrees(math.atan2(arrowy, arrowx))
    if angle < 0:
        angle += 360
    print(angle)

    # Use a collection of IF statements to calculate the score of the arrow based on the distance and angle
    # ...

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
myPen.pencolor('black')

drawTarget()
# Shooting the arrow
arrowx = random.randint(-150, 150)
arrowy = random.randint(-150, 150)
drawCross("#00FFFF", 10, arrowx, arrowy)

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