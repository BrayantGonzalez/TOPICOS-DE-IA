import random
import math

def costo(estado):
    """Calcula el número de pares de reinas que se atacan."""
    ataques = 0
    n = len(estado)
    for i in range(n):
        for j in range(i + 1, n):
            # Misma columna o misma diagonal
            if estado[i] == estado[j] or abs(estado[i] - estado[j]) == abs(i - j):
                ataques += 1
    return ataques

def generar_vecino(estado):
    """Genera un vecino moviendo una reina aleatoria en su fila."""
    vecino = estado.copy()
    fila = random.randint(0, len(estado) - 1)
    nueva_columna = random.randint(0, len(estado) - 1)
    vecino[fila] = nueva_columna
    return vecino

def recocido_simulado(n_reinas=8, temperatura_inicial=1000, enfriamiento=0.95, iteraciones_por_temp=100):
    """Algoritmo de recocido simulado para el problema de las N reinas."""
    # Estado inicial aleatorio
    estado_actual = [random.randint(0, n_reinas - 1) for _ in range(n_reinas)]
    costo_actual = costo(estado_actual)
    T = temperatura_inicial

    while T > 0.1 and costo_actual > 0:
        for _ in range(iteraciones_por_temp):
            vecino = generar_vecino(estado_actual)
            costo_vecino = costo(vecino)
            delta = costo_vecino - costo_actual

            # Si el vecino es mejor o se acepta con probabilidad e^(-delta/T)
            if delta < 0 or random.random() < math.exp(-delta / T):
                estado_actual = vecino
                costo_actual = costo_vecino

        T *= enfriamiento  # Enfriamiento exponencial

    return estado_actual, costo_actual

# Ejecución
solucion, ataques = recocido_simulado()
print(f"Solución encontrada: {solucion}")
print(f"Número de ataques: {ataques}")

# Visualización del tablero
def imprimir_tablero(estado):
    n = len(estado)
    for fila in range(n):
        linea = ""
        for columna in range(n):
            if estado[fila] == columna:
                linea += "Q "
            else:
                linea += ". "
        print(linea)

print("\nTablero:")
imprimir_tablero(solucion)