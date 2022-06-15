#import pygame as pg
import random as ra

# Parametros modelo QLearning RL_MDP Discount rewards
ALPHA = 0.1  # Tasa de aprendizaje
GAMMA = 0.98  # Tasa de descuento
nMax_episodidos = 100

# Acciones
nNorte = 0
nSur = 1
nEste = 2
nOeste = 3

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
    aQ = [[0.0 for i in range(nA) for i in range(nS)]]
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
    if nA == nNorte:
        if col > 0 and col < 7:
            if nDadoA >= 0.0 and nDadoA < 0.5:
                return nEste
            else:
                return nOeste
        if col == 0:
            return nEste
        if col == 7:
            return nOeste
    # Accion Sur
    if nA == nSur:
        if col > 0 and col < 7:
            if nDadoA >= 0.0 and nDadoA < 0.5:
                return nEste
            else:
                return nOeste
        if col == 0:
            return nEste
        if col == 7:
            return nOeste
    # Accion Este
    if nA == nEste:
        if fil > 0 and fil < 11:
            if nDadoA >= 0.0 and nDadoA < 0.5:
                return nNorte
            else:
                return nSur
        if fil == 0:
            return nSur
        if fil == 11:
            return nNorte
    # Accion Oeste
    if nA == nOeste:
        if fil > 0 and fil < 11:
            if nDadoA >= 0.0 and nDadoA < 0.5:
                return nNorte
            else:
                return nSur
        if fil == 0:
            return nSur
        if fil == 11:
            return nNorte

# Simulamos la navegacion


def Run_Action(a, nExito):
    global aPosRM
    global next_state
    nDado = ra.random()
    i = aPosRM[0]  # Fila Posicion del robot mapa
    j = aPosRM[1]  # Columna Posicion del robot mapa
    if a == nNorte:  # El robot sube
        if i > 0:  # Bordes del Mapa
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
    if a == nSur:  # El robot baja
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

    if a == nEste:  # El robot va a la derecha
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

    if a == nOeste:  # El robot va a la izquierda
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


def QLearning(MaxSteps=100, ):
    global nM
    s = aSTATE[0][0]  # Posicion inicial
    steps = 0
    tl_rw = 0
    nM = 0
    for i in range(0, MaxSteps):
        a = Get_Greedy_Action(s)  # Samplea Accion, [0,1,2,3] = [n,s,e,o]
        sp = Run_Action(a, 0.80)
        rw = Get_RW(sp)
        tl_rw += rw
        UpDateQ(s, a, rw, sp)
        s = sp
        steps += 1
        if aPosRM == aMeta:
            break
    return tl_rw, steps


Epsilon = 0.1
Q = InitQTable(62, 4)
aList_A = ['N', 'S', 'E', 'O']
aPosRM = [0, 0]
for i in range(nMax_episodidos):
    total_rw, steps = QLearning(nMax_episodidos)
    print('Episodio: ' + str(i) + ' Steps: ' +
          str(steps) + ' Reward: ' + str(total_rw))
    Epsilon *= 0.9

print(Q)
for i in range(62):
    print(str(i) + ' -> ' + aList_A[Q[i].index(max(Q[i]))] + '\n')
