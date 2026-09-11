"""
=====================================================================
Proyecto 1 - Cálculo 2 (Ingeniería)
Mapeo de Curvas de Nivel en Imágenes - Aplicación del Gradiente
=====================================================================

PASO 1: Elección de la imagen en escala de grises.

En este archivo generamos UNA IMAGEN PROPIA (permitida por la actividad)
que representa un terreno topográfico. La clave del proyecto es darnos
cuenta de que una imagen en escala de grises es, matemáticamente, una
función de dos variables:

        intensidad = f(x, y)

donde (x, y) es la posición del píxel y f(x, y) es su nivel de brillo
(0 = negro, 255 = blanco).

Construimos el terreno como suma de "colinas" (funciones gaussianas),
de modo que f(x, y) es una función suave y diferenciable. Esto nos
permite, más adelante, comparar las curvas de nivel con el gradiente.

Autor: Grupo de Cálculo 2 (UAN)
=====================================================================
"""

import numpy as np
import matplotlib.pyplot as plt


def f_terreno(x, y):
    """
    Función f(x, y) que representa la altura de un terreno.
    Es una combinación de funciones gaussianas que forman montañas y
    un valle, más una rampa suave que da pendiente general.

    Cada término de la forma A * exp(-((x-x0)^2 + (y-y0)^2) / (2*s^2))
    es una "colina" gaussiana centrada en (x0, y0) de amplitud A y
    anchura s.
    """
    # Montaña principal (alta y ancha), centrada en (300, 350)
    p1 = 1.00 * np.exp(-(((x - 300) ** 2) + ((y - 350) ** 2)) / (2 * 90 ** 2))

    # Colina secundaria (más baja), centrada en (150, 120)
    p2 = 0.55 * np.exp(-(((x - 150) ** 2) + ((y - 120) ** 2)) / (2 * 55 ** 2))

    # Colina pequeña, centrada en (430, 150)
    p3 = 0.40 * np.exp(-(((x - 430) ** 2) + ((y - 150) ** 2)) / (2 * 45 ** 2))

    # Valle (depresión) - gaussiana negativa cerca de (250, 220)
    p4 = -0.35 * np.exp(-(((x - 250) ** 2) + ((y - 220) ** 2)) / (2 * 40 ** 2))

    # Rampa suave de sur a norte (pendiente lineal) para dar dirección
    rampa = 0.0015 * y

    return p1 + p2 + p3 + p4 + rampa


# --- Tamaño de la imagen ---------------------------------------------------
# Usamos una cuadrícula de 512x512 píxeles. x e y son las coordenadas.
N = 512
x = np.linspace(0, 511, N)
y = np.linspace(0, 511, N)
X, Y = np.meshgrid(x, y)          # crea las matrices de coordenadas (x, y)

# --- Evaluamos f(x, y) en todos los píxeles --------------------------------
Z = f_terreno(X, Y)               # matriz de alturas de tamaño N x N

# --- Normalizamos los valores a escala de grises [0, 255] ------------------
# El gris más oscuro corresponde a la parte más baja y el más claro a la
# parte más alta del terreno (o viceversa, es indistinto para el análisis).
Z_norm = (Z - Z.min()) / (Z.max() - Z.min())   # escalar a [0, 1]
imagen = (Z_norm * 255).astype(np.uint8)        # escalar a [0, 255] enteros

# --- Guardamos la imagen en escala de grises -------------------------------
ruta_guardado = "../resultados/terreno.png"
plt.imsave(ruta_guardado, imagen, cmap="gray", vmin=0, vmax=255)
print(f"Imagen generada y guardada en: {ruta_guardado}")
print(f"Tamaño: {imagen.shape}  |  min={imagen.min()}  max={imagen.max()}")

# --- (Opcional) Mostrar una vista previa -----------------------------------
plt.imshow(imagen, cmap="gray")
plt.title("Imagen original en escala de grises (terreno sintético)")
plt.axis("off")
plt.show()