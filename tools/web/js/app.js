// app.js — Punto de Entrada Principal e Inicialización Modular (ES Modules Multi-Proyecto)

import { inicializarNavegacion } from './componentes/navegacion.js';
import { cargarSelectorProyectos, registrarNuevoProyecto, eliminarProyectoActivo } from './componentes/selectorProyectos.js';
import { cargarConfiguracionDesarrollador, guardarConfiguracionDesarrollador } from './componentes/configuracionDesarrollador.js';
import { cargarConfiguracionProyecto, guardarConfiguracionProyecto } from './componentes/configuracionProyecto.js';
import { agregarAprendizaje, cargarAprendizajes, inicializarEventosAprendizajes } from './componentes/aprendizajes.js';
import { agregarLogTarea, cargarTareas, establecerPlantillaTarea } from './componentes/bitacoraTareas.js';
import { compilarPrompt, copiarPrompt } from './componentes/visorPrompt.js';

import { limpiarLocalStorage } from './utils.js';
import { refrescarComponentesPorProyecto } from './componentes/selectorProyectos.js';

document.addEventListener('DOMContentLoaded', async () => {
  // Inicializar navegación de pestañas
  inicializarNavegacion();

  // Cargar selector de proyectos y datos iniciales
  await cargarSelectorProyectos();
  cargarConfiguracionDesarrollador();
  cargarConfiguracionProyecto();
  cargarAprendizajes();
  cargarTareas();

  // Inicializar listeners de eventos
  inicializarEventosAprendizajes();

  const btnNuevoProyecto = document.getElementById('btn-nuevo-proyecto');
  if (btnNuevoProyecto) {
    btnNuevoProyecto.addEventListener('click', registrarNuevoProyecto);
  }

  const btnEliminarProyecto = document.getElementById('btn-eliminar-proyecto');
  if (btnEliminarProyecto) {
    btnEliminarProyecto.addEventListener('click', eliminarProyectoActivo);
  }

  const btnClearLocalStorage = document.getElementById('btn-clear-localstorage');
  if (btnClearLocalStorage) {
    btnClearLocalStorage.addEventListener('click', () => {
      limpiarLocalStorage(() => {
        cargarConfiguracionDesarrollador();
        refrescarComponentesPorProyecto();
      });
    });
  }

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
