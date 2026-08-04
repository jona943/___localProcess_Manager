// componentes/visorPrompt.js — Visor, copiado y compilador de prompt.md

import { showToast } from '../utils.js';

export async function cargarVistaPreviaPrompt() {
  const elemento = document.getElementById('prompt-preview');
  if (!elemento) return;
  try {
    const respuesta = await fetch('/api/prompt');
    const texto = await respuesta.text();
    elemento.innerText = texto;
  } catch (err) {
    elemento.innerText = 'Error al cargar prompt.md';
  }
}

export async function compilarPrompt() {
  try {
    const respuesta = await fetch('/api/compile', { method: 'POST' });
    const datos = await respuesta.json();
    if (respuesta.ok) {
      showToast('¡prompt.md compilado exitosamente!');
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
