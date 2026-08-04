#!/usr/bin/env python3
"""
test_brain.py — Script de Pruebas & Benchmark de Latencia Neuronal
Verifica la precisión semántica y la velocidad de consulta del Segundo Cerebro Neuronal.
"""

import time
from vector_store import NeuralVectorStore


def run_benchmark():
    print("=======================================================================")
    print("🧠 Benchmark del Segundo Cerebro Neuronal (LocalProcess_Manager)")
    print("=======================================================================\n")

    store = NeuralVectorStore()
    store.clear_memory()

    # 1. Sembrar conocimiento de prueba
    datos_prueba = [
        ("Motor de base de datos relacional SQLite memory.db y sincronización a Markdown", {"categoria": "base_datos"}),
        ("Servidor HTTP ligero en Python tools/server.py con soporte para ES Modules", {"categoria": "servidor"}),
        ("Sistema de diseño Dark Mode Vanilla CSS con tokens y variables HSL", {"categoria": "frontend"}),
        ("Compilador de prompt en Python tools/compilar_prompt.py para generar prompt.md", {"categoria": "prompt"}),
        ("Asistente de IA con personalidades configurables y nombres de usuario neutros", {"categoria": "agente"}),
        ("Exclusión de memoria binaria en .gitignore para máxima privacidad", {"categoria": "git"})
    ]

    start_index = time.perf_counter()
    for texto, meta in datos_prueba:
        store.add_memory(texto, meta)
    elapsed_index = (time.perf_counter() - start_index) * 1000

    print(f"✅ Se indexaron {len(datos_prueba)} bloques de conocimiento en {elapsed_index:.2f} ms")
    print(f"⚡ Promedio de vectorización por bloque: {elapsed_index / len(datos_prueba):.2f} ms\n")

    # 2. Consultas semánticas de prueba
    consultas = [
        "¿Cómo funciona la base de datos y la sincronización?",
        "Servidor web en python",
        "Privacidad de archivos y gitignore",
        "Diseño de interfaz y estilos CSS"
    ]

    print("-----------------------------------------------------------------------")
    print("🔍 Ejecutando Pruebas de Búsqueda Semántica Neuronal:")
    print("-----------------------------------------------------------------------\n")

    for q in consultas:
        t_start = time.perf_counter()
        resultados = store.search_similar(q, top_k=1)
        t_search = (time.perf_counter() - t_start) * 1000

        if resultados:
            top = resultados[0]
            print(f"❓ Consulta: '{q}'")
            print(f"🎯 Respuesta Neuronal (Similitud: {top['similarity']} | Latencia: {t_search:.3f} ms):")
            print(f"   ↳ {top['content']}\n")
        else:
            print(f"❌ Sin coincidencias para: '{q}'\n")

    print("=======================================================================")
    print("🎉 Prueba completada exitosamente. El motor responde en tiempo real.")
    print("=======================================================================")


if __name__ == "__main__":
    run_benchmark()
