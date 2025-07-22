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

# ---------------------- Entrada / Salida ----------------------

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
        f.write("Resultados de la encuesta:\n\n")
        for tema in encuesta.temas:
            f.write(f"[{tema.promedio_general_opinion:.2f}] {tema.nombre}:\n")
            for p in tema.preguntas:
                f.write(f" [{p.promedio_opinion:.2f}] Pregunta {p.id_pregunta}: ({', '.join(str(e.id) for e in p.encuestados)})\n")
            f.write("\n")

        f.write("Lista de encuestados:\n")
        for e in encuesta.todos_encuestados:
            f.write(f"{e}\n")
        f.write("\n")

        preguntas = [p for tema in encuesta.temas for p in tema.preguntas]

        max_prom = max(preguntas, key=lambda p: (p.promedio_opinion, -id_pregunta_a_tupla(p.id_pregunta)[0], -id_pregunta_a_tupla(p.id_pregunta)[1]))
        min_prom = min(preguntas, key=lambda p: (p.promedio_opinion, id_pregunta_a_tupla(p.id_pregunta)))
        max_exp = max(preguntas, key=lambda p: (p.promedio_experticia, -id_pregunta_a_tupla(p.id_pregunta)[0], -id_pregunta_a_tupla(p.id_pregunta)[1]))
        min_exp = min(preguntas, key=lambda p: (p.promedio_experticia, id_pregunta_a_tupla(p.id_pregunta)))

        max_med_val = max(p.mediana for p in preguntas)
        max_med = min((p for p in preguntas if p.mediana == max_med_val), key=lambda p: id_pregunta_a_tupla(p.id_pregunta))

        min_med_val = min(p.mediana for p in preguntas)
        min_med = min((p for p in preguntas if p.mediana == min_med_val), key=lambda p: id_pregunta_a_tupla(p.id_pregunta))

        max_mod_val = max(p.moda for p in preguntas)
        max_mod = min((p for p in preguntas if p.moda == max_mod_val), key=lambda p: id_pregunta_a_tupla(p.id_pregunta))

        min_mod_val = min(p.moda for p in preguntas)
        min_mod = min((p for p in preguntas if p.moda == min_mod_val), key=lambda p: id_pregunta_a_tupla(p.id_pregunta))

        max_ext_val = max(p.extremismo for p in preguntas)
        max_ext = min((p for p in preguntas if p.extremismo == max_ext_val), key=lambda p: id_pregunta_a_tupla(p.id_pregunta))

        max_con = max(preguntas, key=lambda p: (p.consenso, -p.moda, id_pregunta_a_tupla(p.id_pregunta)))

        f.write("Resultados:\n")
        f.write(f"  Pregunta con mayor promedio de opinion: [{max_prom.promedio_opinion:.2f}] Pregunta: {max_prom.id_pregunta}\n")
        f.write(f"  Pregunta con menor promedio de opinion: [{min_prom.promedio_opinion:.2f}] Pregunta: {min_prom.id_pregunta}\n")
        f.write(f"  Pregunta con mayor promedio de experticia: [{max_exp.promedio_experticia:.2f}] Pregunta: {max_exp.id_pregunta}\n")
        f.write(f"  Pregunta con menor promedio de experticia: [{min_exp.promedio_experticia:.2f}] Pregunta: {min_exp.id_pregunta}\n")
        f.write(f"  Pregunta con Mayor mediana de opinion: [{int(max_med.mediana)}] Pregunta: {max_med.id_pregunta}\n")
        f.write(f"  Pregunta con menor mediana de opinion: [{int(min_med.mediana)}] Pregunta: {min_med.id_pregunta}\n")
        f.write(f"  Pregunta con mayor moda de opinion: [{max_mod.moda}] Pregunta: {max_mod.id_pregunta}\n")
        f.write(f"  Pregunta con menor moda de opinion: [{min_mod.moda}] Pregunta: {min_mod.id_pregunta}\n")
        f.write(f"  Pregunta con mayor extremismo: [{max_ext.extremismo:.2f}] Pregunta: {max_ext.id_pregunta}\n")
        f.write(f"  Pregunta con mayor consenso: [{max_con.consenso:.2f}] Pregunta: {max_con.id_pregunta}\n")


# ---------------------- Main ----------------------

if __name__ == "__main__":
    archivo_entrada = "Test2.txt"
    archivo_salida = "Salida_Test2.txt"

    encuesta = leer_entrada_desde_archivo(archivo_entrada)

    ordenar_encuestados_por_pregunta(encuesta)
    calcular_promedios_y_estadisticas(encuesta)

    ordenar_preguntas_por_tema(encuesta)
    calcular_promedios_y_estadisticas(encuesta)

    ordenar_temas(encuesta)
    ordenar_ranking_global(encuesta)

    guardar_salida_en_archivo(encuesta, archivo_salida)
    print(f"Análisis guardado en {archivo_salida}")
