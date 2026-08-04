# <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="35" height="35" valign="middle" /> localProcess_Manager — Arquitectura Didáctica para Agentes de IA en CLI

[![Runtime - Python](https://img.shields.io/badge/Runtime-Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Format - Markdown & JSON](https://img.shields.io/badge/Format-Markdown_%26_JSON-000000?style=for-the-badge&logo=markdown&logoColor=white)](#)
[![Category - AI CLI & Workflow](https://img.shields.io/badge/Category-AI_CLI_%26_Workflow-0052CC?style=for-the-badge&logo=gnu-bash&logoColor=white)](#)
[![License - MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=open-source-initiative&logoColor=white)](#)

**localProcess_Manager** es un entorno modular y estructurado diseñado para estandarizar y optimizar el flujo de trabajo colaborativo entre desarrolladores de software y agentes de Inteligencia Artificial (IA) en entornos de línea de comandos (CLI) y terminales.

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/chrome/chrome-original.svg" width="22" height="22" valign="middle" /> Propósito del Repositorio

Proporcionar una arquitectura estandarizada que permita a cualquier desarrollador interactuar con asistentes de IA de manera predecible, ordenada y eficiente, manteniendo un control absoluto sobre la base de código y maximizando la ventana de contexto disponible para el modelo.

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/vscode/vscode-original.svg" width="22" height="22" valign="middle" /> Problemas que Resuelve

1. **Pérdida de Contexto**: Aislando los archivos temporales de entrada y salida (`workspace/`), evitando que la terminal acumule registros innecesarios.
2. **Configuración Desacoplada**: Separa las preferencias personales del programador (tono, didáctica, idioma) de los estándares técnicos del proyecto (stack, frameworks, CSS).
3. **Persistencia de Memoria**: Un módulo dedicado (`ai-memory/`) permite al agente recordar de forma indefinida las correcciones hechas por el desarrollador y las lecciones aprendidas entre sesiones.
4. **Modificación Didáctica Supervisada**: Reglas strictly supervisadas para que la IA actúe como tutor y no altere archivos directamente sin aprobación previa del usuario.

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" width="22" height="22" valign="middle" /> Estructura del Repositorio

```text
localProcess_Manager/
├── README.md                     # Guía de uso y documentación principal
├── LICENSE                       # Licencia MIT de código abierto en español
├── control_checkpoints.md        # Registro y control del estado del entorno
├── prompt.md                     # System Prompt compilado inyectable a la IA
├── user-config/                  # Configuración modular desacoplada
│   ├── 1.developer-config.md     # Ajustes del desarrollador (Tono, idioma, didáctica)
│   └── 2.project-config.md       # Estándares técnicos del proyecto (Stack, directorios, CSS)
├── ai-memory/                    # Memoria persistente del agente
│   ├── perfil_usuario.md         # Preferencias y perfil del programador
│   ├── aprendizajes_clave.md     # Lecciones aprendidas y reglas a recordar
│   └── bitacora_tareas.md        # Historial de tareas completadas
├── workspace/                    # Espacio operativo temporal
│   ├── inputs/                   # Fragmentos de código, archivos o documentación para la IA
│   └── outputs/                  # Borradores o reportes que genera la IA antes de aplicarlos
└── tools/                        # Compilador y herramientas Python
    ├── esquema_funciones.json    # Esquema JSON de herramientas (Function Calling)
    ├── requirements.txt          # Dependencias de Python
    └── compilar_prompt.py        # Script Python para compilar prompt.md
```

---

## <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bash/bash-original.svg" width="22" height="22" valign="middle" /> Flujo de Uso e Inicialización

### 1. Inicialización Guiada (Un Solo Uso)
Puedes automatizar tu configuración inicial copiando el contenido de [`___ignore-prompt.md`](./___ignore-prompt.md) y pegándolo en tu primer chat con el agente de IA para responder un cuestionario interactivo que generará tus archivos en `user-config/` y `ai-memory/`.

### 2. Configuración Manual y Compilación
Edita tus preferencias en [`user-config/1.developer-config.md`](./user-config/1.developer-config.md) y [`user-config/2.project-config.md`](./user-config/2.project-config.md). Luego compila el prompt ejecutando:

```bash
python3 tools/compilar_prompt.py
```

### 3. Ejecución en CLI
Usa el archivo compilado [`prompt.md`](./prompt.md) con tu cliente de IA CLI preferido:

* **Antigravity CLI**:
  ```bash
  agy chat --system prompt.md --file [contexto].md
  ```
* **Gemini CLI**:
  ```bash
  gemini-cli --system prompt.md --context [contexto].md
  ```

---

<p align="center">
  <sub>localProcess_Manager — AI CLI Architecture & Workflow 2026</sub>
</p>
