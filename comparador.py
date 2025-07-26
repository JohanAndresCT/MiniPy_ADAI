# comparador.py
import matplotlib.pyplot as plt
import time
import pandas as pd
import seaborn as sns
from a import medir_tiempo_insertion_sort as medir_a
from b import insertion_sort as insertion_sort_b

# ---------------------- Comparación Teórica vs Real: a.py ----------------------
def medir_tiempo_a():
    tamanos = [100, 200, 400, 800, 1600]
    tiempos_reales = []
    from a import insertion_sort as insertion_sort_a

    for n in tamanos:
        lista = [i for i in range(n, 0, -1)]
        start = time.time()
        insertion_sort_a(lista, key_fn=lambda x: x)
        end = time.time()
        duracion = end - start
        tiempos_reales.append(duracion)
        print(f"[a.py] Tamaño: {n}, Tiempo real: {duracion:.6f} s")

    # Calibrar constante c con el primer punto real
    c = tiempos_reales[0] / (tamanos[0] ** 2)
    tiempos_teoricos = [c * (n**2) for n in tamanos]

    # Gráfico a.py vs teoría calibrada
    plt.figure(figsize=(10, 5))
    plt.plot(tamanos, tiempos_reales, marker='o', label="a.py - Tiempo real", color='blue')
    plt.plot(tamanos, tiempos_teoricos, marker='x', linestyle='--', label=f"Teoría O(n²), c={c:.1e}", color='red')
    plt.xlabel("Tamaño de entrada (n)")
    plt.ylabel("Tiempo (s)")
    plt.title("a.py: Insertion Sort vs Teoría O(n²) calibrada")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("a_vs_teoria.png")
    plt.show()

    # Tabla de comparación como imagen
    df = pd.DataFrame({
        "Tamaño (n)": tamanos,
        "Tiempo real (s)": tiempos_reales,
        "Teórico O(n²) calibrado (s)": tiempos_teoricos
    })
    plt.figure(figsize=(8, 2.5))
    sns.set(font_scale=1.0)
    sns.set_style("white")
    tabla = plt.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)
    plt.axis('off')
    plt.title("Tiempos reales vs Teóricos calibrados (a.py)", fontsize=12)
    plt.tight_layout()
    plt.savefig("tabla_tiempos_a_vs_teoria.png")
    plt.show()

# ---------------------- Comparación Teórica vs Real: b.py ----------------------
def medir_tiempo_b():
    tamanos = [100, 200, 400, 800, 1600]
    tiempos_reales = []

    for n in tamanos:
        lista = [i for i in range(n, 0, -1)]
        start = time.time()
        insertion_sort_b(lista, key_fn=lambda x: x)
        end = time.time()
        duracion = end - start
        tiempos_reales.append(duracion)
        print(f"[b.py] Tamaño: {n}, Tiempo real: {duracion:.6f} s")

    # Calibrar constante c con el primer punto real
    c = tiempos_reales[0] / (tamanos[0] ** 2)
    tiempos_teoricos = [c * (n**2) for n in tamanos]

    # Gráfico b.py vs teoría calibrada
    plt.figure(figsize=(10, 5))
    plt.plot(tamanos, tiempos_reales, marker='o', label="b.py - Tiempo real", color='green')
    plt.plot(tamanos, tiempos_teoricos, marker='x', linestyle='--', label=f"Teoría O(n²), c={c:.1e}", color='red')
    plt.xlabel("Tamaño de entrada (n)")
    plt.ylabel("Tiempo (s)")
    plt.title("b.py: Insertion Sort vs Teoría O(n²) calibrada")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("b_vs_teoria.png")
    plt.show()

    # Tabla de comparación como imagen
    df = pd.DataFrame({
        "Tamaño (n)": tamanos,
        "Tiempo real (s)": tiempos_reales,
        "Teórico O(n²) calibrado (s)": tiempos_teoricos
    })
    plt.figure(figsize=(8, 2.5))
    sns.set(font_scale=1.0)
    sns.set_style("white")
    tabla = plt.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)
    plt.axis('off')
    plt.title("Tiempos reales vs Teóricos calibrados (b.py)", fontsize=12)
    plt.tight_layout()
    plt.savefig("tabla_tiempos_b_vs_teoria.png")
    plt.show()

# ---------------------- Comparación de ambos ----------------------
def comparar_insertion_sorts():
    print("\n--- Comparación Algoritmo A vs B (insertion sort) ---")
    print("Ejecutando a.py...")
    medir_tiempo_a()
    print("Ejecutando b.py...")
    medir_tiempo_b()

if __name__ == "__main__":
    comparar_insertion_sorts()
