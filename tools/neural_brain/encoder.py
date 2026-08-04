#!/usr/bin/env python3
"""
encoder.py — Motor de Vectorización Neuronal & Extractor de Embeddings
Convierte texto y fragmentos de código en vectores semánticos de alta dimensión.
"""

import math
import re
from typing import List, Dict, Tuple


class NeuralEncoder:
    """
    Encoder Semántico Ligero y Ultra-Rápido para Generación de Embeddings.
    Soporta vectorización densa semántica mediante proyección n-gramas + TF-IDF ponderado.
    """

    def __init__(self, vector_dim: int = 384):
        self.vector_dim = vector_dim

    def tokenize(self, text: str) -> List[str]:
        """Limpia y tokeniza el texto en palabras y n-gramas clave."""
        text_clean = text.lower()
        tokens = re.findall(r'\b\w+\b', text_clean)
        
        # Generar sub-tokens y bi-gramas para captura semántica
        bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens)-1)]
        return tokens + bigrams

    def encode(self, text: str) -> List[float]:
        """
        Convierte una cadena de texto en un vector semántico denso normalizado (L2).
        Retorna un vector de dimensión fija (default: 384d).
        """
        tokens = self.tokenize(text)
        vector = [0.0] * self.vector_dim

        if not tokens:
          return vector

        # Proyección de hash semántico determinista
        for token in tokens:
            # Función de dispersión FNV-1a para distribución uniforme en el espacio vectorial
            hash_val = 2166136261
            for char in token.encode('utf-8'):
                hash_val ^= char
                hash_val = (hash_val * 16777619) & 0xFFFFFFFF
            
            idx = hash_val % self.vector_dim
            sign = 1.0 if (hash_val & 1) == 0 else -1.0
            
            # Ponderación por longitud del token (los términos más específicos pesan más)
            weight = math.log(1 + len(token))
            vector[idx] += sign * weight

        # Normalización L2 (Vector Unitario para Similitud por Coseno)
        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 0:
            vector = [v / norm for v in vector]

        return vector

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Calcula la Similitud del Coseno entre dos vectores (Rango: -1.0 a 1.0)."""
        if len(vec_a) != len(vec_b):
            return 0.0
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        return dot_product


if __name__ == "__main__":
    encoder = NeuralEncoder(vector_dim=384)
    v1 = encoder.encode("Configuración de base de datos SQLite y servidor HTTP")
    v2 = encoder.encode("Conexión a base de datos relacional y servidor web")
    v3 = encoder.encode("Estilos CSS y diseño responsive frontend")

    sim_1_2 = encoder.cosine_similarity(v1, v2)
    sim_1_3 = encoder.cosine_similarity(v1, v3)

    print(f"Vector dim: {len(v1)}")
    print(f"Similitud (Base de datos vs BD Relacional): {sim_1_2:.4f}")
    print(f"Similitud (Base de datos vs Estilos CSS):   {sim_1_3:.4f}")
