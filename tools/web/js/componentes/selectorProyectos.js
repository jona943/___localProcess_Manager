// componentes/selectorProyectos.js — Gestor y Selector Global de Proyectos (Frontend UI)

import { showToast, escapeHtml } from '../utils.js';
import { cargarConfiguracionProyecto } from './configuracionProyecto.js';
import { cargarAprendizajes } from './aprendizajes.js';
import { cargarTareas } from './bitacoraTareas.js';
import { cargarVistaPreviaPrompt } from './visorPrompt.js';

let proyectoActivo = localStorage.getItem('lpm_active_project') || 'default';

export function getProyectoActivo() {
  return proyectoActivo;
}

export function setProyectoActivo(nombre) {
  proyectoActivo = nombre;
  localStorage.setItem('lpm_active_project', nombre);
  refrescarComponentesPorProyecto();
}

export async function cargarSelectorProyectos() {
  try {
    const res = await fetch('/api/projects');
    const proyectos = await res.json();
    const selectElem = document.getElementById('seleccion-proyecto-activo');
    if (!selectElem) return;

    selectElem.innerHTML = '';
    
    // Si no hay proyectos, agregar por defecto
    if (proyectos.length === 0) {
      proyectos.push({ name: 'default', path: './' });
    }

    let encontrado = false;
    proyectos.forEach(p => {
      if (p.name === proyectoActivo) encontrado = true;
      const opt = document.createElement('option');
      opt.value = p.name;
      opt.innerText = `📁 Proyecto: ${p.name}`;
      if (p.name === proyectoActivo) opt.selected = true;
      selectElem.appendChild(opt);
    });

    if (!encontrado && proyectos.length > 0) {
      proyectoActivo = proyectos[0].name;
      localStorage.setItem('lpm_active_project', proyectoActivo);
      selectElem.value = proyectoActivo;
    }

    selectElem.removeEventListener('change', handleProjectChange);
    selectElem.addEventListener('change', handleProjectChange);

  } catch (err) {
    showToast('Error al cargar la lista de proyectos', true);
  }
}

function handleProjectChange(e) {
  const nuevoProyecto = e.target.value;
  setProyectoActivo(nuevoProyecto);
  showToast(`Proyecto activo cambiado a: ${nuevoProyecto}`);
}

export function refrescarComponentesPorProyecto() {
  cargarConfiguracionProyecto();
  cargarAprendizajes();
  cargarTareas();
  cargarVistaPreviaPrompt();
}

export async function registrarNuevoProyecto() {
  const nombre = prompt("Ingresa el nombre del nuevo proyecto (ej. SmartFit-MVP):");
  if (!nombre || !nombre.trim()) return;

  const ruta = prompt("Ruta relativa o absoluta del proyecto (ej. ./ o ../MiProyecto):", "./") || "./";
  const archivoContexto = prompt("Archivo de contexto técnico (ej. README.md):", "README.md") || "README.md";

  try {
    const res = await fetch('/api/projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: nombre.trim(),
        path: ruta.trim(),
        context_file: archivoContexto.trim()
      })
    });

    if (res.ok) {
      showToast(`¡Proyecto '${nombre.trim()}' registrado con éxito!`);
      proyectoActivo = nombre.trim();
      localStorage.setItem('lpm_active_project', proyectoActivo);
      await cargarSelectorProyectos();
      refrescarComponentesPorProyecto();
    } else {
      showToast('Error al crear el proyecto', true);
    }
  } catch (err) {
    showToast('Error conectando con el servidor', true);
  }
}
