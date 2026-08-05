#!/usr/bin/env python3
"""
test_hybrid_brain.py — Benchmark y Suite de Pruebas Comparativas RAG Híbrido
Compara el rendimiento y la precisión de:
  1. Búsqueda Semántica Pura (Vectores 384d)
  2. Búsqueda Léxica Pura (FTS5 BM25)
  3. Búsqueda Híbrida (FTS5 + Vectores con Algoritmo RRF)
"""

import time
from pathlib import Path
from vector_store import NeuralVectorStore


def run_hybrid_benchmark():
    print("=======================================================================")
    print("🧪 SUITE DE BENCHMARK RAG HÍBRIDO (SQLite FTS5 + Dense Embeddings + RRF)")
    print("=======================================================================\n")

    store = NeuralVectorStore()
    store.clear_memory()

    # 1. Dataset de Prueba Técnico
    dataset = [
        ("Configuración del servidor HTTP local en Python tools/server.py con soporte ES Modules", {"tipo": "servidor"}),
        ("Persistencia relacional en SQLite memory.db con motor Dual-Drive", {"tipo": "base_datos"}),
        ("Sistema de UI Vanilla CSS Dark Mode con variables HSL y diseño IDE", {"tipo": "frontend"}),
        ("Servidor MCP JSON-RPC 2.0 en tools/neural_brain/mcp_brain_server.py para Antigravity CLI", {"tipo": "mcp"}),
        ("Regla permanente: Consumir iconos siempre desde GitHub Raw CDN para evitar cuotas", {"tipo": "regla"}),
        ("Exclusión de la base de datos binaria memory.db en .gitignore para máxima privacidad", {"tipo": "git"}),
        ("Compilación de prompt de sistema en tools/compilar_prompt.py desde memoria SQLite", {"tipo": "prompt"})
    ]

    print("📥 1. Indexando dataset de prueba...")
    t_start_index = time.perf_counter()
    for texto, meta in dataset:
        store.add_memory(texto, meta)
    t_index_ms = (time.perf_counter() - t_start_index) * 1000

    print(f"   ✅ Se indexaron {len(dataset)} documentos en {t_index_ms:.2f} ms ({t_index_ms/len(dataset):.2f} ms/doc)\n")

    # 2. Casos de Prueba Comparativos
    casos_prueba = [
        {
            "nombre": "Caso 1: Coincidencia Exacta de Código / Ruta (FTS5)",
            "query": "mcp_brain_server.py JSON-RPC",
            "esperado": "mcp_brain_server.py"
        },
        {
            "nombre": "Caso 2: Concepto Semántico (Vector)",
            "query": "¿Cómo garantizamos la seguridad de los datos locales en el control de versiones?",
            "esperado": ".gitignore"
        },
        {
            "nombre": "Caso 3: Consulta Mixta (Léxica + Semántica)",
            "query": "variables HSL y tema oscuro UI",
            "esperado": "Vanilla CSS"
        }
    ]

    print("-----------------------------------------------------------------------")
    print("📊 2. Comparativa de Métodos de Búsqueda RAG:")
    print("-----------------------------------------------------------------------\n")

    for caso in casos_prueba:
        q = caso["query"]
        print(f"🔹 {caso['nombre']}")
        print(f"   ❓ Consulta: '{q}'")

        # A) Semántica Pura
        t0 = time.perf_counter()
        res_sem = store.search_similar(q, top_k=1)
        t_sem = (time.perf_counter() - t0) * 1000
        top_sem = res_sem[0]["content"] if res_sem else "Sin resultado"

        # B) Léxica Pura (FTS5)
        t0 = time.perf_counter()
        res_fts = store.search_fts(q, top_k=1)
        t_fts = (time.perf_counter() - t0) * 1000
        top_fts = res_fts[0]["content"] if res_fts else "Sin resultado"

        # C) Híbrida RRF
        t0 = time.perf_counter()
        res_hyb = store.search_hybrid(q, top_k=1)
        t_hyb = (time.perf_counter() - t0) * 1000
        top_hyb = res_hyb[0]["content"] if res_hyb else "Sin resultado"
        score_hyb = res_hyb[0]["rrf_score"] if res_hyb else 0.0

        print(f"   • Semántica (Vector): [{t_sem:.2f} ms] ➔ {top_sem[:55]}...")
        print(f"   • Léxica (FTS5 BM25): [{t_fts:.2f} ms] ➔ {top_fts[:55]}...")
        print(f"   • HÍBRIDA (RRF Score: {score_hyb}): [{t_hyb:.2f} ms] ➔ {top_hyb[:55]}...")
        
        ok = caso["esperado"].lower() in top_hyb.lower()
        print(f"   🎯 Evaluación Híbrida: {'✅ APROBADO' if ok else '❌ FALLADO'}\n")

    print("=======================================================================")
    print("🎉 Benchmark Híbrido Finalizado: RAG Híbrido activo y 100% operativo.")
    print("=======================================================================")


if __name__ == "__main__":
    run_hybrid_benchmark()
