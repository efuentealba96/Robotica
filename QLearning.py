import random as ra
import pygame as pyg
import sys

# Parametros modelo QLearning RL_MDP Discount rewards
ALPHA = 0.1  # Tasa de aprendizaje
GAMMA = 0.98  # Tasa de descuento
nMax_episodidos = 1000

# Acciones
nNORTE = 0
nSUR = 1
nESTE = 2
nWESTE = 3

# Datos mapa de navegacion
nFilasMin = 0
nFilasMax = 11
nColumMin = 0
nColumMax = 7
aMeta = [10, 4]


aMAPA = [[1,  1,  1,  1,  1, -1,  1,  1],  # 0
         [1, -1, -1, -1,  1, -1,  1,  1],  # 1
         [1, -1,  1, -1,  1,  1,  1,  1],  # 2
         [1, -1,  1,  1,  1, -1, -1, -1],  # 3
         [1,  1,  1,  1,  1,  1,  1,  1],  # 4
         [-1, -1, -1,  1, -1, -1, -1,  1],  # 5
         [1,  1,  1,  1,  1,  1, -1,  1],  # 6
         [1, -1, -1,  1, -1,  1, -1,  1],  # 7
         [1,  1, -1,  1, -1,  1,  1,  1],  # 8
         [-1,  1, -1,  1, -1,  1, -1,  1],  # 9
         [-1,  1, -1,  1,  1,  1, -1, -1],  # 10
         [1,  1, -1,  1, -1,  1,  1,  1]]  # 11
# Mapa de 12 x 8 = 96 | Estados = celdas


aSTATE = [[0,  1,  2,  3,  4, -1,  5,  6],  # 0
          [7, -1, -1, -1,  8, -1,  9, 10],  # 1
          [11, -1, 12, -1, 13, 14, 15, 16],  # 2
          [17, -1, 18, 19, 20, -1, -1, -1],  # 3
          [21, 22, 23, 24, 25, 26, 27, 28],  # 4
          [-1, -1, -1, 29, -1, -1, -1, 30],  # 5
          [31, 32, 33, 34, 35, 36, -1, 37],  # 6
          [38, -1, -1, 39, -1, 40, -1, 41],  # 7
          [42, 43, -1, 44, -1, 45, 46, 47],  # 8
          [-1, 48, -1, 49, -1, 50, -1, 51],  # 9
          [-1, 52, -1, 53, 54, 55, -1, -1],  # 10
          [56, 57, -1, 58, -1, 59, 60, 61]]  # 11

# Genere QTable - nS = Estados, nA = Acciones


def InitQTable(nS, nA):
    aQ = [[0.0 for i in range(nA)]for i in range(nS)]
    return aQ

# Estados inicial del robot en el mapa


def InitState():
    aPosRM = [0, 0]
    return aPosRM

# Sampleamos un accion al Azar


def Get_Greedy_Action(nS):
    if ra.random() > Epsilon:
        a = GetMaxAction(nS)
    else:
        a = ra.randint(0, 3)  # 0, 1, 2, 3 = N, S, E, O
    return a

# Sampleamos la mejor accion


def GetMaxAction(nS):
    return Q[nS].index(max(Q[nS]))

# Calculamos los rewards


def Get_RW(aPosRM):
    if aMeta == aPosRM:
        return +5
    else:
        return -0.1


def UpDateQ(s, a, r, sp):
    maxQ = max(Q[sp])
    Q[s][a] = (1-ALPHA) * Q[s][a] + ALPHA * (r + GAMMA * maxQ)

# Retorna otra accion aleatoria a partir
# de la accion que se pasa como parametro
# nA: Accion de origen | fil: posicion en la fila actual | col: posicion en la columna acutal


def OtherAction(nA, fil, col):
    nDadoA = ra.random()
    # Accion Norte
    if nA == nNORTE:
        if col > 0 and col < 7:
            if nDadoA >= 0.0 and nDadoA < 0.5:
                return nESTE
            else:
                return nWESTE
        if col == 0:
            return nESTE
        if col == 7:
            return nWESTE
    # Accion Sur
    if nA == nSUR:
        if col > 0 and col < 7:
            if nDadoA >= 0.0 and nDadoA < 0.5:
                return nESTE
            else:
                return nWESTE
        if col == 0:
            return nESTE
        if col == 7:
            return nWESTE
    # Accion Este
    if nA == nESTE:
        if fil > 0 and fil < 11:
            if nDadoA >= 0.0 and nDadoA < 0.5:
                return nNORTE
            else:
                return nSUR
        if fil == 0:
            return nSUR
        if fil == 11:
            return nNORTE
    # Accion Oeste
    if nA == nWESTE:
        if fil > 0 and fil < 11:
            if nDadoA >= 0.0 and nDadoA < 0.5:
                return nNORTE
            else:
                return nSUR
        if fil == 0:
            return nSUR
        if fil == 11:
            return nNORTE

# Simulamos la navegacion


def Run_Action(a, nExito):
    global aPosRM
    global next_state
    nDado = ra.random()
    i = aPosRM[0]  # Fila Posicion del robot mapa
    j = aPosRM[1]  # Columna Posicion del robot mapa
    if a == nNORTE:  # El robot sube
        if i > nFilasMin:  # Bordes del Mapa
            if aMAPA[i-1][j] != -1:  # Hay una muralla?
                # ------------ Probabilidad ----------------
                if nDado >= 0.0 and nDado <= nExito:  # <-------------- Probabilidad de moverse
                    aPosRM = [i-1, j]
                    next_state = aSTATE[i-1][j]  # Actualizar nuevo Estado
                    return next_state
                else:
                    newAction = OtherAction(a, i, j)
                    next_state = Run_Action(newAction, 1)
                    return next_state
                # ------------------------------------------
            else:  # Si hay una muralla...
                aPosRM = [i, j]
                next_state = aSTATE[i][j]
                return next_state
        else:  # Si esta al borde del mapa...
            aPosRM = [i, j]
            # print(aPosRM)
            next_state = aSTATE[i][j]  # Actualizar nuevo Estado
            return next_state
    #########################################################################
    if a == nSUR:  # El robot baja
        if i < 11:  # Bordes del Mapa
            if aMAPA[i+1][j] != -1:  # Hay una muralla?
                # ------------ Probabilidad ----------------
                if nDado >= 0.0 and nDado <= nExito:  # <-------------- Probabilidad de moverse
                    aPosRM = [i+1, j]
                    next_state = aSTATE[i+1][j]  # Actualizar nuevo Estado
                    return next_state
                else:
                    newAction = OtherAction(a, i, j)
                    next_state = Run_Action(newAction, 1)
                    return next_state
                # ------------------------------------------
            else:  # Si hay una muralla...
                aPosRM = [i, j]
                next_state = aSTATE[i][j]
                return next_state
        else:  # Si esta al borde del mapa...
            aPosRM = [i, j]
            next_state = aSTATE[i][j]
            return next_state

    if a == nESTE:  # El robot va a la derecha
        if j < 7:  # Bordes del Mapa
            if aMAPA[i][j+1] != -1:  # Hay una muralla?
                # ------------ Probabilidad ----------------
                if nDado >= 0.0 and nDado <= nExito:  # <-------------- Probabilidad de moverse
                    aPosRM = [i, j+1]
                    next_state = aSTATE[i][j+1]  # Actualizar nuevo Estado
                    return next_state
                else:
                    newAction = OtherAction(a, i, j)
                    next_state = Run_Action(newAction, 1)
                    return next_state
                # ------------------------------------------
            else:  # Si hay una muralla...
                aPosRM = [i, j]
                next_state = aSTATE[i][j]
                return next_state
        else:  # Si esta al borde del mapa...
            aPosRM = [i, j]
            next_state = aSTATE[i][j]
            return next_state

    if a == nWESTE:  # El robot va a la izquierda
        if j > 0:  # Bordes del Mapa
            if aMAPA[i][j-1] != -1:  # Hay una muralla?
                # ------------ Probabilidad ----------------
                if nDado >= 0.0 and nDado <= nExito:  # <-------------- Probabilidad de moverse
                    aPosRM = [i, j-1]
                    next_state = aSTATE[i][j-1]  # Actualizar nuevo Estado
                    return next_state
                else:
                    newAction = OtherAction(a, i, j)
                    next_state = Run_Action(newAction, 1)
                    return next_state
                # ------------------------------------------
            else:  # Si hay una muralla...
                aPosRM = [i, j]
                next_state = aSTATE[i][j]
                return next_state
        else:  # Si esta al borde del mapa...
            aPosRM = [i, j]
            next_state = aSTATE[i][j]
            return next_state
    return next_state

# QLearning


def QLearning(MaxSteps=100):
    s = aSTATE[0][0]  # Posicion inicial
    steps = 0
    tl_rw = 0
    for i in range(0, MaxSteps):
        a = Get_Greedy_Action(s)  # Samplea Accion, [0,1,2,3] = [n,s,e,o]
        sp = Run_Action(a, 0.80)
        rw = Get_RW(aPosRM)
        tl_rw += rw
        steps += 1
        UpDateQ(s, a, rw, sp)
        s = sp
        if aPosRM == aMeta:
            break
    return tl_rw, steps


Epsilon = 0.1
Q = InitQTable(62, 4)
aList_A = ['N', 'S', 'E', 'O']
for i in range(nMax_episodidos):
    aPosRM = [0, 7]
    total_rw, steps = QLearning(nMax_episodidos)
    print('Episodio: ' + str(i) + ' Steps: ' +
          str(steps) + ' Reward: ' + str(total_rw))
    Epsilon *= 0.9


aOPTIMO = aSTATE
# Crea un mapa con los movimientos optimos
for i in range(146):
    for s in range(len(aOPTIMO)):  # f , c = Q.index(i)
        for z in range(len(aOPTIMO[s])):
            if aOPTIMO[s][z] == i:
                aOPTIMO[s][z] = aList_A[Q[i].index(max(Q[i]))]
                continue
            if aOPTIMO[s][z] == -1:
                aOPTIMO[s][z] = '▉'
                continue

for i in aOPTIMO:
    print(i)

print(aOPTIMO)
# Seccion de trabajo con pygame
pyg.init()
size = width, height = 400, 600
screen = pyg.display.set_mode(size)
pyg.display.set_caption("Proyecto final")
icon = pyg.image.load("images/terminator.png")
pyg.display.set_icon(icon)

sizeImage = (50, 50)

muro = pyg.transform.scale(pyg.image.load("images/muro.png"), sizeImage)
nave = pyg.transform.scale(pyg.image.load("images/nave.png"), (40, 40))
star = pyg.transform.scale(pyg.image.load("images/star.png"), sizeImage)
fondo = pyg.transform.scale(pyg.image.load("images/fondo.jpg"), sizeImage)

x = 0
y = 0
screen.blit(nave, (0, 0))
for i in range(12):
    for j in range(8):
        if aMAPA[i][j] == -1:
            screen.blit(muro, (x, y))
            x += 50
        else:
            screen.blit(fondo, (x, y))
            x += 50
    screen.blit(star, (200, 50*10))
    x = 0
    y += 50
screen.blit(nave, (aPosRM[0], aPosRM[1]))
objetive = True
while True:

    # Falta implementear pygame
    # pyg.time.delay(500)
    # if(objetive == True):
    #     if()

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            sys.exit()

    pyg.display.update()
