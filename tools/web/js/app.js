// app.js — Punto de Entrada Principal e Inicialización Modular (ES Modules)

import { inicializarNavegacion } from './componentes/navegacion.js';
import { cargarConfiguracionDesarrollador, guardarConfiguracionDesarrollador } from './componentes/configuracionDesarrollador.js';
import { cargarConfiguracionProyecto, guardarConfiguracionProyecto } from './componentes/configuracionProyecto.js';
import { agregarAprendizaje, cargarAprendizajes, inicializarEventosAprendizajes } from './componentes/aprendizajes.js';
import { agregarLogTarea, cargarTareas, establecerPlantillaTarea } from './componentes/bitacoraTareas.js';
import { compilarPrompt, copiarPrompt } from './componentes/visorPrompt.js';

document.addEventListener('DOMContentLoaded', () => {
  // Inicializar navegación de pestañas
  inicializarNavegacion();

  // Cargar datos iniciales de los componentes
  cargarConfiguracionDesarrollador();
  cargarConfiguracionProyecto();
  cargarAprendizajes();
  cargarTareas();

  // Inicializar listeners de eventos
  inicializarEventosAprendizajes();

  // Exponer funciones necesarias a la ventana global
  window.saveDeveloperConfig = guardarConfiguracionDesarrollador;
  window.saveProjectConfig = guardarConfiguracionProyecto;
  window.addLearning = agregarAprendizaje;
  window.addTaskLog = agregarLogTarea;
  window.setTaskPreset = establecerPlantillaTarea;
  window.copyPrompt = copiarPrompt;

  const botonCompilar = document.getElementById('btn-compile-prompt');
  if (botonCompilar) {
    botonCompilar.addEventListener('click', compilarPrompt);
  }
});
