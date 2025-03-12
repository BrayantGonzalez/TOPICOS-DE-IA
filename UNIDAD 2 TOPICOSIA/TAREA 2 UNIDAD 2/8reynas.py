import random
import time

def generar_estado():
    """Genera un estado inicial aleatorio para el problema de las 8 reinas."""
    return [random.randint(0, 7) for _ in range(8)]

def evaluar(estado):
    """Cuenta la cantidad de conflictos entre reinas en el tablero."""
    conflictos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if estado[i] == estado[j] or abs(estado[i] - estado[j]) == abs(i - j):
                conflictos += 1
    return conflictos

def obtener_vecinos(estado):
    """Genera vecinos modificando la posición de una única reina por columna."""
    vecinos = []
    for i in range(8):
        for nueva_fila in range(8):
            if estado[i] != nueva_fila:
                vecino = estado[:]
                vecino[i] = nueva_fila
                vecinos.append(vecino)
    return vecinos

def busqueda_tabu(max_iteraciones=500, tabu_tamano=20):
    """Implementa el algoritmo de búsqueda Tabú para resolver el problema de las 8 reinas."""
    estado_actual = generar_estado()
    mejor_estado = estado_actual[:]
    mejor_valor = evaluar(mejor_estado)
    tabu_lista = []
    
    for _ in range(max_iteraciones):
        vecinos = obtener_vecinos(estado_actual)
        vecinos = sorted(vecinos, key=evaluar)  # Ordenar por menor número de conflictos

        for vecino in vecinos:
            if vecino not in tabu_lista or evaluar(vecino) < mejor_valor:
                estado_actual = vecino
                break
        
        tabu_lista.append(estado_actual)
        if len(tabu_lista) > tabu_tamano:
            tabu_lista.pop(0)

        valor_actual = evaluar(estado_actual)
        if valor_actual < mejor_valor:
            mejor_estado = estado_actual[:]
            mejor_valor = valor_actual

        if mejor_valor == 0:  # Si encontramos una solución óptima, terminamos
            break

    return mejor_estado, mejor_valor

# Ejecutar el algoritmo y medir el tiempo de ejecución
inicio = time.time()
solucion, conflictos = busqueda_tabu()
tiempo_total = time.time() - inicio

# Mostrar resultados
print("Solución encontrada:", solucion)
print("Conflictos:", conflictos)
print("Tiempo de ejecución:", tiempo_total, "segundos")