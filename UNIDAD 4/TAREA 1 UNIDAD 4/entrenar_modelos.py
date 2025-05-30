import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Función para crear datos de entrenamiento
def crear_datos(operacion):
    x_data, y_data = [], []
    for i in range(10):
        for j in range(10):
            x_data.append([i, j])
            if operacion == '+':
                y_data.append(i + j)
            elif operacion == '-':
                y_data.append(i - j)
            elif operacion == '*':
                y_data.append(i * j)
            elif operacion == '/':
                y_data.append(i / j if j != 0 else 0)
    return np.array(x_data), np.array(y_data)

# Función para crear el modelo
def crear_modelo():
    model = Sequential([
        Dense(16, input_dim=2, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Crear y guardar modelos
operaciones = {'+': 'modelo_suma.h5', '-': 'modelo_resta.h5',
               '*': 'modelo_multi.h5', '/': 'modelo_div.h5'}

for op, filename in operaciones.items():
    x, y = crear_datos(op)
    model = crear_modelo()
    model.fit(x, y, epochs=300, verbose=1)
    model.save(filename)

print("Modelos entrenados y guardados con éxito.")
