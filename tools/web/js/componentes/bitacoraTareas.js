// componentes/bitacoraTareas.js — Bitácora de Tareas e Interacciones

import { escapeHtml, showToast } from '../utils.js';

export async function cargarTareas() {
  try {
    const respuesta = await fetch('/api/tasks');
    const lista = await respuesta.json();
    const contenedor = document.getElementById('tasks-container');
    if (!contenedor) return;
    contenedor.innerHTML = '';

    if (lista.length === 0) {
      contenedor.innerHTML = '<p class="text-muted">Bitácora vacía.</p>';
      return;
    }

    lista.forEach(item => {
      const elemento = document.createElement('div');
      elemento.className = 'timeline-item';
      elemento.innerHTML = `
        <div class="timeline-time">${item.created_at}</div>
        <div class="timeline-text" style="flex: 1;">${escapeHtml(item.task_summary)}</div>
        <button class="btn-delete" data-id="${item.id}" title="Eliminar entrada">🗑️</button>
      `;
      elemento.querySelector('.btn-delete').addEventListener('click', () => eliminarLogTarea(item.id));
      contenedor.appendChild(elemento);
    });
  } catch (err) {
    showToast('Error cargando bitácora', true);
  }
}

export function establecerPlantillaTarea(texto) {
  const entrada = document.getElementById('task-input');
  if (entrada) entrada.value = texto;
}

export async function agregarLogTarea() {
  const entrada = document.getElementById('task-input');
  if (!entrada) return;
  const resumen = entrada.value.trim();

  if (!resumen) {
    showToast('Ingresa una descripción para el log', true);
    return;
  }

  try {
    const respuesta = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task_summary: resumen })
    });
    if (respuesta.ok) {
      showToast('Entrada agregada a la bitácora');
      entrada.value = '';
      cargarTareas();
    }
  } catch (err) {
    showToast('Error agregando log', true);
  }
}

export async function eliminarLogTarea(id) {
  if (!confirm('¿Deseas eliminar este registro de la bitácora?')) return;
  try {
    const respuesta = await fetch('/api/tasks/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    });
    if (respuesta.ok) {
      showToast('Entrada eliminada de la bitácora');
      cargarTareas();
    }
  } catch (err) {
    showToast('Error al eliminar log', true);
  }
}
