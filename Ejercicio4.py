
import numpy as np

matrix_Trancicion = np.array(
    [[0.9, 0.07, 0.03], [0.85, 0.1, 0.05], [0.6, 0.1, 0.3]])
# vector de probabilidades historicas
x_0 = np.array([0.7, 0.2, 0.1])  # produccion, mantencion,reparacion

x_7 = np.dot(x_0, np.linalg.matrix_power(matrix_Trancicion, 7))
print(
    "Probabilidad de que la maquina funcione correctamente durante 7 días ===> "+str(x_7[0]))

x_3 = np.dot(x_0, np.linalg.matrix_power(matrix_Trancicion, 3))
print(
    "Probabilidad de que la maquina entre en mantencion 3 días ===> "+str(x_3[1]))

x_5 = np.dot(x_0, np.linalg.matrix_power(matrix_Trancicion, 5))
print(
    "Probabilidad de que entre en mantencion en 5 días ===> "+str(x_3[2]))

# x_k = np.dot(x_0, np.linalg.matrix_power(matrix_Trancicion, 7))
# print(x_k)
