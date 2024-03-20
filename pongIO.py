"""Pong, classic arcade game.

Exercises

1. Change the colors.
2. What is the frame rate? Make it faster or slower.
3. Change the speed of the ball.
4. Change the size of the paddles.
5. Change how the ball bounces off walls.
6. How would you add a computer player?
6. Add a second ball.
"""

from random import choice, random
from turtle import *

from freegames import vector


def value():
    """Randomly generate value between (-5, -3) or (3, 5)."""
    return (3 + random() * 2) * choice([1, -1])

ball = vector(0, 0)
aim = vector(5, 5)
state = {1: (0,0), 2: (0,0)}


def move(player, change, direction):
    """Move player position by change."""
    if (direction == 1):
        state[player] = (state[player][0],state[player][1]+change)
    else:
        state[player] = (state[player][0]+change,state[player][1])



def rectangle(x, y, width, height, fillcolor):
    """Draw rectangle at (x, y) with given width and height."""
    up()
    goto(x, y)
    down()
    color(fillcolor)
    begin_fill()
    
    for count in range(2):
        forward(width)
        left(90)
        forward(height)
        left(90)
    end_fill()


def draw():
    """Draw game and move pong ball."""
    clear()
    rectangle(-200-state[1][1], state[1][0], 10, 50, 'orange')
    rectangle(190-state[2][1], state[2][0], 10, 50, 'blue')

    ball.move(aim)
    x = ball.x
    y = ball.y

    up()
    goto(x, y)
    color('black')

        
    dot(10)
    update()

    if y < -200 or y > 200:
        aim.y = -aim.y

    if x < -185-state[1][1] and x > -200-state[1][1]:
        low = state[1][0]
        high = state[1][0] + 50

        if low <= y <= high:
            aim.x = -aim.x
    
    
    if x < -190:
        return
       

    if x > 185-state[2][1] and x < 200-state[2][1]:
        low = state[2][0]
        high = state[2][0] + 50

        if low <= y <= high:
            aim.x = -aim.x
            

    if x > 190:
        return

    ontimer(draw, 50)


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: move(1, 20, 0), 'w')
onkey(lambda: move(1, 20, 1), 'a')
onkey(lambda: move(1, -20, 0), 's')
onkey(lambda: move(1, -20, 1), 'd')
onkey(lambda: move(2, 20, 0), 'i')
onkey(lambda: move(2, 20, 1), 'j')
onkey(lambda: move(2, -20, 0), 'k')
onkey(lambda: move(2, -20, 1), 'l')

draw()
done()