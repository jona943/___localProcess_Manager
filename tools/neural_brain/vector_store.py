#!/usr/bin/env python3
"""
vector_store.py — Almacenamiento Vectorial e Índice Neuronal de Búsqueda Híbrida (FTS5 + Vector Embeddings)
Maneja la indexación, persistencia, FTS5 y recuperación híbrida por RRF en SQLite.
"""

import json
import sqlite3
import time
from pathlib import Path
from typing import List, Dict, Any
from encoder import NeuralEncoder

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "memory.db"


class NeuralVectorStore:
    """Motor de Almacenamiento e Índice Vectorial Neuronal Híbrido (FTS5 + Dense Vectors)."""

    def __init__(self, db_path: Path = DB_PATH, vector_dim: int = 384):
        self.db_path = db_path
        self.encoder = NeuralEncoder(vector_dim=vector_dim)
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Inicializa la tabla de vectores neuronales y la tabla FTS5 con Triggers de sincronización."""
        with self.get_connection() as conn:
            # 1. Tabla Principal
            conn.execute("""
                CREATE TABLE IF NOT EXISTS neural_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    vector TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 2. Tabla Virtual FTS5 para Búsqueda Léxica por Palabras Clave
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS neural_memory_fts USING fts5(
                    content,
                    metadata,
                    content='neural_memory',
                    content_rowid='id'
                )
            """)

            # 3. Triggers de Sincronización Automática entre neural_memory y neural_memory_fts
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS neural_memory_ai AFTER INSERT ON neural_memory BEGIN
                    INSERT INTO neural_memory_fts(rowid, content, metadata)
                    VALUES (new.id, new.content, new.metadata);
                END;
            """)

            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS neural_memory_ad AFTER DELETE ON neural_memory BEGIN
                    INSERT INTO neural_memory_fts(neural_memory_fts, rowid, content, metadata)
                    VALUES('delete', old.id, old.content, old.metadata);
                END;
            """)

            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS neural_memory_au AFTER UPDATE ON neural_memory BEGIN
                    INSERT INTO neural_memory_fts(neural_memory_fts, rowid, content, metadata)
                    VALUES('delete', old.id, old.content, old.metadata);
                    INSERT INTO neural_memory_fts(rowid, content, metadata)
                    VALUES (new.id, new.content, new.metadata);
                END;
            """)

            conn.commit()

    def add_memory(self, content: str, metadata: Dict[str, Any] = None) -> int:
        """Vectoriza un contenido y lo almacena en el índice neuronal y FTS5."""
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

    def search_fts(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Búsqueda Léxica por Palabras Clave usando FTS5 (BM25)."""
        results = []
        clean_query = ' OR '.join([f'"{w}"' for w in query.replace('"', '').split() if w.strip()])
        if not clean_query:
            clean_query = query

        with self.get_connection() as conn:
            try:
                rows = conn.execute("""
                    SELECT rowid as id, content, metadata, rank
                    FROM neural_memory_fts
                    WHERE neural_memory_fts MATCH ?
                    ORDER BY rank ASC
                    LIMIT ?
                """, (clean_query, top_k)).fetchall()

                for row in rows:
                    results.append({
                        "id": row["id"],
                        "content": row["content"],
                        "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                        "fts_rank": row["rank"]
                    })
            except sqlite3.OperationalError:
                pass

        return results

    def search_similar(self, query: str, top_k: int = 5, threshold: float = 0.1) -> List[Dict[str, Any]]:
        """Búsqueda Neuronal Semántica basada exclusivamente en Vectores y Similitud del Coseno."""
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
                        "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                        "similarity": round(similarity, 4),
                        "created_at": row["created_at"]
                    })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        top_results = results[:top_k]
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        for res in top_results:
            res["search_latency_ms"] = round(elapsed_ms, 3)

        return top_results

    def search_hybrid(self, query: str, top_k: int = 3, alpha: float = 0.5, rrf_k: int = 60) -> List[Dict[str, Any]]:
        """
        Búsqueda Híbrida RAG: Combina FTS5 (BM25) y Similitud Vectorial usando RRF (Reciprocal Rank Fusion).
        - alpha: Peso asignado a la relevancia vectorial (0.0 a 1.0).
        - rrf_k: Constante suavizadora de RRF (estándar AWS/Elasticsearch = 60).
        """
        start_time = time.perf_counter()

        # 1. Recuperar candidatos vectoriales y FTS5
        vec_results = self.search_similar(query, top_k=20, threshold=-1.0)
        fts_results = self.search_fts(query, top_k=20)

        # 2. Mapear rankings
        doc_scores = {}
        doc_details = {}

        # Procesar posiciones vectoriales
        for rank, doc in enumerate(vec_results, 1):
            doc_id = doc["id"]
            doc_details[doc_id] = doc
            rrf_vec_score = alpha * (1.0 / (rrf_k + rank))
            doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + rrf_vec_score

        # Procesar posiciones FTS5
        for rank, doc in enumerate(fts_results, 1):
            doc_id = doc["id"]
            if doc_id not in doc_details:
                with self.get_connection() as conn:
                    row = conn.execute("SELECT id, content, metadata, created_at FROM neural_memory WHERE id=?", (doc_id,)).fetchone()
                    if row:
                        doc_details[doc_id] = {
                            "id": row["id"],
                            "content": row["content"],
                            "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                            "similarity": 0.0,
                            "created_at": row["created_at"]
                        }

            rrf_fts_score = (1.0 - alpha) * (1.0 / (rrf_k + rank))
            doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + rrf_fts_score

        # 3. Construir lista final ordenada por puntaje RRF
        hybrid_results = []
        for doc_id, score in sorted(doc_scores.items(), key=lambda x: x[1], reverse=True):
            item = doc_details[doc_id].copy()
            item["rrf_score"] = round(score, 6)
            hybrid_results.append(item)

        top_results = hybrid_results[:top_k]
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        for res in top_results:
            res["search_latency_ms"] = round(elapsed_ms, 3)

        return top_results

    def clear_memory(self):
        """Limpia el índice vectorial y el índice FTS5."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM neural_memory")
            try:
                conn.execute("DELETE FROM neural_memory_fts")
            except sqlite3.OperationalError:
                pass
            conn.commit()


if __name__ == "__main__":
    store = NeuralVectorStore()
    store.clear_memory()

    # Indexación de prueba
    store.add_memory("Implementación de Servidor Web HTTP local en Python tools/server.py", {"modulo": "fase2"})
    store.add_memory("Configuración de base de datos SQLite memory.db con motor Dual-Drive", {"modulo": "fase1"})
    store.add_memory("Estilos Vanilla CSS Dark Mode con arquitectura de variables IDE", {"modulo": "ui"})
    store.add_memory("Servidor MCP JSON-RPC 2.0 en Python tools/neural_brain/mcp_brain_server.py", {"modulo": "fase3"})

    # Búsqueda Híbrida de prueba
    query = "servidor mcp json-rpc"
    print(f"\n🔍 Consulta Híbrida: '{query}'")
    matches = store.search_hybrid(query, top_k=2)
    for idx, match in enumerate(matches, 1):
        print(f"[{idx}] Puntaje RRF: {match['rrf_score']} | Latencia: {match['search_latency_ms']} ms")
        print(f"    Contenido: {match['content']}\n")

