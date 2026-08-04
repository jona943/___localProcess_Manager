// config.js — Esquemas y constantes de configuración del Dashboard UI

export const DEVELOPER_FIELDS_SCHEMA = {
  "Nombre del Programador": { free: true, placeholder: "[Coloca aquí tu nombre completo o usuario]" },
  "Nombre del Agente": { free: true, placeholder: "[Coloca aquí el nombre personalizado para tu Agente de IA]" },
  "Personalidad/Tono": {
    options: [
      "Profesional, didáctico y directo",
      "Español latino formal y estructurado",
      "Mentor técnico formal y estructurado",
      "Conciso, al grano y pragmático",
      "Didáctico y explicativo paso a paso"
    ]
  },
  "Idioma Principal": {
    options: [
      "Español",
      "Inglés",
      "Portugués",
      "Francés",
      "Alemán"
    ]
  },
  "Terminología Técnica": {
    options: [
      "1. Totalmente traducido al español",
      "2. Español con términos básicos en inglés",
      "3. Spanglish técnico estándar",
      "4. Términos técnicos en inglés con sintaxis nativa",
      "5. 100% Inglés técnico puro"
    ]
  },
  "Nivel de Didáctica": {
    options: [
      "1. Máximo / Didáctico (Explicar paso a paso)",
      "2. Alto (Explicar conceptos principales)",
      "3. Medio (Resúmenes breves y fragmentos directos)",
      "4. Avanzado (Respuestas concisas, explicar solo lo mínimo)",
      "5. Experto / Nulo (Sin explicaciones, solo código)"
    ]
  },
  "Comentarios en Código": {
    options: [
      "Instructivo y sencillo",
      "Solo lo necesario",
      "Sin comentarios"
    ]
  },
  "Frecuencia de Feedback": {
    options: [
      "Frecuente",
      "Ocasional",
      "Ninguno"
    ]
  }
};

export const PROJECT_FIELDS_SCHEMA = {
  "Nombre del Proyecto": { free: true, placeholder: "[Coloca aquí el nombre de tu proyecto]" },
  "Directorio del Proyecto": { free: true, placeholder: "[Ruta del proyecto, ej: ./ o ../MiProyecto]" },
  "Archivo de Contexto": { free: true, placeholder: "[Nombre del archivo técnico de contexto, ej: README.md]" },
  "Tecnologías Principales": {
    options: [
      "Node.js, JavaScript, HTML5",
      "Python 3, Fast-API / Flask",
      "React, TypeScript, TailwindCSS",
      "Next.js, React, Node.js",
      "Go (Golang), gRPC, Docker",
      "Java, Spring Boot",
      "C# (.NET Core)",
      "PHP, Laravel"
    ]
  },
  "Módulos": {
    options: [
      "ES Modules (import / export)",
      "CommonJS (require)",
      "Módulos Estándar de Python",
      "Go Modules",
      "Cargo / Rust Crates"
    ]
  },
  "Estilos (CSS)": {
    options: [
      "Vanilla CSS (Mover inline a externos)",
      "TailwindCSS (Clases de utilidad)",
      "Sass / SCSS",
      "CSS Modules",
      "Styled Components",
      "Bootstrap"
    ]
  },
  "Manejo de Asincronía": {
    options: [
      "Asíncrono puro (async/await, Promesas)",
      "Asyncio / Native SQLite",
      "Callbacks / Event Loop tradicional",
      "RxJS / Observables",
      "Multiprocesamiento / Threads"
    ]
  },
  "Arquitectura de Código": {
    options: [
      "Modular src/ (routes, controllers, services)",
      "Dual-Drive (SQLite + MCP + UI)",
      "Modelo-Vista-Controlador (MVC)",
      "Arquitectura Hexagonal / Clean Architecture",
      "Microservicios Decoplados"
    ]
  }
};
