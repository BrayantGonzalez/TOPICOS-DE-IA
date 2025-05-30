import numpy as np
from tensorflow.keras.models import load_model

# Cargar modelos
model_suma = load_model("modelo_suma.h5")
model_resta = load_model("modelo_resta.h5")
model_multi = load_model("modelo_multi.h5")
model_div = load_model("modelo_div.h5")

def calcular(op, a, b):
    entrada = np.array([[a, b]])
    if op == '+':
        return float(model_suma.predict(entrada, verbose=0))
    elif op == '-':
        return float(model_resta.predict(entrada, verbose=0))
    elif op == '*':
        return float(model_multi.predict(entrada, verbose=0))
    elif op == '/':
        return float(model_div.predict(entrada, verbose=0)) if b != 0 else "indefinido"
    else:
        return "Operación no válida"

# Pruebas
print("3 + 5 =", calcular('+', 3, 5))
print("7 - 2 =", calcular('-', 7, 2))
print("4 * 6 =", calcular('*', 4, 6))
print("8 / 2 =", calcular('/', 8, 2))
print("5 / 0 =", calcular('/', 5, 0))
