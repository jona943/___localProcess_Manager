#!/usr/bin/env python3
"""
memory_engine.py — Motor de Memoria SQLite & Sincronizador Dual
Maneja la base de datos binaria memory.db y exporta a archivos .md para vista humana.
"""

import sqlite3
import datetime
from pathlib import Path

# Directorios principales
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "memory.db"

DEV_CONFIG_MD = BASE_DIR / "user-config" / "1.developer-config.md"
PROJECT_CONFIG_MD = BASE_DIR / "user-config" / "2.project-config.md"
LEARNINGS_MD = BASE_DIR / "ai-memory" / "aprendizajes_clave.md"
TASKS_MD = BASE_DIR / "ai-memory" / "bitacora_tareas.md"


def get_connection():
    """Obtiene conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inicializa la estructura de tablas en memory.db si no existen."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Configuración del Desarrollador
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS developer_config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)

        # 2. Configuración del Proyecto
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)

        # 3. Aprendizajes Clave (Memoria Semántica)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                topic TEXT NOT NULL,
                rule TEXT NOT NULL,
                importance INTEGER DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)

        # 4. Bitácora de Tareas (Memoria Episódica)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_summary TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.commit()


# ==========================================
# FUNCIONES CRUD (CREATE, READ, UPDATE, DELETE)
# ==========================================

def set_config(table_name: str, key: str, value: str):
    """Guarda o actualiza un valor de configuración."""
    if table_name not in ("developer_config", "project_config"):
        raise ValueError("Nombre de tabla no válido.")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {table_name} (key, value) VALUES (?, ?) "
            f"ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value)
        )
        conn.commit()


def get_all_config(table_name: str) -> dict:
    """Obtiene toda la configuración como un diccionario."""
    if table_name not in ("developer_config", "project_config"):
        raise ValueError("Nombre de tabla no válido.")

    with get_connection() as conn:
        cursor = conn.cursor()
        rows = cursor.execute(f"SELECT key, value FROM {table_name}").fetchall()
        return {row["key"]: row["value"] for row in rows}


def add_learning(category: str, topic: str, rule: str, importance: int = 1):
    """Registra un nuevo aprendizaje o regla clave."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO learnings (category, topic, rule, importance, created_at) VALUES (?, ?, ?, ?, ?)",
            (category, topic, rule, importance, now)
        )
        conn.commit()


def get_learnings(category: str = None) -> list:
    """Recupera los aprendizajes guardados (filtrado opcional por categoría)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if category:
            rows = cursor.execute(
                "SELECT * FROM learnings WHERE category=? ORDER BY id ASC", (category,)
            ).fetchall()
        else:
            rows = cursor.execute("SELECT * FROM learnings ORDER BY id ASC").fetchall()
        return [dict(row) for row in rows]


def delete_learning(learning_id: int):
    """Elimina un aprendizaje o regla clave por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM learnings WHERE id=?", (learning_id,))
        conn.commit()


def add_task_log(task_summary: str):
    """Registra una entrada en la bitácora de tareas."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO task_logs (task_summary, created_at) VALUES (?, ?)",
            (task_summary, now)
        )
        conn.commit()


def delete_task_log(task_id: int):
    """Elimina una entrada de la bitácora de tareas por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM task_logs WHERE id=?", (task_id,))
        conn.commit()


def get_task_logs() -> list:
    """Recupera el historial de la bitácora de tareas."""
    with get_connection() as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM task_logs ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]


# ==========================================
# SINCRONIZADOR DUAL (SQLite ➔ Markdown)
# ==========================================

def export_to_markdown():
    """Genera/Sincroniza automáticamente la vista Markdown para humanos desde SQLite."""
    
    # 1. Exportar Developer Config
    dev_data = get_all_config("developer_config")
    dev_md_content = "# 👤 Configuración del Desarrollador (Vista Humana)\n\n"
    dev_md_content += "| Propiedad | Valor |\n| :--- | :--- |\n"
    for k, v in dev_data.items():
        dev_md_content += f"| **{k}** | {v} |\n"
    DEV_CONFIG_MD.parent.mkdir(parents=True, exist_ok=True)
    DEV_CONFIG_MD.write_text(dev_md_content, encoding="utf-8")

    # 2. Exportar Project Config
    proj_data = get_all_config("project_config")
    proj_md_content = "# 🛠️ Configuración del Proyecto (Vista Humana)\n\n"
    proj_md_content += "| Propiedad | Valor |\n| :--- | :--- |\n"
    for k, v in proj_data.items():
        proj_md_content += f"| **{k}** | {v} |\n"
    PROJECT_CONFIG_MD.parent.mkdir(parents=True, exist_ok=True)
    PROJECT_CONFIG_MD.write_text(proj_md_content, encoding="utf-8")

    # 3. Exportar Aprendizajes Clave
    learnings = get_learnings()
    learn_md_content = "# 🧠 Aprendizajes Clave y Reglas Persistentes\n\n"
    if learnings:
        for item in learnings:
            learn_md_content += f"### [{item['category'].upper()}] {item['topic']}\n"
            learn_md_content += f"- **Regla**: {item['rule']}\n"
            learn_md_content += f"- *Registrado*: `{item['created_at']}` | Relevancia: {item['importance']}\n\n"
    else:
        learn_md_content += "_No hay aprendizajes registrados aún._\n"
    LEARNINGS_MD.parent.mkdir(parents=True, exist_ok=True)
    LEARNINGS_MD.write_text(learn_md_content, encoding="utf-8")

    # 4. Exportar Bitácora de Tareas
    tasks = get_task_logs()
    tasks_md_content = "# 📝 Bitácora de Tareas y Logs de Interacción\n\n"
    if tasks:
        for t in tasks:
            tasks_md_content += f"- **[{t['created_at']}]**: {t['task_summary']}\n"
    else:
        tasks_md_content += "_No hay tareas registradas en la bitácora._\n"
    TASKS_MD.parent.mkdir(parents=True, exist_ok=True)
    TASKS_MD.write_text(tasks_md_content, encoding="utf-8")


def seed_initial_data():
    """Siembra datos iniciales de prueba si la base de datos está vacía."""
    init_db()

    # Si la tabla dev_config está vacía, sembrar con valores por defecto
    defaults_dev = {
        "Nombre del Programador": "Desarrollador",
        "Nombre del Agente": "Agente-AI",
        "Personalidad/Tono": "Profesional, didáctico y directo",
        "Idioma Principal": "Español",
        "Terminología Técnica": "3. Spanglish técnico estándar",
        "Nivel de Didáctica": "1. Máximo / Didáctico (Explicar paso a paso)",
        "Comentarios en Código": "Instructivo y sencillo",
        "Frecuencia de Feedback": "Ocasional"
    }
    for k, v in defaults_dev.items():
        set_config("developer_config", k, v)

    proj_config = get_all_config("project_config")
    if not proj_config:
        defaults_proj = {
            "Nombre del Proyecto": "localProcess_Manager",
            "Directorio del Proyecto": "./",
            "Archivo de Contexto": "README.md",
            "Tecnologías Principales": "Python 3, SQLite, MCP",
            "Módulos": "Python standard library & pydantic",
            "Estilos (CSS)": "Vanilla CSS (Dark Mode IDE)",
            "Manejo de Asincronía": "Asyncio / Native SQLite",
            "Arquitectura de Código": "Dual-Drive (SQLite + MCP + UI)"
        }
        for k, v in defaults_proj.items():
            set_config("project_config", k, v)

    learnings = get_learnings()
    if not learnings:
        add_learning(
            category="arquitectura",
            topic="Regla de Oro Didáctica",
            rule="El agente NUNCA debe modificar código directamente sin petición explícita del usuario.",
            importance=5
        )
        add_learning(
            category="estabilidad",
            topic="Uso de Devicon CDN",
            rule="Usar siempre raw.githubusercontent.com para logos Devicon SVG.",
            importance=4
        )

    tasks = get_task_logs()
    if not tasks:
        add_task_log("Inicialización de la arquitectura Dual-Drive con SQLite en Python.")

    # Exportar a Markdown inmediatamente
    export_to_markdown()


if __name__ == "__main__":
    print("--- Inicializando Base de Datos memory.db y Sincronizador Dual ---")
    seed_initial_data()
    print("¡Base de datos memory.db creada y sincronizada con los archivos Markdown!")
