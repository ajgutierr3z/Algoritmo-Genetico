# algoritmo_genetico.py
"""
Práctica de I.A.: Resolviendo el problema del agente viajero
Autor: Ajgutierr3z
Descripción: Mediante el uso de un algoritmo genético se puede encontrar la ruta más óptima al problema clásico del agente viajero
"""
import random
import numpy as np
import matplotlib.pyplot as plt

# ---------- PARÁMETROS ----------
NUM_CIUDADES = 10
NUM_GENERACIONES = 100
POBLACION_SIZE = 100
TASA_MUTACION = 0.02
ELITISMO = True

# ---------- FUNCIONES AUXILIARES ----------
def generar_ciudades(n):
    return np.random.rand(n, 2) * 100

def distancia_total(ruta, ciudades):
    dist = 0
    for i in range(len(ruta)):
        desde = ciudades[ruta[i]]
        hasta = ciudades[ruta[(i + 1) % len(ruta)]]
        dist += np.linalg.norm(desde - hasta)
    return dist

def crear_poblacion(ciudades):
    poblacion = []
    for _ in range(POBLACION_SIZE):
        ruta = list(range(len(ciudades)))
        random.shuffle(ruta)
        poblacion.append(ruta)
    return poblacion

def seleccionar(poblacion, ciudades):
    puntajes = [(ruta, distancia_total(ruta, ciudades)) for ruta in poblacion]
    puntajes.sort(key=lambda x: x[1])
    seleccionados = [x[0] for x in puntajes[:POBLACION_SIZE // 2]]
    return seleccionados

def cruzar(padre1, padre2):
    i, j = sorted(random.sample(range(len(padre1)), 2))
    hijo = [-1] * len(padre1)
    hijo[i:j] = padre1[i:j]
    ptr = 0
    for val in padre2:
        if val not in hijo:
            while hijo[ptr] != -1:
                ptr += 1
            hijo[ptr] = val
    return hijo

def mutar(ruta):
    if random.random() < TASA_MUTACION:
        i, j = random.sample(range(len(ruta)), 2)
        ruta[i], ruta[j] = ruta[j], ruta[i]
    return ruta

def siguiente_generacion(poblacion, ciudades):
    seleccionados = seleccionar(poblacion, ciudades)
    siguiente = seleccionados[:1] if ELITISMO else []
    while len(siguiente) < POBLACION_SIZE:
        padre1, padre2 = random.sample(seleccionados, 2)
        hijo = cruzar(padre1, padre2)
        hijo = mutar(hijo)
        siguiente.append(hijo)
    return siguiente

def mostrar_ruta(ruta, ciudades):
    puntos = [ciudades[i] for i in ruta + [ruta[0]]]
    x, y = zip(*puntos)
    plt.plot(x, y, 'o-', color='blue')
    plt.title("Ruta óptima encontrada")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

# ---------- EJECUCIÓN ----------
ciudades = generar_ciudades(NUM_CIUDADES)
poblacion = crear_poblacion(ciudades)
mejores_distancias = []

for gen in range(NUM_GENERACIONES):
    poblacion = siguiente_generacion(poblacion, ciudades)
    mejor_ruta = min(poblacion, key=lambda r: distancia_total(r, ciudades))
    mejor_dist = distancia_total(mejor_ruta, ciudades)
    mejores_distancias.append(mejor_dist)
    print(f"Generación {gen + 1}: {mejor_dist:.2f}")

# ---------- RESULTADOS ----------
mostrar_ruta(mejor_ruta, ciudades)
plt.plot(mejores_distancias, color='green')
plt.title("Evolución de la distancia mínima")
plt.xlabel("Generaciones")
plt.ylabel("Distancia")
plt.grid(True)
plt.show()
