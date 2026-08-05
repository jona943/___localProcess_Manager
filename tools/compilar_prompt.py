#!/usr/bin/env python3
"""
compilar_prompt.py — Compilador del Prompt de Sistema para localProcess_Manager
Lee la configuración directamente desde la base de datos relacional SQLite (memory.db) para generar prompt.md
"""

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
BASE_DIR = TOOLS_DIR.parent
PROMPT_OUTPUT_PATH = BASE_DIR / "prompt.md"

sys.path.append(str(TOOLS_DIR))
import memory_engine


def compilar(project_name: str = "default"):
    print(f"--- Iniciando Compilación del Prompt (Proyecto: {project_name}) ---")

    # Obtener configuración directa desde SQLite (memory.db)
    dev_config = memory_engine.get_all_config("developer_config")
    project_config = memory_engine.get_all_config("project_config", project_name=project_name)

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
        "Tecnologías Principales", "Python 3, SQLite, MCP, RAG Híbrido"
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
        "Arquitectura de Código", "Zero-Clutter RAG Híbrido (SQLite + FTS5 + MCP + UI)"
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
2.  **Base de Datos & RAG Neuronal (SQLite `memory.db`):**
    *   Tus memorias, preferencias del programador `{dev_name}`, reglas clave y bitácora residen en `memory.db`.
    *   Consultas y guardas memorias mediante el Servidor MCP (`consultar_memoria_neuronal`, `guardar_memoria_neuronal`) con Búsqueda Híbrida RAG (FTS5 + Vectores).
3.  **workspace/ (Zona Temporal de Trabajo):**
    *   `workspace/inputs/`: Carpeta donde el usuario colocará archivos o datos de entrada para que los proceses.
    *   `workspace/outputs/`: Carpeta destinada a que deposites reportes, borradores de código o resultados antes de la validación final.
4.  **tools/ (Capacidades, Dashboard UI y MCP):**
    *   `tools/server.py`: Servidor HTTP Local y Dashboard UI.
    *   `tools/neural_brain/mcp_brain_server.py`: Servidor MCP JSON-RPC 2.0.
    *   `tools/compilar_prompt.py`: Compilador del Prompt en Python.

---

## 🧠 GESTIÓN DE MEMORIAS Y BITÁCORA (SERVIDORES MCP & RAG HÍBRIDO)
Como agente de IA, utilizas el protocolo MCP y el motor RAG Híbrido:
- **Antes de responder a consultas complejas:** Invoca `consultar_memoria_neuronal` para recuperar en sub-milisegundos las reglas clave y el contexto histórico.
- **Si el usuario te enseña una nueva regla o corrección:** Invoca `guardar_memoria_neuronal` para persistir el aprendizaje en SQLite y FTS5 de forma permanente.

## IMPORTANTE
COMO AGENTE ES IMPORTANTE QUE RESPETES LA REGLA DE ORO Y CONSULTES TU MEMORIA NEURONAL EN CADA SESIÓN.
"""

    PROMPT_OUTPUT_PATH.write_text(system_prompt_template, encoding="utf-8")
    print(f"¡Éxito! prompt.md ha sido generado y guardado en: {PROMPT_OUTPUT_PATH}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compilador de Prompt de Sistema por Proyecto (LocalProcess_Manager)")
    parser.add_argument("--project", "-p", default=None, help="Nombre explícito del proyecto en SQLite")
    parser.add_argument("--folder", "-f", default=None, help="Ruta o nombre de la carpeta actual")
    args = parser.parse_args()

    identificador = args.project or args.folder or "default"
    proyecto_resuelto = memory_engine.resolve_project_name(identificador)
    compilar(project_name=proyecto_resuelto)


