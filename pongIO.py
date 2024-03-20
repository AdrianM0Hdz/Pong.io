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

# Importar librerias
from random import choice, random
from turtle import *

from freegames import vector

# Retornar un valor aleatorio entre (-5 y -3) o (3 y 5)
def value():
    """Randomly generate value between (-5, -3) or (3, 5)."""
    return (3 + random() * 2) * choice([1, -1])

# Variables globales
ball = vector(0, 0)
aim = vector(5, 5)
state = {1: (0,0), 2: (0,0)}

# Cabmiar la posición del jugador segun el input
# player es el indice del jugador, change es la cantidad a moverse, direction es en que eje
def move(player, change, direction):
    """Move player position by change."""
    # Si la direccion es 1, mover vertical; si no, mover horizontal
    if (direction == 1):
        state[player] = (state[player][0],state[player][1]+change)
    else:
        state[player] = (state[player][0]+change,state[player][1])


# Metodo para dibujar rectangulos para las paletas, segun coordenada en 'x', 'y', ancho, alto y color
def rectangle(x, y, width, height, fillcolor):
    """Draw rectangle at (x, y) with given width and height."""
    # Moverse a posición de paleta sin trazar
    up()
    goto(x, y)
    down()
    color(fillcolor)
    begin_fill()
    
    # Dibujar y llenar por ancho y largo de paleta
    for count in range(2):
        forward(width)
        left(90)
        forward(height)
        left(90)
    end_fill()


# Escribir texto en pantalla
def write_txt(txt: str): 
    """ escribe texto en la pantalla """
    goto(-170, -50)
    color('black')
    write(txt, font=('Arial', 20, 'normal'))

def draw():
    """Draw game and move pong ball."""
    # Borrar pantalla
    clear()

    # Dibujar paletas de los jugadores de diferentes colores según su offset
    rectangle(-200-state[1][1], state[1][0], 10, 50, 'orange')
    rectangle(190-state[2][1], state[2][0], 10, 50, 'blue')

    # Mover la pelota según vector deseado
    ball.move(aim)
    x = ball.x
    y = ball.y

    # Dibujar pelota
    up()
    goto(x, y)
    color('black')
    dot(10)
    update()

    # Si la pelota toca el punto mas alto o bajo, rebotar vertical
    if y < -200 or y > 200:
        aim.y = -aim.y

    # Si la pelota se encuentra dentro del area de la paleta 1, rebotar horizontal
    if x < -185-state[1][1] and x > -200-state[1][1]:
        low = state[1][0]
        high = state[1][0] + 50

        if low <= y <= high:
            aim.x = -aim.x
    
    # Si la pelota se encuentra en pared izquierda, parar juego y anunciar ganador.
    if x < -190:
        write_txt("Jugador de la derecha \n gana") 
        return
       
    # Si la pelota se encuentra dentro del area de la paleta 1, rebotar vertical
    if x > 185-state[2][1] and x < 200-state[2][1]:
        low = state[2][0]
        high = state[2][0] + 50

        if low <= y <= high:
            aim.x = -aim.x
            
    # Si la pelota se encuentra en pared derecha, parar juego y anunciar ganador.
    if x > 190:
        write_txt("Jugador de la izquierda \n gana") 
        return 
    
    # Llamar draw despues de 50ms
    ontimer(draw, 50)

# Setup de turtle
setup(420, 420, 370, 0)
hideturtle()
tracer(False)

# Setup para inputs de jugador
listen()
onkey(lambda: move(1, 20, 0), 'w')
onkey(lambda: move(1, 20, 1), 'a')
onkey(lambda: move(1, -20, 0), 's')
onkey(lambda: move(1, -20, 1), 'd')
onkey(lambda: move(2, 20, 0), 'i')
onkey(lambda: move(2, 20, 1), 'j')
onkey(lambda: move(2, -20, 0), 'k')
onkey(lambda: move(2, -20, 1), 'l')

# Llamada a inicio de juego
draw()
done()