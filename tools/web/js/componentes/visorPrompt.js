// componentes/visorPrompt.js — Visor, copiado y compilador de prompt.md Multi-Proyecto

import { showToast } from '../utils.js';
import { getProyectoActivo } from './selectorProyectos.js';

export async function cargarVistaPreviaPrompt() {
  const proyectoActual = getProyectoActivo();
  const elemento = document.getElementById('prompt-preview');
  if (!elemento) return;
  try {
    const respuesta = await fetch(`/api/prompt?project=${encodeURIComponent(proyectoActual)}`);
    const texto = await respuesta.text();
    elemento.innerText = texto;
  } catch (err) {
    elemento.innerText = 'Error al cargar prompt.md';
  }
}

export async function compilarPrompt() {
  const proyectoActual = getProyectoActivo();
  try {
    const respuesta = await fetch('/api/compile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_name: proyectoActual })
    });
    const datos = await respuesta.json();
    if (respuesta.ok) {
      showToast(`¡prompt.md compilado exitosamente para '${proyectoActual}'!`);
      cargarVistaPreviaPrompt();
    } else {
      showToast('Error compilando prompt: ' + datos.error, true);
    }
  } catch (err) {
    showToast('Error enviando petición de compilación', true);
  }
}

export function copiarPrompt() {
  const elemento = document.getElementById('prompt-preview');
  if (!elemento) return;
  const texto = elemento.innerText;
  navigator.clipboard.writeText(texto);
  showToast('¡prompt.md copiado al portapapeles!');
}
