// componentes/navegacion.js — Navegación entre pestañas y actualización de encabezados

import { cargarVistaPreviaPrompt } from './visorPrompt.js';

export function inicializarNavegacion() {
  document.querySelectorAll('.nav-item').forEach(boton => {
    boton.addEventListener('click', () => {
      document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      boton.classList.add('active');
      const nombrePestana = boton.getAttribute('data-tab');
      const panelObjetivo = document.getElementById(`tab-${nombrePestana}`);
      if (panelObjetivo) panelObjetivo.classList.add('active');

      // Actualizar título y subtítulo del encabezado
      const titulos = {
        developer: ['Configuración del Desarrollador', 'Personalidad del agente, idioma y preferencias de didáctica'],
        project: ['Configuración del Proyecto', 'Estándares del proyecto, stack tecnológico y arquitectura'],
        learnings: ['Aprendizajes Clave & Reglas Persistentes', 'Memoria semántica registrada para evitar repetir errores'],
        tasks: ['Bitácora de Tareas & Interacciones', 'Historial cronológico de actividades completadas'],
        prompt: ['Visor de System Prompt (prompt.md)', 'Vista previa del prompt compilado inyectable a la IA']
      };

      if (titulos[nombrePestana]) {
        document.getElementById('page-title').innerText = titulos[nombrePestana][0];
        document.getElementById('page-subtitle').innerText = titulos[nombrePestana][1];
      }

      if (nombrePestana === 'prompt') cargarVistaPreviaPrompt();
    });
  });
}
