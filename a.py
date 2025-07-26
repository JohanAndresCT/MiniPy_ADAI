import time
import matplotlib.pyplot as plt

# ---------------------- Clases Base ----------------------

class Encuestado:
    def __init__(self, id, nombre, experticia, opinion):
        self.id = id
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion

    def __str__(self):
        return f"({self.id}, Nombre:'{self.nombre}', Experticia:{self.experticia}, Opinión:{self.opinion})"

class Pregunta:
    def __init__(self, id_pregunta):
        self.id_pregunta = id_pregunta
        self.encuestados = []
        self.promedio_opinion = 0.0
        self.promedio_experticia = 0.0
        self.mediana = 0.0
        self.moda = 0
        self.extremismo = 0.0
        self.consenso = 0.0

    def agregar_encuestado(self, encuestado):
        self.encuestados.append(encuestado)

    def calcular_promedios(self):
        n = len(self.encuestados)
        if n == 0:
            return
        self.promedio_opinion = sum(e.opinion for e in self.encuestados) / n
        self.promedio_experticia = sum(e.experticia for e in self.encuestados) / n

    def ordenar_opiniones(self, opiniones):
        for i in range(1, len(opiniones)):
            actual = opiniones[i]
            j = i - 1
            while j >= 0 and opiniones[j] > actual:
                opiniones[j + 1] = opiniones[j]
                j -= 1
            opiniones[j + 1] = actual
        return opiniones

    def calcular_estadisticas(self):
        n = len(self.encuestados)
        if n == 0:
            return
        opiniones = [e.opinion for e in self.encuestados]
        self.ordenar_opiniones(opiniones)

        self.mediana = opiniones[n // 2] if n % 2 == 1 else min(opiniones[n // 2 - 1], opiniones[n // 2])

        frecuencia = [0] * 11
        for op in opiniones:
            frecuencia[op] += 1
        max_freq = max(frecuencia)
        self.moda = min(i for i, f in enumerate(frecuencia) if f == max_freq)

        extremos = opiniones.count(0) + opiniones.count(10)
        self.extremismo = round(extremos / n, 2)
        self.consenso = round(max_freq / n, 2)

class Tema:
    def __init__(self, nombre):
        self.nombre = nombre
        self.preguntas = []
        self.promedio_general_opinion = 0.0
        self.promedio_general_experticia = 0.0
        self.total_encuestados = 0

    def agregar_pregunta(self, pregunta):
        self.preguntas.append(pregunta)

    def calcular_estadisticas(self):
        if not self.preguntas:
            return
        self.promedio_general_opinion = sum(p.promedio_opinion for p in self.preguntas) / len(self.preguntas)
        self.promedio_general_experticia = sum(p.promedio_experticia for p in self.preguntas) / len(self.preguntas)
        self.total_encuestados = sum(len(p.encuestados) for p in self.preguntas)

class Encuesta:
    def __init__(self):
        self.temas = []
        self.todos_encuestados = []

    def agregar_tema(self, tema):
        self.temas.append(tema)

    def agregar_encuestado_global(self, encuestado):
        self.todos_encuestados.append(encuestado)

# ---------------------- Funciones Auxiliares ----------------------

def buscar_encuestado_por_id(lista, id):
    for e in lista:
        if e.id == id:
            return e
    return None

def insertion_sort(lista, key_fn):
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and key_fn(lista[j]) > key_fn(actual):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual

def id_pregunta_a_tupla(id_str):
    return tuple(map(int, id_str.split('.')))

def ordenar_encuestados_por_pregunta(encuesta):
    for tema in encuesta.temas:
        for pregunta in tema.preguntas:
            insertion_sort(pregunta.encuestados, lambda e: (-e.opinion, -e.experticia, e.id))

def ordenar_preguntas_por_tema(encuesta):
    for tema in encuesta.temas:
        insertion_sort(
            tema.preguntas,
            lambda p: (
                -p.promedio_opinion,
                -p.promedio_experticia,
                -len(p.encuestados),
                id_pregunta_a_tupla(p.id_pregunta)
            )
        )

def ordenar_temas(encuesta):
    insertion_sort(
        encuesta.temas,
        lambda t: (
            -t.promedio_general_opinion,
            -t.promedio_general_experticia,
            -t.total_encuestados,
            int(t.nombre.split()[1])
        )
    )

def calcular_promedios_y_estadisticas(encuesta):
    for tema in encuesta.temas:
        for pregunta in tema.preguntas:
            pregunta.calcular_promedios()
            pregunta.calcular_estadisticas()
        tema.calcular_estadisticas()

def ordenar_ranking_global(encuesta):
    insertion_sort(encuesta.todos_encuestados, lambda e: (-e.experticia, -e.id))

def leer_entrada_desde_archivo(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
    secciones = contenido.split("\n\n")

    encuesta = Encuesta()
    participantes_txt = secciones[0].splitlines()

    for linea in participantes_txt:
        partes = linea.strip().split()
        id = int(partes[0])
        nombre = " ".join(partes[1:-2])
        experticia = int(partes[-2])
        opinion = int(partes[-1])
        encuesta.agregar_encuestado_global(Encuestado(id, nombre, experticia, opinion))

    for i, bloque in enumerate(secciones[1:]):
        tema = Tema(f"Tema {i + 1}")
        for linea in bloque.strip().splitlines():
            partes = linea.strip().split()
            id_pregunta = partes[0]
            ids = list(map(int, partes[1:]))
            pregunta = Pregunta(id_pregunta)
            for pid in ids:
                e = buscar_encuestado_por_id(encuesta.todos_encuestados, pid)
                if e:
                    pregunta.agregar_encuestado(e)
            tema.agregar_pregunta(pregunta)
        encuesta.agregar_tema(tema)

    return encuesta

def guardar_salida_en_archivo(encuesta, archivo_salida):
    with open(archivo_salida, "w", encoding="utf-8") as f:
        preguntas = [p for tema in encuesta.temas for p in tema.preguntas]

        max_prom = max(preguntas, key=lambda p: p.promedio_opinion)
        min_prom = min(preguntas, key=lambda p: p.promedio_opinion)
        max_med = max(preguntas, key=lambda p: p.mediana)
        min_med = min(preguntas, key=lambda p: p.mediana)
        max_mod = max(preguntas, key=lambda p: p.moda)
        min_mod = min(preguntas, key=lambda p: p.moda)
        max_ext = max(preguntas, key=lambda p: p.extremismo)
        max_con = max(preguntas, key=lambda p: p.consenso)

        f.write(f"Pregunta con mayor promedio de opinión: {max_prom.id_pregunta} ({max_prom.promedio_opinion:.2f})\n")
        f.write(f"Pregunta con menor promedio de opinión: {min_prom.id_pregunta} ({min_prom.promedio_opinion:.2f})\n")
        f.write(f"Pregunta con mayor mediana: {max_med.id_pregunta} ({max_med.mediana})\n")
        f.write(f"Pregunta con menor mediana: {min_med.id_pregunta} ({min_med.mediana})\n")
        f.write(f"Pregunta con mayor moda: {max_mod.id_pregunta} ({max_mod.moda})\n")
        f.write(f"Pregunta con menor moda: {min_mod.id_pregunta} ({min_mod.moda})\n")
        f.write(f"Pregunta con mayor extremismo: {max_ext.id_pregunta} ({max_ext.extremismo:.2f})\n")
        f.write(f"Pregunta con mayor consenso: {max_con.id_pregunta} ({max_con.consenso:.2f})\n")

# ---------------------- Comparación Sort vs Teoría ----------------------

def medir_tiempo_insertion_sort():
    print("\n--- Comparación Insertion Sort vs O(n²) ---")

    tamanos = [100, 200, 400, 800, 1600]
    tiempos_reales = []

    for n in tamanos:
        lista = [i for i in range(n, 0, -1)]  # peor caso
        start = time.time()
        insertion_sort(lista, key_fn=lambda x: x)
        end = time.time()
        duracion = end - start
        tiempos_reales.append(duracion)
        print(f"Tamaño: {n}, Tiempo real: {duracion:.6f} s")

    tiempos_teoricos = [(n**2) * 1e-7 for n in tamanos]

    plt.figure(figsize=(10, 5))
    plt.plot(tamanos, tiempos_reales, marker='o', label="Tiempo real Insertion Sort", color='blue')
    plt.plot(tamanos, tiempos_teoricos, marker='x', linestyle='--', label="Teoría O(n²)", color='red')
    plt.xlabel("Tamaño de entrada (n)")
    plt.ylabel("Tiempo (s)")
    plt.title("Comparación: Insertion Sort real vs Teoría O(n²)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("comparacion_insertion_vs_on2.png")
    plt.show()

# ---------------------- Main ----------------------

if __name__ == "__main__":
    archivo_entrada = "Test4.txt"
    archivo_salida = "Salida_Test4.txt"
    tiempos = {}

    start = time.time()
    encuesta = leer_entrada_desde_archivo(archivo_entrada)
    tiempos["leer_entrada"] = time.time() - start

    start = time.time()
    ordenar_encuestados_por_pregunta(encuesta)
    tiempos["ordenar_encuestados"] = time.time() - start

    start = time.time()
    calcular_promedios_y_estadisticas(encuesta)
    tiempos["estadisticas_1"] = time.time() - start

    start = time.time()
    ordenar_preguntas_por_tema(encuesta)
    tiempos["ordenar_preguntas"] = time.time() - start

    start = time.time()
    calcular_promedios_y_estadisticas(encuesta)
    tiempos["estadisticas_2"] = time.time() - start

    start = time.time()
    ordenar_temas(encuesta)
    tiempos["ordenar_temas"] = time.time() - start

    start = time.time()
    ordenar_ranking_global(encuesta)
    tiempos["ordenar_ranking"] = time.time() - start

    start = time.time()
    guardar_salida_en_archivo(encuesta, archivo_salida)
    tiempos["guardar_salida"] = time.time() - start

    total = sum(tiempos.values())
    print("\n--- Tiempos de ejecución por etapa ---")
    for k, v in tiempos.items():
        print(f"{k}: {v:.6f} s")
    print(f"Tiempo total: {total:.6f} s")

    # Gráfico de tiempos por etapa
    etapas = list(tiempos.keys())
    valores = list(tiempos.values())
    plt.figure(figsize=(10, 5))
    plt.bar(etapas, valores, color='steelblue')
    plt.xlabel("Etapa del procesamiento")
    plt.ylabel("Tiempo (s)")
    plt.title("Tiempo de ejecución por etapa")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("grafica_tiempos.png")
    plt.show()

    # Gráfico comparativo
    medir_tiempo_insertion_sort()
