# -*- coding: UTF-8 -*-
import random as RA
import time
import math

###########################################
ALPHA = 0.1             # Tasa de Aprendizaje
GAMMA = 0.9             # Factor de Descuento
nMAX_EPISODIOS = 1000

# Acciones
nNORTE = 0
nSUR = 1
nESTE = 2
nWESTE = 3

# Datos de Navegación
# (NOTA) Se podrian ignorar con un if
nFIL_MIN = 0
nFIL_MAX = 11
nCOL_MIN = 0
nCOL_MAX = 14
aMETA = [10, 11]  # Posicion de destino del robot

aMAPA = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 0
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 1
    [1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1],  # 2
    [1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, -1, -1, 1],  # 3
    [1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, 1],  # 4
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 5
    [1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1],  # 6
    [1, 1, -1, -1, -1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1],  # 7
    [1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 8
    [1, 1, -1, 1, 1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1],  # 9
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 10
    [1, 1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1]  # 11
]

aSTATE = [
    [0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14],  # 0
    [15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29],  # 1
    [30,  31,  -1,  -1,  -1,  32,  -1,  -1,  -1,  33,  34,  35,  36,  37,  38],  # 2
    [39,  40,  -1,  41,  42,  43,  44,  45,  -1,  46,  47,  48,  -1,  -1,  49],  # 3
    [50,  51,  -1,  52,  53,  54,  55,  56,  57,  58,  59,  -1,  -1,  -1,  60],  # 4
    [61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75],  # 5
    [76,  77,  78,  79,  80,  81,  82,  83,  -1,  -1,  84,  85,  86,  87,  88],  # 6
    [89,  90,  -1,  -1,  -1,  91,  92,  93,  94,  -1,  -1,  -1,  95,  96,  -1],  # 7
    [97,  98,  -1,  99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],  # 8
    [111, 112,  -1, 113, 114, 115,  -1, 116, 117,  -1,  -1,  -1,  -1, 118, 119],  # 9
    [120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134],  # 10
    [135, 136, 137, 138,  -1,  -1,  -1, 139, 140, 141, 142, 143, 144, 145,  -1]  # 11
]

# Genera QTABLE -> nS = Estados , nA = Acciones


def InitQ_Table(nS, nA):
    aQ = [[0.0 for i in range(nA)] for i in range(nS)]
    return aQ

# Estado Inicial del Robot


def Init_State():
    aPosRM = [0, 0]
    return aPosRM  # Poicion del RObot en el mapa


def Get_Greedy_Action(nS):
    if RA.random() > Epsilon:
        a = Get_Max_Action(nS)
    else:
        a = RA.randint(0, 3)
    return a

# Samplear la mejor opcion


def Get_Max_Action(nS):
    return Q[nS].index(max(Q[nS]))

# Calcular la rewards


def Get_Rw(sp, fi, co):
    if fi == aMETA[0] and co == aMETA[1]:
        return + 1, True
    else:
        return - 1, False

# Q(.) = State(1), a=Accion, r=Reward, sp=State


def UpDateQ(s, a, r, sp):
    maxQ = max(Q[sp])
    Q[s][a] = Q[s][a] + ALPHA * (r + GAMMA * maxQ - Q[s][a])  # CAMBIO AQUI

# Simulando navegación


def Run_Action(a, nEXITO):
    global aPosRM, next_state
    nDado = RA.random()  # Se Tira el dado
    i = aPosRM[0]  # Fila Posicion del RObot Mapa
    j = aPosRM[1]  # Columna Posicion del RObot Mapa
    if nDado >= 0.0 and nDado <= nEXITO:  # Probabilidad de exito
        ############################################
        if a == nNORTE:  # El robot Sube
            if i > nFIL_MIN:
                if aMAPA[i-1][j] != -1:  # Hay una muralla?
                    i -= 1
                    j = j
                    aPosRM = [i, j]
                    next_state = aSTATE[i][j]  # Actualizar nuevo Estado
                else:
                    i = i
                    j = j
                    aPosRM = [i, j]
                    next_state = aSTATE[i][j]  # Actualizar nuevo Estado
            else:
                i = i
                j = j
                aPosRM = [i, j]
                next_state = aSTATE[i][j]  # Actualizar nuevo Estado
        ############################################
        if a == nSUR:  # El robot baja
            if i < nFIL_MAX:
                if aMAPA[i+1][j] != -1:  # Hay una muralla?
                    i += 1
                    j = j
                    aPosRM = [i, j]
                    next_state = aSTATE[i][j]  # Actualizar nuevo Estado
                else:
                    i = i
                    j = j
                    aPosRM = [i, j]
                    next_state = aSTATE[i][j]  # Actualizar nuevo Estado
            else:
                i = i
                j = j
                aPosRM = [i, j]
                next_state = aSTATE[i][j]  # Actualizar nuevo Estado
        ############################################
        if a == nESTE:  # El robot baja
            if j < nCOL_MAX:
                if aMAPA[i][j+1] != -1:  # Hay una muralla?
                    i = i
                    j += 1
                    aPosRM = [i, j]
                    next_state = aSTATE[i][j]  # Actualizar nuevo Estado
                else:
                    i = i
                    j = j
                    aPosRM = [i, j]
                    next_state = aSTATE[i][j]  # Actualizar nuevo Estado
            else:
                i = i
                j = j
                aPosRM = [i, j]
                next_state = aSTATE[i][j]  # Actualizar nuevo Estado
        ############################################
        if a == nWESTE:  # El robot baja
            if j > nCOL_MIN:
                if aMAPA[i][j-1] != -1:  # Hay una muralla?
                    i = i
                    j -= 1
                    aPosRM = [i, j]
                    next_state = aSTATE[i][j]  # Actualizar nuevo Estado
                else:
                    i = i
                    j = j
                    aPosRM = [i, j]
                    next_state = aSTATE[i][j]  # Actualizar nuevo Estado
            else:
                i = i
                j = j
                aPosRM = [i, j]
                next_state = aSTATE[i][j]  # Actualizar nuevo Estado
    return next_state, i, j

# Q-Learning


def QLearning(MaxSteps=100, lFlag=False):
    global nM
    s = aSTATE[0][0]  # numero del estado [1.2.3.4....145]
    steps = 0
    tl_rw = 0
    nM = 0
    for i in range(0, MaxSteps):
        a = Get_Greedy_Action(s)
        # print(aPosRM)
        sp, f, c = Run_Action(a, 0.95)
        rw, t = Get_Rw(sp, f, c)
        tl_rw += rw
        UpDateQ(s, a, rw, sp)
        s = sp
        steps += 1
        if t == True:
            nM += 1
            break
    return tl_rw, steps


# ----------MAIN----------
Epsilon = 0.1
Q = InitQ_Table(146, 4)
aList_A = ['N', 'S', 'E', 'O']
aPosRM = [0, 0]

for i in range(1000):
    total_rw, steps = QLearning(1000)
    print("Episodio = ", i, " , Steps = ", steps, " , Reward = ", total_rw, " , Epsilon = ", Epsilon)
    Epsilon *= 0.9

print(Q)
aOPTIMO = aSTATE

# Crea un mapa con los movimientos optimos
for i in range(146):
    for s in range(len(aOPTIMO)):  # f , c = Q.index(i)
        for z in range(len(aOPTIMO[s])):
            if aOPTIMO[s][z] == i:
                aOPTIMO[s][z] = aList_A[Q[i].index(max(Q[i]))]
                continue
            if aOPTIMO[s][z] == -1:
                aOPTIMO[s][z] = '▇'
for i in aOPTIMO:
    print(i)
