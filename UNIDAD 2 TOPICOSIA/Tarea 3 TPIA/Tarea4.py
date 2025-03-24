import random
import time

def inicializar_tablero():
    return [random.randint(0, 7) for _ in range(8)]

def calcular_conflictos(tablero):
    conflictos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if tablero[i] == tablero[j] or abs(tablero[i] - tablero[j]) == abs(i - j):
                conflictos += 1
    return conflictos

def generar_vecinos(tablero):
    vecinos = []
    for i in range(8):
        for j in range(8):
            if tablero[i] != j:
                vecino = list(tablero)
                vecino[i] = j
                vecinos.append(vecino)
    return vecinos

def busqueda_tabu(max_iteraciones, tamano_tabu):
    tablero = inicializar_tablero()
    mejor_tablero = list(tablero)
    lista_tabu = []
    movimientos = 0

    inicio = time.time()

    for iteracion in range(max_iteraciones):
        vecinos = generar_vecinos(tablero)
        mejor_vecino = None
        mejor_conflictos = float('inf')

        for vecino in vecinos:
            if vecino not in lista_tabu:
                conflictos = calcular_conflictos(vecino)
                if conflictos < mejor_conflictos:
                    mejor_conflictos = conflictos
                    mejor_vecino = vecino

        if mejor_vecino is None:
            break

        tablero = mejor_vecino
        movimientos += 1

        if calcular_conflictos(tablero) < calcular_conflictos(mejor_tablero):
            mejor_tablero = list(tablero)

        lista_tabu.append(list(tablero))
        if len(lista_tabu) > tamano_tabu:
            lista_tabu.pop(0)

    fin = time.time()
    tiempo_ejecucion = fin - inicio

    return mejor_tablero, movimientos, tiempo_ejecucion

# Parámetros
max_iteraciones = 1000
tamano_tabu = 10

# Ejecución
mejor_tablero, movimientos, tiempo_ejecucion = busqueda_tabu(max_iteraciones, tamano_tabu)

# Resultados
print("Mejor tablero encontrado:", mejor_tablero)
print("Número de movimientos:", movimientos)
print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")