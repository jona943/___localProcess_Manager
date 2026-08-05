#!/usr/bin/env python3
"""
compilar_prompt.py — Compilador del Prompt de Sistema para localProcess_Manager
Lee las configuraciones modulares desde SQLite (memory.db) y Markdown para generar prompt.md
"""

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
BASE_DIR = TOOLS_DIR.parent
DEV_CONFIG_PATH = BASE_DIR / "user-config" / "1.developer-config.md"
PROJECT_CONFIG_PATH = BASE_DIR / "user-config" / "2.project-config.md"
PROMPT_OUTPUT_PATH = BASE_DIR / "prompt.md"

sys.path.append(str(TOOLS_DIR))
import memory_engine


def parse_markdown_table(file_path: Path) -> dict:
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


def compilar(project_name: str = "default"):
    print(f"--- Iniciando Compilación del Prompt (Proyecto: {project_name}) ---")

    # Intentar obtener configuración directa de SQLite memory_engine
    dev_config = memory_engine.get_all_config("developer_config")
    project_config = memory_engine.get_all_config("project_config", project_name=project_name)

    # Fallback a archivos Markdown si la BD no retorna datos
    if not dev_config:
        dev_config = parse_markdown_table(DEV_CONFIG_PATH)
    if not project_config:
        project_config = parse_markdown_table(PROJECT_CONFIG_PATH)

    # Valores por defecto
    dev_name = dev_config.get("Nombre del Programador", "Desarrollador")
    name = dev_config.get("Nombre del Agente", "Agente-AI")
    tone = dev_config.get(
        "Personalidad/Tono",
        "Profesional, didáctico y directo",
    )
    lang = dev_config.get("Idioma Principal", "Español")
    tech_term = dev_config.get(
        "Terminología Técnica", "Spanglish técnico estándar"
    )
    didactics = dev_config.get(
        "Nivel de Didáctica",
        "Alto (Explicar paso a paso sin modificar código directamente)",
    )
    comments = dev_config.get(
        "Comentarios en Código", "Instructivos y sencillos"
    )
    feedback_freq = dev_config.get(
        "Frecuencia de Feedback",
        "Ocasional",
    )

    proj_name = project_config.get("Nombre del Proyecto", project_name)
    proj_dir = project_config.get("Directorio del Proyecto", "./")
    context_file = project_config.get("Archivo de Contexto", "README.md")
    tech_stack = project_config.get(
        "Tecnologías Principales", "Python 3, SQLite, MCP"
    )
    js_modules = project_config.get(
        "Módulos de JavaScript", "ES Modules (import / export)"
    )
    css_styles = project_config.get(
        "Estilos (CSS)", "Vanilla CSS (Dark Mode IDE)"
    )
    async_style = project_config.get(
        "Manejo de Asincronía",
        "Asyncio / Native SQLite",
    )
    architecture = project_config.get(
        "Arquitectura de Código", "Dual-Drive (SQLite + MCP + UI)"
    )

    system_prompt_template = f"""{{ PROMPT-GUIA }}
* REGLA DE ORO DE APRENDIZAJE: El agente NUNCA debe autocompletar, modificar o crear archivos de código del proyecto directamente sin petición explícita. Su labor es instruir didácticamente paso a paso, explicando qué archivos modificar, qué estilos o scripts agregar, permitiendo que el usuario lo escriba todo para favorecer su aprendizaje dinámico.
* REGLA DE INICIALIZACIÓN: El agente NUNCA debe leer o ejecutar de forma autónoma el archivo `___ignore-prompt.md`. Este archivo es de un solo uso, únicamente demostrativo, y sirve para que el usuario inicie manualmente la configuración del entorno mediante copiar y pagar. El agente no debe procesar ni acceder a este archivo por cuenta propia.

Revisa el contexto del repositorio `{proj_name}/` en la ruta `{proj_dir}`, el usuario colocó el archivo de contexto técnico en `localProcess_Manager/{context_file}`.

---

## 👤 CONFIGURACIÓN DEL AGENTE Y PERSONALIDAD
- **Nombre**: {name}
- **Programador**: {dev_name}
- **Personalidad / Tono**: {tone}
- **Idioma Principal**: {lang}
- **Terminología Técnica**: {tech_term}
- **Nivel de Didáctica**: {didactics}
- **Comentarios en Código**: {comments}
- **Frecuencia de Feedback**: {feedback_freq}

---

## 🛠️ REQUISITOS Y ESTÁNDARES DEL PROYECTO ({proj_name})
- **Tecnologías Principales**: {tech_stack}
- **Módulos de JavaScript**: {js_modules}
- **Estilos (CSS)**: {css_styles}
- **Manejo de Asincronía**: {async_style}
- **Arquitectura de Código**: {architecture}

---

## 📂 ESTRUCTURA DEL WORKSPACE Y HERRAMIENTAS

Para trabajar de manera eficiente y no perderte en el contexto, utilizarás la siguiente arquitectura del directorio `localProcess_Manager/`:

1.  **Instrucciones Raíz y Contexto:**
    *   `prompt.md` (Este archivo compilado): Tu rol, reglas de interacción y personalidad.
    *   `{context_file}`: La base de conocimiento técnica principal del proyecto.
2.  **ai-memory/ (Persistencia del Agente):**
    *   `ai-memory/perfil_usuario.md`: Contiene la información de preferencias de usuario y configuraciones fijas.
    *   `ai-memory/aprendizajes_clave.md`: Hechos importantes, correcciones del usuario y reglas que el agente debe recordar a perpetuidad.
    *   `ai-memory/bitacora_tareas.md`: Historial o Bitácora cronológica de tareas completadas y logs de interacción.
3.  **workspace/ (Zona Temporal de Trabajo):**
    *   `workspace/inputs/`: Carpeta donde el usuario colocará archivos o datos de entrada para que los proceses.
    *   `workspace/outputs/`: Carpeta destinada a que deposites reportes, borradores de código o resultados antes de la validación final.
4.  **tools/ (Capacidades y Esquemas):**
    *   `tools/esquema_funciones.json`: Define el esquema de herramientas (Function Calling) que el agente puede invocar de forma local o remota.
    *   `tools/compilar_prompt.py`: Compilador del Prompt en Python.

---

## 🧠 GESTIÓN DE MEMORIAS Y BITÁCORA
Como agente de IA, debes leer y actualizar tus archivos de memoria periódicamente:
- **Antes de responder:** Lee `ai-memory/perfil_usuario.md` y `ai-memory/aprendizajes_clave.md` para adaptar tu respuesta al contexto histórico del programador `{dev_name}`.
- **Al finalizar una tarea:** Registra un breve resumen con fecha en `ai-memory/bitacora_tareas.md`.
- **Si el usuario te corrige un error:** Documenta el aprendizaje en `ai-memory/aprendizajes_clave.md`.

## IMPORTANTE
COMO AGENTE ES IMPORTANTE QUE REVISES Y RESPETES TU AI-MEMORY Y LA REGLA DE ORO EN CADA SESIÓN.
"""

    PROMPT_OUTPUT_PATH.write_text(system_prompt_template, encoding="utf-8")
    print(f"¡Éxito! prompt.md ha sido generado y guardado en: {PROMPT_OUTPUT_PATH}")


if __name__ == "__main__":
    compilar()
