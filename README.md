# <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="35" height="35" valign="middle" /> localProcess_Manager — Arquitectura Didáctica y Segundo Cerebro Neuronal para Agentes de IA en CLI

[![Runtime - Python](https://img.shields.io/badge/Runtime-Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Database - SQLite Dual Drive](https://img.shields.io/badge/Database-SQLite_Dual_Drive-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](#)
[![Protocol - MCP Server](https://img.shields.io/badge/Protocol-MCP_Stdio_JSON--RPC-4A154B?style=for-the-badge&logo=json&logoColor=white)](#)
[![Frontend - ES Modules Vanilla](https://img.shields.io/badge/Frontend-ES_Modules_Vanilla-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](#)
[![Status - In Development & Ideation](https://img.shields.io/badge/Status-Ideation_%26_Experimental-orange?style=for-the-badge&logo=git&logoColor=white)](#)
[![License - MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=open-source-initiative&logoColor=white)](#)

> [!NOTE]
> **Proyecto en Fase de Ideación y Pruebas Activas**: Este entorno se encuentra en proceso de desarrollo experimental continuo. Las arquitecturas Dual-Drive, el servidor MCP y los módulos del Segundo Cerebro Neuronal se están refinando activamente a través de iteraciones de prueba.

**localProcess_Manager** es un entorno modular de arquitectura avanzada diseñado para estandarizar la colaboración entre desarrolladores de software y agentes de Inteligencia Artificial (IA) en terminales y línea de comandos (CLI). Incorpora una arquitectura **Dual-Drive (SQLite + Markdown)**, un **Dashboard de Configuración Web Local** y un **Segundo Cerebro Neuronal (Neural Memory Engine — NME)** expuesto vía protocolo **MCP (Model Context Protocol)**.

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/chrome/chrome-original.svg" width="22" height="22" valign="middle" /> Propósito del Repositorio

Proporcionar un entorno estandarizado que permita interactuar con asistentes de IA en CLI de manera predecible, ultrarrápida y privada, eliminando el desperdicio de tokens en prompts estáticos gigantescos mediante búsquedas semánticas neuronales de sub-milisegundo.

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/vscode/vscode-original.svg" width="22" height="22" valign="middle" /> Componentes Principales de la Arquitectura

1. **Segundo Cerebro Neuronal (NME)**: Extractor de embeddings densos en 384 dimensiones (`encoder.py`) y motor de almacenamiento e índice semántico vectorial en SQLite (`vector_store.py`) con tiempos de respuesta en ~1.1 ms.
2. **Servidor MCP Protocol (Model Context Protocol)**: Conector nativo `stdio` JSON-RPC 2.0 (`mcp_brain_server.py`) que permite a Antigravity CLI, Claude Code y clientes de terminal consultar e inyectarse memoria semántica automáticamente sin necesidad de cargar prompts manualmente.
3. **Servidor HTTP Local & Dashboard UI Modular**: Panel de control web local (`tools/server.py` y `tools/web/`) construido con ES Modules nativos y componentes desacoplados (`tools/web/js/componentes/`).
4. **Arquitectura Dual-Drive**: Persistencia primaria en base de datos binaria local privada `memory.db` con sincronización automática a vista humana en archivos Markdown (`user-config/` y `ai-memory/`).
5. **Privacidad Garantizada**: `memory.db` excluido de control de versiones vía `.gitignore` para mantener los datos de memoria 100% locales en la máquina del desarrollador.

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" width="22" height="22" valign="middle" /> Estructura del Repositorio

```text
localProcess_Manager/
├── README.md                     # Guía de uso y documentación principal
├── LICENSE                       # Licencia MIT de código abierto en español
├── control_checkpoints.md        # Registro y control del estado del entorno
├── prompt.md                     # System Prompt compilado inyectable a la IA
├── .gitignore                    # Exclusión de binario memory.db y cache de Python
├── user-config/                  # Configuración modular (Vista humana Markdown)
│   ├── 1.developer-config.md     # Ajustes del desarrollador (Tono, idioma, didáctica)
│   └── 2.project-config.md       # Estándares técnicos del proyecto (Stack, CSS)
├── ai-memory/                    # Memoria persistente del agente (Vista humana Markdown)
│   ├── perfil_usuario.md         # Preferencias y perfil del programador
│   ├── aprendizajes_clave.md     # Lecciones aprendidas y reglas a recordar
│   └── bitacora_tareas.md        # Historial de tareas completadas
├── workspace/                    # Espacio operativo temporal
│   ├── inputs/                   # Fragmentos de código o documentación para la IA
│   └── outputs/                  # Borradores o reportes que genera la IA
└── tools/                        # Herramientas, Servidor HTTP, MCP y Segundo Cerebro
    ├── compilar_prompt.py        # Compilador de prompt.md en Python
    ├── memory_engine.py          # Motor de persistencia SQLite Dual-Drive
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
    │           ├── aprendizajes.js
    │           ├── bitacoraTareas.js
    │           └── visorPrompt.js
    └── neural_brain/             # Segundo Cerebro Neuronal (Neural Memory Engine — NME)
        ├── encoder.py            # Motor de vectorización de 384d
        ├── vector_store.py       # Almacenamiento vectorial e índice de similitud del coseno
        ├── mcp_brain_server.py   # Servidor MCP stdio JSON-RPC 2.0 para Antigravity CLI
        └── test_mcp_client.py    # Simulador de pruebas para cliente MCP
```

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bash/bash-original.svg" width="22" height="22" valign="middle" /> Guía de Ejecución e Integración

### 1. Iniciar el Dashboard Web Local
Ejecuta el servidor de configuración local:

```bash
python3 tools/server.py
```
Abre en tu navegador `http://localhost:8000` para administrar configuraciones, aprendizajes clave y previsualizar el System Prompt compilado.

---

### 2. Registrar el Servidor MCP en Antigravity CLI
Para que Antigravity CLI consulte el Segundo Cerebro Neuronal de forma autónoma sin pasar ningún prompt en cada ejecución, registra el servidor MCP en tu archivo global `~/.gemini/antigravity.json` o local `.gemini/mcp.json`:

```json
{
  "mcpServers": {
    "segundo-cerebro-nme": {
      "command": "python3",
      "args": [
        "/ruta/absoluta/a/___localProcess_Manager/tools/neural_brain/mcp_brain_server.py"
      ]
    }
  }
}
```

---

### 3. Probar la Integración MCP
Puedes ejecutar la prueba de simulación de cliente MCP para verificar la latencia y la respuesta en tiempo real:

```bash
python3 tools/neural_brain/test_mcp_client.py
```

---

<p align="center">
  <sub>localProcess_Manager — AI CLI Architecture & Workflow 2026</sub>
</p>
