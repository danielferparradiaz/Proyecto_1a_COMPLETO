"""
=====================================================================
Proyecto 1 - Cálculo 2 (Ingeniería)
Mapeo de Curvas de Nivel en Imágenes - Aplicación del Gradiente
=====================================================================

PIPELINE COMPLETO (pasos 2, 3 y 4).

Este script toma la imagen en escala de grises generada en
"generar_terreno.py" y ejecuta el proceso de análisis por pasos:

  PASO 2 -> Suavizado con filtro gaussiano (reducir ruido antes de
            derivar, porque la derivada amplifica el ruido).
  PASO 3 -> Cálculo del gradiente con el filtro de Sobel, obteniendo
            las derivadas parciales df/dx y df/dy, y la MAGNITUD
            del gradiente |∇f|.
  PASO 4 -> Obtención de las curvas de nivel (contornos) y comparación
            visual con la magnitud del gradiente.

Cada paso guarda una imagen en la carpeta "../resultados/".

Autor: Grupo de Cálculo 2 (UAN)
=====================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage


# =====================================================================
# CARGA DE LA IMAGEN
# =====================================================================
ruta_imagen = "../resultados/terreno.png"
imagen = plt.imread(ruta_imagen)

# Si la imagen viene en color (RGB/RGBA), la convertimos a escala de
# grises y nos quedamos con una única matriz 2D. Para la conversión
# usamos los pesos estándar de luminancia (0.299, 0.587, 0.114).
if imagen.ndim == 3:
    imagen = imagen[:, :, :3]                          # descartar alfa
    imagen = (0.299 * imagen[:, :, 0] +
              0.587 * imagen[:, :, 1] +
              0.114 * imagen[:, :, 2])

# plt.imread devuelve valores en [0, 1]. Los pasamos a float en [0, 255]
# para trabajar con los valores de intensidad como una función f(x, y).
f = imagen.astype(np.float64)
if f.max() <= 1.0:            # si está en [0,1], lo escalamos a [0,255]
    f = f * 255.0

print(f"Imagen cargada: {ruta_imagen}  forma={f.shape}")


# =====================================================================
# PASO 2: SUAVIZADO DE LA IMAGEN (filtro gaussiano)
# =====================================================================
# Antes de calcular el gradiente conviene suavizar la imagen. La razón
# es matemática: la derivada amplifica las variaciones rápidas (ruido).
# Un filtro gaussiano es la convolución de f con una campana de Gauss,
# que promedia cada píxel con sus vecinos ponderados. El parámetro
# "sigma" controla cuánto se suaviza (a mayor sigma, más suave).
sigma = 2.0
f_suave = ndimage.gaussian_filter(f, sigma=sigma)


# =====================================================================
# PASO 3: CÁLCULO DEL GRADIENTE (filtro de Sobel)
# =====================================================================
# Recordemos que el gradiente de una función f(x, y) es el vector:
#
#           ∇f = ( ∂f/∂x , ∂f/∂y )
#
# En una imagen discreta no podemos derivar de forma exacta, así que
# aproximamos las derivadas parciales con el OPERADOR DE SOBEL, que es
# una convolución con unas máscaras que detectan cambios de intensidad
# en la dirección horizontal (matriz Sx) y vertical (matriz Sy).
#
# El filtro de Sobel entrega la derivada en dirección x (df/dx) con
# sobel(..., axis=1) y la dirección y (df/dy) con axis=0.

df_dx = ndimage.sobel(f_suave, axis=1)   # ∂f/∂x
df_dy = ndimage.sobel(f_suave, axis=0)   # ∂f/∂y

# Magnitud del gradiente. Es la longitud del vector gradiente:
#           |∇f| = sqrt( (∂f/∂x)^2 + (∂f/∂y)^2 )
# Nos dice CUÁNTO cambia la intensidad en cada punto (la pendiente).
magnitud = np.hypot(df_dx, df_dy)

# Dirección del gradiente (ángulo), útil para visualizar hacia dónde
# crece la función con mayor rapidez.
direccion = np.arctan2(df_dy, df_dx)


# =====================================================================
# PASO 4: CURVAS DE NIVEL (CONTORNOS)
# =====================================================================
# Una curva de nivel es el conjunto de puntos (x, y) donde f(x, y) = c
# (una constante). En el terreno equivalen a las "líneas de la misma
# altura". matplotlib las dibuja con plt.contour.
niveles = 8   # número de curvas de nivel que queremos dibujar


# =====================================================================
# VISUALIZACIÓN DE RESULTADOS
# =====================================================================
# Creamos una figura con varios subplots para comparar todos los pasos.
fig, ejes = plt.subplots(2, 3, figsize=(16, 10))

# --- (a) Imagen original ------------------------------------------------
ejes[0, 0].imshow(f, cmap="gray")
ejes[0, 0].set_title("(a) Paso 1: Imagen original f(x,y)")
ejes[0, 0].axis("off")

# --- (b) Imagen suavizada ------------------------------------------------
ejes[0, 1].imshow(f_suave, cmap="gray")
ejes[0, 1].set_title("(b) Paso 2: Imagen suavizada (gaussiano)")
ejes[0, 1].axis("off")

# --- (c) Magnitud del gradiente -----------------------------------------
# |∇f| es grande en bordes/montañas (donde la imagen cambia rápido).
im_mag = ejes[0, 2].imshow(magnitud, cmap="hot")
ejes[0, 2].set_title("(c) Paso 3: Magnitud del gradiente |∇f|")
ejes[0, 2].axis("off")
fig.colorbar(im_mag, ax=ejes[0, 2], fraction=0.046)

# --- (d) Derivada parcial respecto a x ----------------------------------
ejes[1, 0].imshow(df_dx, cmap="RdBu", vmin=-df_dx.max(), vmax=df_dx.max())
ejes[1, 0].set_title(r"(d) Derivada parcial $\partial f/\partial x$")
ejes[1, 0].axis("off")

# --- (e) Derivada parcial respecto a y ----------------------------------
ejes[1, 1].imshow(df_dy, cmap="RdBu", vmin=-df_dy.max(), vmax=df_dy.max())
ejes[1, 1].set_title(r"(e) Derivada parcial $\partial f/\partial y$")
ejes[1, 1].axis("off")

# --- (f) Curvas de nivel sobre la imagen --------------------------------
ejes[1, 2].imshow(f_suave, cmap="gray")
contornos = ejes[1, 2].contour(f_suave, levels=niveles, cmap="jet", linewidths=1.5)
ejes[1, 2].clabel(contornos, inline=True, fontsize=7, fmt="%.2f")
ejes[1, 2].set_title("(f) Paso 4: Curvas de nivel (contornos)")
ejes[1, 2].axis("off")

plt.tight_layout()
ruta_resumen = "../resultados/resumen_pasos.png"
plt.savefig(ruta_resumen, dpi=150, bbox_inches="tight")
print(f"Resumen de pasos guardado en: {ruta_resumen}")
plt.show()


# =====================================================================
# FIGURA EXTRA: comparación directa curvas de nivel vs gradiente
# =====================================================================
# Este es el resultado clave del proyecto: las curvas de nivel son
# PERPENDICULARES al gradiente. Donde las curvas están muy juntas,
# la magnitud del gradiente es grande (terreno empinado). Donde están
# separadas, el gradiente es pequeño (terreno plano).
fig2, ejes2 = plt.subplots(1, 2, figsize=(14, 6))

# Izquierda: curvas de nivel
ejes2[0].imshow(f_suave, cmap="gray")
c = ejes2[0].contour(f_suave, levels=niveles, cmap="jet", linewidths=2)
ejes2[0].clabel(c, inline=True, fontsize=8, fmt="%.2f")
ejes2[0].set_title("Curvas de nivel (alturas constantes)")
ejes2[0].axis("off")

# Derecha: magnitud del gradiente
ejes2[1].imshow(magnitud, cmap="hot")
ejes2[1].set_title("Magnitud del gradiente (pendiente)")
ejes2[1].axis("off")

plt.tight_layout()
ruta_comparacion = "../resultados/comparacion_nivel_vs_gradiente.png"
plt.savefig(ruta_comparacion, dpi=150, bbox_inches="tight")
print(f"Comparación guardada en: {ruta_comparacion}")
plt.show()

print("\n¡Proyecto completado exitosamente!")
print("Archivos generados en ../resultados/, revisa las imágenes.")