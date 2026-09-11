"""
=====================================================================
Proyecto 1 - Cálculo 2 (Ingeniería)
Generador del informe en PDF usando fpdf2.
Lee las imágenes de ../resultados/ y produce ../Proyecto_1a_informe.pdf
=====================================================================
"""

from fpdf import FPDF

FONT_REG = "/Library/Fonts/Arial Unicode.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_ITALIC = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"

R = "../resultados/"


class InformePDF(FPDF):
    def header(self):
        self.set_font("reg", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, "Proyecto 1 - Mapeo de Curvas de Nivel en Imagenes (Calculo 2)", align="R")
        self.ln(6)

    def footer(self):
        self.set_y(-12)
        self.set_font("reg", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Pagina {self.page_no()}", align="C")

    def titulo(self, texto, nivel=1):
        self.ln(3)
        if nivel == 1:
            self.set_font("bold", "", 16)
            self.set_text_color(20, 40, 90)
        elif nivel == 2:
            self.set_font("bold", "", 13)
            self.set_text_color(40, 60, 110)
        else:
            self.set_font("bold", "", 11)
            self.set_text_color(60, 80, 130)
        self.multi_cell(0, 7, texto)
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def parrafo(self, texto):
        self.set_font("reg", "", 10.5)
        self.multi_cell(0, 5.6, texto)
        self.ln(2)

    def formula(self, texto):
        self.set_font("reg", "", 11)
        self.set_x(20)
        self.multi_cell(0, 6, texto, align="C")
        self.ln(2)

    def imagen(self, ruta, titulo, ancho=160):
        self.ln(1)
        self.set_font("italic", "", 9)
        self.set_text_color(80, 80, 80)
        self.cell(0, 5, titulo, align="C")
        self.ln(2)
        self.set_text_color(0, 0, 0)
        self.image(ruta, w=ancho, x=(210 - ancho) / 2)
        self.ln(4)


pdf = InformePDF("P", "mm", "A4")
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_font("reg", "", FONT_REG)
pdf.add_font("bold", "", FONT_BOLD)
pdf.add_font("italic", "", FONT_ITALIC)

pdf.add_page()

# ---- Portada -------------------------------------------------------------
pdf.ln(25)
pdf.set_font("bold", "", 22)
pdf.set_text_color(20, 40, 90)
pdf.multi_cell(0, 10, "Proyecto 1\nMapeo de Curvas de Nivel en Imagenes", align="C")
pdf.ln(4)
pdf.set_font("italic", "", 13)
pdf.set_text_color(80, 80, 80)
pdf.multi_cell(0, 7, "Aplicacion del Gradiente (Calculo 2) con Asistencia de IA", align="C")
pdf.ln(8)
pdf.set_font("reg", "", 12)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 6, "Curso: Calculo 2 - Ingenieria\n\nIntegrantes: [Nombre 1], [Nombre 2], [Nombre 3], [Nombre 4]\n\nFecha de entrega: 31 de agosto", align="C")
pdf.ln(6)

# ---- 1. Marco teorico ----------------------------------------------------
pdf.titulo("1. Marco Teorico", 1)
pdf.titulo("1.1 Que es una curva de nivel y como se relaciona con el gradiente", 2)
pdf.parrafo(
    "Una funcion de dos variables f(x, y) asigna un numero a cada punto del plano. "
    "Para visualizarla, una herramienta clave son las curvas de nivel, que son el "
    "conjunto de puntos donde la funcion toma un valor constante:"
)
pdf.formula("f(x, y) = c")
pdf.parrafo(
    "En un mapa topografico, cada curva de nivel une puntos que estan a la misma "
    "altura. Las curvas separadas indican terreno suave, mientras que las curvas muy "
    "juntas indican una pendiente pronunciada. El gradiente de f es el vector de sus "
    "derivadas parciales:"
)
pdf.formula("\u2207f = ( \u2202f/\u2202x ,  \u2202f/\u2202y )")
pdf.parrafo(
    "El gradiente tiene dos propiedades fundamentales que conectan directamente con "
    "las curvas de nivel: (1) Direccion: \u2207f apunta en la direccion de maximo "
    "crecimiento de la funcion. (2) Perpendicularidad: \u2207f es siempre perpendicular "
    "a las curvas de nivel en cada punto. Esto explica por que la magnitud del "
    "gradiente es grande exactamente donde las curvas de nivel estan mas apretadas "
    "(zonas empinadas) y pequena donde estan separadas (zonas planas)."
)

pdf.titulo("1.2 De la funcion matematica a la imagen en escala de grises", 2)
pdf.parrafo(
    "Una imagen en escala de grises es, literalmente, una funcion de dos variables: "
    "cada pixel tiene una posicion (x, y) y un valor de intensidad (brillo) entre 0 "
    "(negro) y 255 (blanco). Ese valor de brillo es f(x, y). Por eso todo el aparato "
    "matematico del gradiente aplica de forma directa: \u2202f/\u2202x mide cuanto cambia "
    "el brillo al movernos en la direccion horizontal; \u2202f/\u2202y mide el cambio en la "
    "vertical; y la magnitud |\u2207f| detecta los bordes (cambios bruscos de intensidad), "
    "la base del procesamiento digital de imagenes."
)

pdf.titulo("1.3 Usos del mapeo de contornos en ingenieria multimedia", 2)
pdf.parrafo(
    "Modelado de terrenos (GIS / topografia): los mapas de curvas de nivel permiten "
    "representar la elevacion de un terreno en 2D; el gradiente indica la pendiente y "
    "ayuda a planear carreteras, drenajes o zonas de riesgo.\n\n"
    "Realidad aumentada y vision por computador: la deteccion de bordes (magnitud del "
    "gradiente) permite reconocer objetos, esquinas y superficies para superponer "
    "informacion virtual sobre el mundo real."
)

# ---- 2. Metodologia ------------------------------------------------------
pdf.titulo("2. Metodologia", 1)
pdf.parrafo(
    "El trabajo se desarrollo en cuatro pasos usando Python con las librerias numpy, "
    "scipy y matplotlib."
)
pdf.parrafo(
    "Paso 1: eleccion de la imagen (terreno sintetico definido por una funcion f(x, y)).\n"
    "Paso 2: suavizado con filtro gaussiano (sigma = 2) usando scipy.ndimage.gaussian_filter.\n"
    "Paso 3: calculo del gradiente con el operador de Sobel usando scipy.ndimage.sobel.\n"
    "Paso 4: obtencion de curvas de nivel con matplotlib.pyplot.contour."
)

pdf.titulo("2.1 Justificacion del suavizado previo", 2)
pdf.parrafo(
    "Derivar una senal ruidosa amplifica el ruido (la derivada de una oscilacion rapida "
    "es una oscilacion grande). Por eso, antes de calcular el gradiente se aplica un "
    "filtro gaussiano, que promedia cada pixel con sus vecinos ponderados por una "
    "campana de Gauss. Esto suaviza variaciones pequenas sin perder la estructura "
    "grande del terreno."
)

pdf.titulo("2.2 El gradiente discreto: operador de Sobel", 2)
pdf.parrafo(
    "Como la imagen es discreta, las derivadas parciales se aproximan con el operador "
    "de Sobel, que convoluciona la imagen con dos mascaras pequenas (una para x y otra "
    "para y). Con ellas obtenemos \u2202f/\u2202x y \u2202f/\u2202y, y luego la magnitud:"
)
pdf.formula("|\u2207f| = \u221a( (\u2202f/\u2202x)\u00b2 + (\u2202f/\u2202y)\u00b2 )")

# ---- 3. Resultados -------------------------------------------------------
pdf.titulo("3. Resultados", 1)
pdf.parrafo("A continuacion se muestran las imagenes de cada paso.")

pdf.titulo("Paso 1 - Imagen original", 3)
pdf.parrafo(
    "Se genera un terreno sintetico definido como suma de gaussianas (montanas) mas "
    "una rampa, donde el brillo de cada pixel es la altura f(x, y)."
)
pdf.imagen(R + "terreno.png", "Figura 1. Imagen original en escala de grises (terreno sintetico).", ancho=90)

pdf.titulo("Pasos 2 a 4 - Resumen", 3)
pdf.imagen(R + "resumen_pasos.png", "Figura 2. Resumen: suavizado, gradiente, derivadas parciales y curvas de nivel.", ancho=180)

pdf.titulo("Resultado clave - Curvas de nivel vs. gradiente", 3)
pdf.imagen(R + "comparacion_nivel_vs_gradiente.png", "Figura 3. Comparacion curvas de nivel vs. magnitud del gradiente.", ancho=175)

pdf.titulo("Observaciones", 3)
pdf.parrafo(
    "- Las curvas de nivel dibujan con claridad la montana principal, las colinas y el "
    "valle, tal como un mapa topografico.\n"
    "- La magnitud del gradiente es maxima precisamente en los bordes de las montanas, "
    "donde el brillo cambia mas rapido. Esto confirma la relacion teorica: pendiente "
    "grande - gradiente grande - curvas de nivel juntas.\n"
    "- Las tres ideas (curva de nivel, gradiente y derivadas parciales) son totalmente "
    "coherentes entre si, comprobando visualmente la teoria del curso."
)

# ---- 4. Papel de la IA ---------------------------------------------------
pdf.titulo("4. Papel de la IA en el proyecto", 1)
pdf.parrafo(
    "La IA (ChatGPT / OpenCode) se uso como asistente, no como reemplazo del trabajo. "
    "Las preguntas mas relevantes que le hicimos fueron:"
)
pdf.parrafo(
    "1. 'Por que conviene suavizar una imagen antes de calcular el gradiente?' -> Nos "
    "explico que la derivada amplifica el ruido y que un filtro gaussiano es la via "
    "estandar para atenuarlo.\n"
    "2. 'Que librerias de Python y que funciones se usan para el filtro de Sobel y las "
    "curvas de nivel?' -> Indico scipy.ndimage.sobel, gaussian_filter y matplotlib.contour.\n"
    "3. 'Como se relacionan matematicamente las curvas de nivel con el gradiente?' -> "
    "Recordo que son ortogonales entre si.\n"
    "4. 'Como genero una imagen propia en escala de grises que represente una funcion "
    "f(x, y)?' -> Sugirio construir el terreno con gaussianas."
)
pdf.parrafo(
    "Aporte: la IA acelero la parte de programacion y aclaro conceptos, pero el diseno "
    "del experimento, la interpretacion de resultados y la redaccion de este informe "
    "fueron realizados por el grupo."
)

# ---- 5. Reflexion --------------------------------------------------------
pdf.titulo("5. Reflexion sobre la experiencia de aprendizaje", 1)
pdf.parrafo(
    "Este proyecto nos permitio materializar un concepto abstracto: ver el gradiente "
    "funcionando sobre una imagen real. Entender que cada pixel es f(x, y) y que el "
    "brillo cambia segun \u2207f hizo mucho mas tangible la idea de derivada parcial y de "
    "vector gradiente.\n\n"
    "La IA fue util sobre todo para desbloquear dudas tecnicas de programacion y para "
    "reformular conceptos en ejemplos concretos. El principal aprendizaje fue saber que "
    "preguntar: la calidad de la respuesta de la IA depende de la calidad de la "
    "pregunta, y eso exige haber estudiado la teoria antes."
)

# ---- 6. Codigo fuente ----------------------------------------------------
pdf.titulo("6. Codigo fuente", 1)
pdf.parrafo(
    "El codigo completo y documentado se encuentra en la carpeta codigo/:\n"
    "- generar_terreno.py: genera la imagen en escala de grises (Paso 1).\n"
    "- proyecto.py: ejecuta los pasos 2 a 4 y produce las figuras de resultados."
)

pdf.output("../Proyecto_1a_informe.pdf")
print("PDF generado: ../Proyecto_1a_informe.pdf")