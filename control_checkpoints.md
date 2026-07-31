# Control de Checkpoints: Estructura Estándar para Agentes de IA en CLI (localProcess_Manager)

Este documento sirve para realizar el seguimiento del proceso de estandarización del repositorio `localProcess_Manager` para su uso optimizado con agentes de IA en Terminal (Antigravity, Gemini, Claude, etc.).

## Checkpoints

- [x] **1. Analizar y Diseñar la Arquitectura Estándar**
  - [x] Revisar el contexto del proyecto y el prompt existente.
  - [x] Definir los campos y formatos de los archivos en `ai-memory/`.
  - [x] Determinar la interacción entre el espacio de trabajo (`workspace/`) y la IA.

- [x] **2. Crear la Estructura de Directorios**
  - [x] Crear la carpeta `ai-memory/` (ya existe, pero asegurar su estado).
  - [x] Crear la carpeta `workspace/inputs/`.
  - [x] Crear la carpeta `workspace/outputs/`.
  - [x] Crear la carpeta `tools/`.

- [x] **3. Inicializar los Archivos de Memoria (`ai-memory/`)**
  - [x] Crear `ai-memory/perfil_usuario.md` con las preferencias actuales identificadas (por ejemplo, el tono sinaloense y estilo didáctico).
  - [x] Crear `ai-memory/aprendizajes_clave.md` para albergar correcciones a perpetuidad.
  - [x] Crear `ai-memory/bitacora_tareas.md` con el log de la tarea actual.

- [x] **4. Actualizar y Refinar `prompt.md`**
  - [x] Mantener la personalidad (acento sinaloense, didáctico).
  - [x] Actualizar las instrucciones de memoria para usar los archivos específicos en vez de archivos fechados sueltos.
  - [x] Describir el uso de `workspace/inputs/` y `workspace/outputs/`.
  - [x] Describir el uso de `tools/` y la lectura de `LocalDrop-Contexto.md`.

- [x] **5. Definir la Plantilla/Ejemplo de Herramientas (`tools/esquema_funciones.json`)**
  - [x] Crear un esquema de ejemplo para el Function Calling o capacidades locales.

- [x] **6. Crear Guía de Uso del Repositorio (`README.md`)**
  - [x] Explicar cómo inicializar cualquier agente de IA CLI con esta estructura.

- [x] **7. Verificación Final**
  - [x] Revisar que todo el repositorio cumpla con la estructura propuesta y las reglas de diseño.

## ⚙️ Componente de Configuración Personalizada (`user-config/`)

- [x] **8. Crear Plantillas de Configuración**
  - [x] Rellenar `user-config/1.developer-config.md` con la tabla de preferencias del desarrollador (usuario).
  - [x] Rellenar `user-config/2.project-config.md` con la tabla de requisitos y metadatos del proyecto.

- [x] **9. Desarrollar el Compilador del Prompt (`tools/compilar_prompt.py`)**
  - [x] Desarrollar un script en Python 3 que lea y parsee las tablas de configuración.
  - [x] Generar un archivo `prompt.md` personalizado a partir de las configuraciones y una plantilla base.

- [x] **10. Probar el Generador**
  - [x] Ejecutar el script `python3 tools/compilar_prompt.py` y comprobar que `prompt.md` se actualice correctamente con las preferencias.
