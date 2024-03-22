from random import choice, random, randrange
from turtle import *

from freegames import vector



ball = vector(0, 0)
aim = vector(5, 5)
state = {1: (0, 0, 50, 0), 2: (0, 0, 50, 0)}
powerup = vector(0, 0)
powerup_state = {'active': False, 'type': None}

def create_powerup():
    #Crear un powerup de manera aleatoria
    if not powerup_state['active']:
        powerup.x = randrange(-200, 200)
        powerup.y = randrange(-200, 200)
        powerup_state['active'] = True
        powerup_state['type'] = 'enlarge_paddle'
        
        ontimer(create_powerup, 10000)  # Create a new powerup every 10 seconds
    else:
        ontimer(create_powerup, 1000)  # Check again in 1 second


    

def check_powerup(player):
    #Verificar colisión con el powerup y asignar.
    if powerup_state['active']:
        if player == 1:
            y, x, _, _ = state[player]
            print('powerup')
            print(powerup.x, powerup.y)
            print('player', player)
            print(x, y)
            if abs((-200 - x - 15) - powerup.x) < 35 and abs((y-15) - powerup.y) < 35:
                if powerup_state['type'] == 'enlarge_paddle':
                    aumentar_height(player)
                powerup_state['active'] = False
        else:
            y, x, _, _ = state[player]
            if abs((190 - x) - powerup.x) < 35 and abs((y-15) - powerup.y) < 35:
                if powerup_state['type'] == 'enlarge_paddle':
                    aumentar_height(player)
                powerup_state['active'] = False

            


def move(player, change, direction):
    #Moverse
    if direction == 1:
        state[player] = (state[player][0], state[player][1] + change, state[player][2], state[player][3])
    else:
        state[player] = (state[player][0] + change, state[player][1], state[player][2], state[player][3])

def aumentar_height(player):
    # Aumenta el tamaño de la paleta durante 5 segundos
    state[player] = (state[player][0], state[player][1], 100, 1)
    def disminuir_height():
        state[player] = (state[player][0], state[player][1], 50, 0)
    ontimer(disminuir_height, 5000)






def rectangle(x, y, width, height, fillcolor):
    """Draw rectangle at (x, y) with given width and height."""
    up()
    goto(x, y)
    down()
    color(fillcolor)
    begin_fill()
    for _ in range(2):
        forward(width)
        left(90)
        forward(height)
        left(90)
    end_fill()

def draw():
    """Draw game and move pong ball."""
    clear()
    rectangle(-200 - state[1][1], state[1][0], 10, state[1][2], 'orange')
    rectangle(190 - state[2][1], state[2][0], 10, state[2][2], 'blue')
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
    if x < -185 - state[1][1] and x > -205 - state[1][1]:
        low = state[1][0]
        high = state[1][0] + state[1][2]
        if low <= y <= high:
            aim.x = -aim.x
    if x < -190:
        return
    if x > 185 - state[2][1] and x < 205 - state[2][1]:
        low = state[2][0]
        high = state[2][0] + state[2][2]
        if low <= y <= high:
            aim.x = -aim.x
    if x > 190:
        return
    create_powerup()
    if powerup_state['active']:
        up()
        goto(powerup.x, powerup.y)
        color('green')
        dot(20)
    check_powerup(1)
    check_powerup(2)
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
