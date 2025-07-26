
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
        self.encuestados = {}  # id -> Encuestado
        self.promedio_opinion = 0.0
        self.promedio_experticia = 0.0
        self.mediana = 0.0
        self.moda = 0
        self.extremismo = 0.0
        self.consenso = 0.0

    def agregar_encuestado(self, encuestado):
        self.encuestados[encuestado.id] = encuestado

    def calcular_promedios(self):
        datos = list(self.encuestados.values())
        n = len(datos)
        if n == 0:
            return
        self.promedio_opinion = sum(e.opinion for e in datos) / n
        self.promedio_experticia = sum(e.experticia for e in datos) / n

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
        datos = list(self.encuestados.values())
        n = len(datos)
        if n == 0:
            return
        opiniones = [e.opinion for e in datos]
        opiniones = self.ordenar_opiniones(opiniones[:])

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
        self.preguntas = {}  # id_pregunta -> Pregunta
        self.promedio_general_opinion = 0.0
        self.promedio_general_experticia = 0.0
        self.total_encuestados = 0

    def agregar_pregunta(self, pregunta):
        self.preguntas[pregunta.id_pregunta] = pregunta

    def calcular_estadisticas(self):
        preguntas = list(self.preguntas.values())
        if not preguntas:
            return
        self.promedio_general_opinion = sum(p.promedio_opinion for p in preguntas) / len(preguntas)
        self.promedio_general_experticia = sum(p.promedio_experticia for p in preguntas) / len(preguntas)
        self.total_encuestados = sum(len(p.encuestados) for p in preguntas)


class Encuesta:
    def __init__(self):
        self.temas = {}  # nombre -> Tema
        self.encuestados = {}  # id -> Encuestado

    def agregar_encuestado(self, encuestado):
        self.encuestados[encuestado.id] = encuestado

    def agregar_tema(self, tema):
        self.temas[tema.nombre] = tema


# ---------------------- Funciones Auxiliares ----------------------

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


# ---------------------- Entrada / Salida ----------------------

def leer_entrada_desde_archivo(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read().strip()
    secciones = contenido.split("\n\n")
    encuesta = Encuesta()

    for linea in secciones[0].splitlines():
        partes = linea.strip().split()
        id = int(partes[0])
        nombre = " ".join(partes[1:-2])
        experticia = int(partes[-2])
        opinion = int(partes[-1])
        encuesta.agregar_encuestado(Encuestado(id, nombre, experticia, opinion))

    for i, bloque in enumerate(secciones[1:]):
        tema = Tema(f"Tema {i + 1}")
        for linea in bloque.strip().splitlines():
            partes = linea.strip().split()
            id_pregunta = partes[0]
            ids = list(map(int, partes[1:]))
            pregunta = Pregunta(id_pregunta)
            for pid in ids:
                e = encuesta.encuestados.get(pid)
                if e:
                    pregunta.agregar_encuestado(e)
            pregunta.calcular_promedios()
            pregunta.calcular_estadisticas()
            tema.agregar_pregunta(pregunta)
        tema.calcular_estadisticas()
        encuesta.agregar_tema(tema)
    return encuesta


def guardar_salida_en_archivo(encuesta, archivo_salida):
    temas = list(encuesta.temas.values())
    insertion_sort(temas, lambda t: (-t.promedio_general_opinion, -t.promedio_general_experticia, -t.total_encuestados))

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write("Resultados de la encuesta:\n\n")
        for tema in temas:
            f.write(f"[{tema.promedio_general_opinion:.2f}] {tema.nombre}:\n")
            preguntas = list(tema.preguntas.values())
            insertion_sort(preguntas, lambda p: (-p.promedio_opinion, -p.promedio_experticia, -len(p.encuestados), id_pregunta_a_tupla(p.id_pregunta)))
            for p in preguntas:
                enc = list(p.encuestados.values())
                insertion_sort(enc, lambda e: (-e.opinion, -e.experticia, e.id))
                f.write(f" [{p.promedio_opinion:.2f}] Pregunta {p.id_pregunta}: ({', '.join(str(e.id) for e in enc)})\n")
            f.write("\n")

        f.write("Lista de encuestados:\n")
        enc = list(encuesta.encuestados.values())
        insertion_sort(enc, lambda e: (-e.experticia, -e.id))
        for e in enc:
            f.write(f"{e}\n")
        f.write("\n")


        preguntas = [p for t in temas for p in t.preguntas.values()]

        max_prom = max(preguntas, key=lambda p: (p.promedio_opinion, -id_pregunta_a_tupla(p.id_pregunta)[0], -id_pregunta_a_tupla(p.id_pregunta)[1]))
        min_prom = min(preguntas, key=lambda p: (p.promedio_opinion, id_pregunta_a_tupla(p.id_pregunta)))
        max_exp = max(preguntas, key=lambda p: (p.promedio_experticia, -id_pregunta_a_tupla(p.id_pregunta)[0], -id_pregunta_a_tupla(p.id_pregunta)[1]))
        min_exp = min(preguntas, key=lambda p: (p.promedio_experticia, id_pregunta_a_tupla(p.id_pregunta)))
        max_med = max(preguntas, key=lambda p: (p.mediana, -id_pregunta_a_tupla(p.id_pregunta)[0]))
        min_med = min(preguntas, key=lambda p: (p.mediana, id_pregunta_a_tupla(p.id_pregunta)))
        max_mod = max(preguntas, key=lambda p: (p.moda, -id_pregunta_a_tupla(p.id_pregunta)[0]))
        min_mod = min(preguntas, key=lambda p: (p.moda, id_pregunta_a_tupla(p.id_pregunta)))
        max_ext = max(preguntas, key=lambda p: (p.extremismo, -id_pregunta_a_tupla(p.id_pregunta)[0]))
        max_con = max(preguntas, key=lambda p: (p.consenso, -p.moda, id_pregunta_a_tupla(p.id_pregunta)))

        f.write("Resultados:\n")
        f.write(f"  Pregunta con mayor promedio de opinion: [{max_prom.promedio_opinion:.2f}] Pregunta: {max_prom.id_pregunta}\n")
        f.write(f"  Pregunta con menor promedio de opinion: [{min_prom.promedio_opinion:.2f}] Pregunta: {min_prom.id_pregunta}\n")
        f.write(f"  Pregunta con mayor promedio de experticia: [{max_exp.promedio_experticia:.2f}] Pregunta: {max_exp.id_pregunta}\n")
        f.write(f"  Pregunta con menor promedio de experticia: [{min_exp.promedio_experticia:.2f}] Pregunta: {min_exp.id_pregunta}\n")
        f.write(f"  Pregunta con mayor mediana de opinion: [{int(max_med.mediana)}] Pregunta: {max_med.id_pregunta}\n")
        f.write(f"  Pregunta con menor mediana de opinion: [{int(min_med.mediana)}] Pregunta: {min_med.id_pregunta}\n")
        f.write(f"  Pregunta con mayor moda de opinion: [{max_mod.moda}] Pregunta: {max_mod.id_pregunta}\n")
        f.write(f"  Pregunta con menor moda de opinion: [{min_mod.moda}] Pregunta: {min_mod.id_pregunta}\n")
        f.write(f"  Pregunta con mayor extremismo: [{max_ext.extremismo:.2f}] Pregunta: {max_ext.id_pregunta}\n")
        f.write(f"  Pregunta con mayor consenso: [{max_con.consenso:.2f}] Pregunta: {max_con.id_pregunta}\n")


# ---------------------- Main ----------------------

if __name__ == "__main__":
    archivo_entrada = "Test4.txt"
    archivo_salida = "Salida_Test4.txt"
    encuesta = leer_entrada_desde_archivo(archivo_entrada)
    guardar_salida_en_archivo(encuesta, archivo_salida)
    print(f"Análisis guardado en {archivo_salida}")