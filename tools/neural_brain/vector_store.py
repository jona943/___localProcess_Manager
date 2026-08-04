#!/usr/bin/env python3
"""
vector_store.py — Almacenamiento Vectorial e Índice Neuronal de Búsqueda
Maneja la indexación, persistencia y recuperación por similitud semántica en SQLite.
"""

import json
import sqlite3
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple
from encoder import NeuralEncoder

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "memory.db"


class NeuralVectorStore:
    """Motor de Almacenamiento e Índice Vectorial Neuronal."""

    def __init__(self, db_path: Path = DB_PATH, vector_dim: int = 384):
        self.db_path = db_path
        self.encoder = NeuralEncoder(vector_dim=vector_dim)
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Inicializa la tabla de vectores neuronales si no existe."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS neural_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    vector TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def add_memory(self, content: str, metadata: Dict[str, Any] = None) -> int:
        """Vectoriza un contenido y lo almacena en el índice neuronal."""
        vector = self.encoder.encode(content)
        vector_json = json.dumps(vector)
        metadata_json = json.dumps(metadata or {})

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO neural_memory (content, metadata, vector) VALUES (?, ?, ?)",
                (content, metadata_json, vector_json)
            )
            conn.commit()
            return cursor.lastrowid

    def search_similar(self, query: str, top_k: int = 3, threshold: float = 0.1) -> List[Dict[str, Any]]:
        """
        Búsqueda Neuronal Semántica: Convierte la consulta a vector y calcula
        la similitud del coseno contra todos los vectores almacenados.
        """
        start_time = time.perf_counter()
        query_vec = self.encoder.encode(query)

        results = []
        with self.get_connection() as conn:
            rows = conn.execute("SELECT id, content, metadata, vector, created_at FROM neural_memory").fetchall()
            
            for row in rows:
                doc_vec = json.loads(row["vector"])
                similarity = self.encoder.cosine_similarity(query_vec, doc_vec)
                
                if similarity >= threshold:
                    results.append({
                        "id": row["id"],
                        "content": row["content"],
                        "metadata": json.loads(row["metadata"]),
                        "similarity": round(similarity, 4),
                        "created_at": row["created_at"]
                    })

        # Ordenar por mayor similitud semántica
        results.sort(key=lambda x: x["similarity"], reverse=True)
        top_results = results[:top_k]
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        for res in top_results:
            res["search_latency_ms"] = round(elapsed_ms, 3)

        return top_results

    def clear_memory(self):
        """Limpia el índice vectorial."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM neural_memory")
            conn.commit()


if __name__ == "__main__":
    store = NeuralVectorStore()
    store.clear_memory()

    # Indexación de prueba
    store.add_memory("Implementación de Servidor Web HTTP local en Python tools/server.py", {"modulo": "fase2"})
    store.add_memory("Configuración de base de datos SQLite memory.db con motor Dual-Drive", {"modulo": "fase1"})
    store.add_memory("Estilos Vanilla CSS Dark Mode con arquitectura de variables IDE", {"modulo": "ui"})

    # Búsqueda semántica de prueba
    query = "base de datos relacional sqlite"
    print(f"\n🔍 Consulta: '{query}'")
    matches = store.search_similar(query, top_k=2)
    for idx, match in enumerate(matches, 1):
        print(f"[{idx}] Similitud: {match['similarity']} | Latencia: {match['search_latency_ms']} ms")
        print(f"    Contenido: {match['content']}\n")
