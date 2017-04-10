#!/usr/bin/python3

import turtle
import math

def square(t, length):
    for i in range(4):
        t.fd(100)
        t.lt(90)
        
def polyline(t, n, length, angle):
    """Draws n line segments with the given length and angle(in degrees)
    between them. t is a turtle
    """
    for i in range(n):
        t.fd(length)
        t.lt(angle)

def polygon(t, n=7, length=100):
    angle = 360 / n
    polyline(t, n, length, angle)

def arc(t, r, angle):
    arc_len = 2 * math.pi * r * angle / 360
    n = int(arc_len / 3) + 1
    step_len = arc_len / n
    step_angle = angle / n

    polyline(t, n, step_len, step_angle)
    
def circle(t, r):
    arc(t, r, 360)

def flowers(t, n):
    for i in range(n):
        arc(t, 50, 80)
        t.lt(100)
        arc(t, 50, 80)
        t.lt(60)

def shapes(t, n, length):
    outter_angle = 360 / n
    inner_angle = (180 - outter_angle) / 2
    inner_len = (length / 2) / math.cos(inner_angle / 180 * math.pi)

    for i in range(n):
        t.fd(length)
        t.lt(outter_angle + inner_angle)
        t.fd(inner_len)
        t.lt(180)
        t.fd(inner_len)
        t.lt(outter_angle + inner_angle)

def draw_B(t, r=30):
    arc(t, r, 180)
    t.lt(180)
    arc(t, r, 180)
    t.lt(90)
    t.fd(4*r)

def main():
    bob = turtle.Turtle()
    bob.color("red")
    
    '''
    square(bob, 100)
    bob.setx(200)
    bob.sety(-300)
    polygon(bob, 7, 50)

    bob.setx(0)
    bob.sety(200)
    '''

    #flowers(bob, 9)
    #shapes(bob, 8, 100)
    draw_B(bob)
    turtle.mainloop()

if __name__ == '__main__':
    main()
