from random import choice, random, randrange, randint
from turtle import *

from freegames import vector


# Variables globales
ball = vector(0, 0)
aim = vector(5, 5)
state = {1: (0, 0, 50, 0), 2: (0, 0, 50, 0)}
powerup = vector(0, 0)
powerup_state = {'active': False, 'type': None}

player_left_movement_rate = 1
player_right_movement_rate = 1

# Crear powerup
def create_powerup():
    #Crear un powerup de manera aleatoria
    if not powerup_state['active']:
        # definir coordenadas aleatorias
        powerup.x = randrange(-200, 200)
        powerup.y = randrange(-200, 200)
        powerup_state['active'] = True
        # Definir de manera aleatoria que tipo de powerup es
        if randint(0, 1) == 1:
            powerup_state['type'] = 'enlarge_paddle'
        else:
            powerup_state['type'] = 'speedup_paddle'
            
        ontimer(create_powerup, 10000)  # Create a new powerup every 10 seconds
    else:
        ontimer(create_powerup, 1000)  # Check again in 1 second


    

def check_powerup(player):
    #Verificar colisión con el powerup y asignar.
    if powerup_state['active']:
        # Revisar que jugador estamos evaluando
        if player == 1:
            y, x, _, _ = state[player]
            # Revisar colisiones de jugador 1
            if powerup.x < -185 - state[1][1] and powerup.x > -205 - state[1][1]:
                low = state[1][0]
                high = state[1][0] + state[1][2]
                if low <= powerup.y <= high:
                    if powerup_state['type'] == 'enlarge_paddle':
                        aumentar_height(player)
                    else:
                        speedup_paddle(1)
                    powerup_state['active'] = False               
        else:
            y, x, _, _ = state[player]
            # Revisar colisiones de jugador 2
            if powerup.x > 185 - state[2][1] and powerup.x < 205 - state[2][1]:
                low = state[2][0]
                high = state[2][0] + state[2][2]
                if low <= powerup.y <= high:
                    if powerup_state['type'] == 'enlarge_paddle':
                        aumentar_height(player)
                    else:
                        speedup_paddle(2)
                    powerup_state['active'] = False
                

def speedup_paddle(player):
    print("SPEEDUP TRIGGERED")
    if player == 1:
        global player_left_movement_rate
        player_left_movement_rate = 2
        def restore_l():
            global player_left_movement_rate 
            player_left_movement_rate = 1 
        ontimer(restore_l, 5000)
    else:
        global player_right_movement_rate
        player_right_movement_rate = 2
        def restore_r():
            global player_right_movement_rate
            player_right_movement_rate = 1
        ontimer(restore_r, 5000)

# Cabmiar la posición del jugador segun el input
# player es el indice del jugador, change es la cantidad a moverse, direction es en que eje
def move(player, change, direction):
    #Moverse
    # Si la direccion es 1, mover vertical; si no, mover horizontal
    if direction == 1:
        state[player] = (state[player][0], state[player][1] + change, state[player][2], state[player][3])
    else:
        state[player] = (state[player][0] + change, state[player][1], state[player][2], state[player][3])

# Cambiar altura de jugador
def aumentar_height(player):
    # Aumenta el tamaño de la paleta durante 5 segundos
    state[player] = (state[player][0], state[player][1], 100, 1)
    def disminuir_height():
        state[player] = (state[player][0], state[player][1], 50, 0)
    ontimer(disminuir_height, 5000)





# Metodo para dibujar rectangulos para las paletas, segun coordenada en 'x', 'y', ancho, alto y color
def rectangle(x, y, width, height, fillcolor):
    #Dibujar rectángulo en pantalla con las dimensiones dadas
    # Moverse a posición de paleta sin trazar
    up()
    goto(x, y)
    down()
    color(fillcolor)
    begin_fill()
    # hacer trazos y fill
    for _ in range(2):
        forward(width)
        left(90)
        forward(height)
        left(90)
    end_fill()

def draw():
    #Dibujar los elementos en pantalla y actualizar frames. Tambien hacer llamadas a funciones de verificación de colisiones
    # Borrar pantalla
    clear()

    # Dibujar paletas de los jugadores de diferentes colores según su offset
    rectangle(-200 - state[1][1], state[1][0], 10, state[1][2], 'orange')
    rectangle(190 - state[2][1], state[2][0], 10, state[2][2], 'blue')

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
    if x < -185 - state[1][1] and x > -205 - state[1][1]:
        low = state[1][0]
        high = state[1][0] + state[1][2]
        if low <= y <= high:
            aim.x = -aim.x

    # Si la pelota se encuentra en pared izquierda, parar.
    if x < -190:
        return

    # Si la pelota se encuentra dentro del area de la paleta 1, rebotar vertical
    if x > 185 - state[2][1] and x < 205 - state[2][1]:
        low = state[2][0]
        high = state[2][0] + state[2][2]
        if low <= y <= high:
            aim.x = -aim.x

    # Si la pelota se encuentra en pared derecha, parar.
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

# Setup de turtle
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()

#Movimiento de los jugadores
def move_player_factory(player: int, sign: int, axis: int):
    def _foo():
        global player_left_movement_rate, player_right_movement_rate
        rate = 0 
        if player == 1:
            rate = player_left_movement_rate
        else: 
            rate = player_right_movement_rate
        move(player, 20 * sign * rate, axis)
    return _foo

# Setup para inputs de jugador 1
onkey(move_player_factory(1, 1, 0), 'w')
onkey(move_player_factory(1, 1, 1), 'a')
onkey(move_player_factory(1, -1, 0), 's')
onkey(move_player_factory(1, -1, 1), 'd')

# Setup para inputs de jugador 2
onkey(move_player_factory(2, 1, 0), 'i')
onkey(move_player_factory(2, 1, 1), 'j')
onkey(move_player_factory(2, -1, 0), 'k')
onkey(move_player_factory(2, -1, 1), 'l')

# Llamada a inicio de juego
draw()
done()
