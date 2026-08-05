# <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="35" height="35" valign="middle" /> localProcess_Manager — Arquitectura Didáctica y Segundo Cerebro Neuronal para Agentes de IA en CLI

[![Runtime - Python](https://img.shields.io/badge/Runtime-Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Database - SQLite RAG Hybrid](https://img.shields.io/badge/Database-SQLite_FTS5_%26_Vectores-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](#)
[![Protocol - MCP Server](https://img.shields.io/badge/Protocol-MCP_Stdio_JSON--RPC-4A154B?style=for-the-badge&logo=json&logoColor=white)](#)
[![Frontend - ES Modules Vanilla](https://img.shields.io/badge/Frontend-ES_Modules_Vanilla-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](#)
[![Status - In Development & Ideation](https://img.shields.io/badge/Status-Ideation_%26_Experimental-orange?style=for-the-badge&logo=git&logoColor=white)](#)
[![License - MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=open-source-initiative&logoColor=white)](#)

> [!NOTE]
> **Proyecto en Fase de Ideación y Pruebas Activas**: Este entorno se encuentra en proceso de desarrollo experimental continuo. Las arquitecturas Zero-Clutter, el motor RAG Híbrido (FTS5 + Vectores RRF), el servidor MCP y el instalador automático se están refinando activamente a través de iteraciones de prueba.

**localProcess_Manager** es un entorno modular de arquitectura avanzada diseñado para estandarizar la colaboración entre desarrolladores de software y agentes de Inteligencia Artificial (IA) en terminales y línea de comandos (CLI). Incorpora una arquitectura **Zero-Clutter RAG Híbrida (SQLite FTS5 + Vectores 384d)**, un **Dashboard de Configuración Web Local** y un **Segundo Cerebro Neuronal (Neural Memory Engine — NME)** expuesto vía el protocolo **MCP (Model Context Protocol)**.

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/chrome/chrome-original.svg" width="22" height="22" valign="middle" /> Propósito del Repositorio

Proporcionar un entorno estandarizado que permita interactuar con asistentes de IA en CLI de manera predecible, ultrarrápida y privada. Elimina la redundancia de archivos Markdown y el desperdicio de tokens mediante búsquedas léxicas y semánticas híbridas de sub-milisegundo (< 3 ms) respaldadas en SQLite.

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/vscode/vscode-original.svg" width="22" height="22" valign="middle" /> Componentes Principales de la Arquitectura

1. **Búsqueda RAG Híbrida (FTS5 + Vectores RRF)**:
   * **Búsqueda Léxica**: Coincidencia exacta de tokens de código y rutas vía SQLite **FTS5** (BM25).
   * **Búsqueda Semántica**: Extractor de embeddings densos de 384 dimensiones (`encoder.py`).
   * **Fusión RRF**: Algoritmo **Reciprocal Rank Fusion** (`vector_store.py`) que combina ambas búsquedas en sub-milisegundos con `TRIGGERS` de base de datos nativos.
2. **Servidor MCP Protocol (Model Context Protocol)**: Conector nativo `stdio` JSON-RPC 2.0 (`mcp_brain_server.py`) que expone las herramientas `consultar_memoria_neuronal`, `guardar_memoria_neuronal` y `limpiar_memoria_neuronal` para Antigravity CLI.
3. **Instalador Automático 1-Clic (`install.sh`)**: Script de configuración automatizada para Linux que registra el Servidor MCP en `settings.json` y configura la función inteligente `agy-ctx` en el entorno de terminal del usuario.
4. **Dashboard HTTP Local & UI Multi-Proyecto**: Panel de control web local (`tools/server.py` y `tools/web/`) construido con Vanilla CSS e ES Modules desacoplados para administrar, renombrar y eliminar proyectos en tiempo real.
5. **Arquitectura Zero-Clutter**: Persistencia primaria y única fuente de verdad en base de datos relacional binaria privada `memory.db`, ofreciendo reportes consolidados en Markdown bajo demanda vía `/api/export` sin generar archivos `.md` redundantes en disco.

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" width="22" height="22" valign="middle" /> Estructura del Repositorio

```text
localProcess_Manager/
├── README.md                     # Guía de uso y documentación principal
├── LICENSE                       # Licencia MIT de código abierto en español
├── install.sh                    # Instalador automático de la integración con Antigravity CLI
├── control_checkpoints.md        # Registro y control del estado del entorno
├── prompt.md                     # System Prompt compilado inyectable a la IA
├── .gitignore                    # Exclusión de binario memory.db y cache de Python
├── workspace/                    # Espacio operativo temporal
│   ├── inputs/                   # Fragmentos de código o documentación para la IA
│   └── outputs/                  # Borradores o reportes que genera la IA
└── tools/                        # Herramientas, Servidor HTTP, MCP y Segundo Cerebro
    ├── compilar_prompt.py        # Compilador de prompt.md con auto-resolución por carpeta
    ├── memory_engine.py          # Motor de persistencia SQLite y exportador a demanda
    ├── server.py                 # Servidor HTTP local y API del Dashboard Web
    ├── web/                      # Dashboard UI Web (Vanilla CSS + ES Modules)
    │   ├── index.html            # Punto de entrada HTML del Dashboard
    │   ├── style.css             # Sistema de diseño Dark Mode (IDE)
    │   └── js/                   # Javascript modular
    │       ├── app.js            # Punto de entrada e inicialización
    │       ├── config.js         # Esquemas y opciones de configuración
    │       ├── utils.js          # Funciones auxiliares y helpers
    │       └── componentes/      # Módulos de componentes en español
    │           ├── navegacion.js
    │           ├── configuracionDesarrollador.js
    │           ├── configuracionProyecto.js
    │           ├── selectorProyectos.js
    │           ├── aprendizajes.js
    │           ├── bitacoraTareas.js
    │           └── visorPrompt.js
    └── neural_brain/             # Segundo Cerebro Neuronal (RAG Híbrido + MCP)
        ├── encoder.py            # Motor de vectorización de 384d
        ├── vector_store.py       # Almacenamiento vectorial, índice FTS5 y fusión RRF
        ├── mcp_brain_server.py   # Servidor MCP stdio JSON-RPC 2.0 para Antigravity CLI
        ├── test_brain.py         # Benchmark de latenciaNeuronal
        ├── test_hybrid_brain.py  # Suite de pruebas comparativas RAG Híbrido
        └── test_mcp_client.py    # Simulador de pruebas para cliente MCP
```

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bash/bash-original.svg" width="22" height="22" valign="middle" /> Guía de Instalación y Uso Rápido (Linux)

### 1. Instalación en 1 Clic
Clona el repositorio y ejecuta el instalador automático:

```bash
git clone https://github.com/jona943/___localProcess_Manager.git
cd ___localProcess_Manager
./install.sh
source ~/.bashrc
```

---

### 2. Iniciar el Dashboard Web Local
Inicia el panel de control local:

```bash
python3 tools/server.py
```
Abre `http://localhost:8000` en tu navegador para administrar preferencias de desarrollador, registrar proyectos y generar prompts compilados.

---

### 3. Usar Antigravity CLI en Cualquier Proyecto (`agy-ctx`)
Navega a cualquier carpeta de tu equipo y ejecuta:

```bash
cd ~/Escritorio/MiProyecto
agy-ctx
```

Antigravity CLI detectará automáticamente tu proyecto en SQLite, cargará tus reglas técnicas e iniciará la sesión con el Servidor MCP RAG Híbrido conectado.

---

<p align="center">
  <sub>localProcess_Manager — AI CLI Architecture & Workflow 2026</sub>
</p>

