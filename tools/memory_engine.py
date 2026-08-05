#!/usr/bin/env python3
"""
memory_engine.py — Motor de Memoria SQLite Dual-Drive con Soporte Multi-Proyecto
Maneja la base de datos binaria memory.db y exporta a archivos .md para vista humana.
"""

import sqlite3
import datetime
from pathlib import Path
from typing import List, Dict, Any

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

        # Verificación y migración para bases de datos existentes
        cursor.execute("PRAGMA table_info(project_config)")
        cols_proj = [c[1] for c in cursor.fetchall()]
        if cols_proj and "project_name" not in cols_proj:
            cursor.execute("DROP TABLE IF EXISTS project_config")
            cursor.execute("DROP TABLE IF EXISTS learnings")
            cursor.execute("DROP TABLE IF EXISTS task_logs")

        # 1. Registro de Proyectos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                name TEXT PRIMARY KEY,
                path TEXT NOT NULL,
                context_file TEXT DEFAULT 'README.md',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Configuración del Desarrollador (Global)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS developer_config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)

        # 3. Configuración del Proyecto (Multiproyecto)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_config (
                project_name TEXT NOT NULL DEFAULT 'default',
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                PRIMARY KEY (project_name, key)
            )
        """)

        # 4. Aprendizajes Clave (Memoria Semántica por Proyecto + Global)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL DEFAULT 'global',
                category TEXT NOT NULL,
                topic TEXT NOT NULL,
                rule TEXT NOT NULL,
                importance INTEGER DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)

        # 5. Bitácora de Tareas (Memoria Episódica por Proyecto)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL DEFAULT 'default',
                task_summary TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.commit()


# ==========================================
# GESTIÓN DE PROYECTOS
# ==========================================

def get_projects() -> List[Dict[str, Any]]:
    """Obtiene la lista de todos los proyectos registrados."""
    init_db()
    with get_connection() as conn:
        rows = conn.execute("SELECT name, path, context_file, created_at FROM projects ORDER BY name ASC").fetchall()
        return [dict(row) for row in rows]


def add_project(name: str, path: str = "./", context_file: str = "README.md") -> bool:
    """Registra un nuevo proyecto en la base de datos."""
    init_db()
    if not name:
        return False
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO projects (name, path, context_file) VALUES (?, ?, ?) "
            "ON CONFLICT(name) DO UPDATE SET path=excluded.path, context_file=excluded.context_file",
            (name, path, context_file)
        )
        conn.commit()
    
    # Inicializar configuración por defecto para el proyecto si está vacía
    defaults_proj = {
        "Nombre del Proyecto": name,
        "Directorio del Proyecto": path,
        "Archivo de Contexto": context_file,
        "Tecnologías Principales": "Python 3, SQLite, MCP",
        "Módulos": "Python standard library",
        "Estilos (CSS)": "Vanilla CSS (Dark Mode IDE)",
        "Manejo de Asincronía": "Asyncio / Native SQLite",
        "Arquitectura de Código": "Dual-Drive (SQLite + MCP + UI)"
    }
    for k, v in defaults_proj.items():
        set_config("project_config", k, v, project_name=name)
        
    return True


def delete_project(name: str) -> bool:
    """Elimina un proyecto y todas sus configuraciones, aprendizajes y logs asociados."""
    with get_connection() as conn:
        conn.execute("DELETE FROM projects WHERE name=?", (name,))
        conn.execute("DELETE FROM project_config WHERE project_name=?", (name,))
        conn.execute("DELETE FROM task_logs WHERE project_name=?", (name,))
        conn.execute("DELETE FROM learnings WHERE project_name=?", (name,))
        conn.commit()
    return True


# ==========================================
# FUNCIONES CONFIG (DEVELOPER & PROJECT)
# ==========================================

def set_config(table_name: str, key: str, value: str, project_name: str = "default"):
    """Guarda o actualiza un valor de configuración."""
    init_db()
    if table_name not in ("developer_config", "project_config"):
        raise ValueError("Nombre de tabla no válido.")

    with get_connection() as conn:
        cursor = conn.cursor()
        if table_name == "developer_config":
            cursor.execute(
                "INSERT INTO developer_config (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, value)
            )
        else:
            cursor.execute(
                "INSERT INTO project_config (project_name, key, value) VALUES (?, ?, ?) "
                "ON CONFLICT(project_name, key) DO UPDATE SET value=excluded.value",
                (project_name, key, value)
            )
        conn.commit()


def get_all_config(table_name: str, project_name: str = "default") -> dict:
    """Obtiene toda la configuración como un diccionario."""
    init_db()
    if table_name not in ("developer_config", "project_config"):
        raise ValueError("Nombre de tabla no válido.")

    with get_connection() as conn:
        cursor = conn.cursor()
        if table_name == "developer_config":
            rows = cursor.execute("SELECT key, value FROM developer_config").fetchall()
        else:
            rows = cursor.execute("SELECT key, value FROM project_config WHERE project_name=?", (project_name,)).fetchall()
            if not rows and project_name != "default":
                # Fallback al proyecto por defecto si no existe configuración específica
                rows = cursor.execute("SELECT key, value FROM project_config WHERE project_name='default'").fetchall()
        return {row["key"]: row["value"] for row in rows}


# ==========================================
# APRENDIZAJES & BITÁCORA MULTIPROYECTO
# ==========================================

def add_learning(category: str, topic: str, rule: str, importance: int = 1, project_name: str = "global"):
    """Registra un nuevo aprendizaje o regla clave asignado a un proyecto o global."""
    init_db()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO learnings (category, topic, rule, importance, created_at, project_name) VALUES (?, ?, ?, ?, ?, ?)",
            (category, topic, rule, importance, now, project_name)
        )
        conn.commit()


def get_learnings(category: str = None, project_name: str = "default") -> list:
    """Recupera los aprendizajes guardados para el proyecto específico más los globales."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM learnings WHERE (project_name=? OR project_name='global')"
        params = [project_name]
        
        if category:
            query += " AND category=?"
            params.append(category)
            
        query += " ORDER BY id ASC"
        rows = cursor.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def delete_learning(learning_id: int):
    """Elimina un aprendizaje o regla clave por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM learnings WHERE id=?", (learning_id,))
        conn.commit()


def add_task_log(task_summary: str, project_name: str = "default"):
    """Registra una entrada en la bitácora de tareas para un proyecto específico."""
    init_db()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO task_logs (task_summary, created_at, project_name) VALUES (?, ?, ?)",
            (task_summary, now, project_name)
        )
        conn.commit()


def delete_task_log(task_id: int):
    """Elimina una entrada de la bitácora de tareas por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM task_logs WHERE id=?", (task_id,))
        conn.commit()


def get_task_logs(project_name: str = "default") -> list:
    """Recupera el historial de la bitácora de tareas del proyecto activo."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM task_logs WHERE project_name=? ORDER BY id DESC", (project_name,)).fetchall()
        return [dict(row) for row in rows]


# ==========================================
# SINCRONIZADOR DUAL (SQLite ➔ Markdown)
# ==========================================

def export_to_markdown(project_name: str = "default"):
    """Genera/Sincroniza la vista Markdown para humanos desde SQLite."""
    init_db()
    
    # 1. Exportar Developer Config
    dev_data = get_all_config("developer_config")
    dev_md_content = "# 👤 Configuración del Desarrollador (Vista Humana)\n\n"
    dev_md_content += "| Propiedad | Valor |\n| :--- | :--- |\n"
    for k, v in dev_data.items():
        dev_md_content += f"| **{k}** | {v} |\n"
    DEV_CONFIG_MD.parent.mkdir(parents=True, exist_ok=True)
    DEV_CONFIG_MD.write_text(dev_md_content, encoding="utf-8")

    # 2. Exportar Project Config
    proj_data = get_all_config("project_config", project_name=project_name)
    proj_md_content = "# 🛠️ Configuración del Proyecto (Vista Humana)\n\n"
    proj_md_content += "| Propiedad | Valor |\n| :--- | :--- |\n"
    for k, v in proj_data.items():
        proj_md_content += f"| **{k}** | {v} |\n"
    PROJECT_CONFIG_MD.parent.mkdir(parents=True, exist_ok=True)
    PROJECT_CONFIG_MD.write_text(proj_md_content, encoding="utf-8")

    # 3. Exportar Aprendizajes Clave
    learnings = get_learnings(project_name=project_name)
    learn_md_content = "# 🧠 Aprendizajes Clave y Reglas Persistentes\n\n"
    if learnings:
        for item in learnings:
            learn_md_content += f"### [{item['category'].upper()}] {item['topic']} (Proyecto: {item.get('project_name', 'global')})\n"
            learn_md_content += f"- **Regla**: {item['rule']}\n"
            learn_md_content += f"- *Registrado*: `{item['created_at']}` | Relevancia: {item['importance']}\n\n"
    else:
        learn_md_content += "_No hay aprendizajes registrados aún._\n"
    LEARNINGS_MD.parent.mkdir(parents=True, exist_ok=True)
    LEARNINGS_MD.write_text(learn_md_content, encoding="utf-8")

    # 4. Exportar Bitácora de Tareas
    tasks = get_task_logs(project_name=project_name)
    tasks_md_content = "# 📝 Bitácora de Tareas y Logs de Interacción\n\n"
    if tasks:
        for t in tasks:
            tasks_md_content += f"- **[{t['created_at']}]**: {t['task_summary']}\n"
    else:
        tasks_md_content += "_No hay tareas registradas en la bitácora._\n"
    TASKS_MD.parent.mkdir(parents=True, exist_ok=True)
    TASKS_MD.write_text(tasks_md_content, encoding="utf-8")


def parse_markdown_file(file_path: Path) -> dict:
    """Lee y parsea tablas de propiedades en formato Markdown."""
    if not file_path.exists():
        return {}
    content = file_path.read_text(encoding="utf-8")
    config = {}
    for line in content.splitlines():
        trimmed = line.strip()
        if trimmed.startswith("|") and trimmed.endswith("|"):
            raw_cells = trimmed.split("|")
            cells = [c.strip() for c in raw_cells[1:-1]]
            if len(cells) < 2:
                continue
            prop_name = cells[0].lower()
            if "propiedad" in prop_name or "---" in prop_name:
                continue
            key = cells[0].replace("**", "").strip()
            value = cells[1].strip()
            if key and value:
                config[key] = value
    return config


def seed_initial_data():
    """Siembra datos iniciales importando archivos Markdown si existen."""
    init_db()

    # Asegurar proyectos por defecto
    projects = get_projects()
    if not projects:
        add_project("default", "./", "README.md")
        add_project("localProcess_Manager", "./", "README.md")

    # 1. Importar primero desde Markdown si existen valores
    dev_from_md = parse_markdown_file(DEV_CONFIG_MD)
    for k, v in dev_from_md.items():
        if k and v:
            set_config("developer_config", k, v)

    proj_from_md = parse_markdown_file(PROJECT_CONFIG_MD)
    for k, v in proj_from_md.items():
        if k and v:
            set_config("project_config", k, v, project_name="localProcess_Manager")

    # 2. Rellenar con defaults solo lo que falte
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
    current_dev = get_all_config("developer_config")
    for k, v in defaults_dev.items():
        if k not in current_dev:
            set_config("developer_config", k, v)

    export_to_markdown()


if __name__ == "__main__":
    print("--- Inicializando Base de Datos memory.db y Sincronizador Dual (Multi-Proyecto) ---")
    seed_initial_data()
    print("¡Base de datos memory.db creada y sincronizada!")
