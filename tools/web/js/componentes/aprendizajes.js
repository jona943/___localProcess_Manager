// componentes/aprendizajes.js — Gestión de Aprendizajes Clave Multi-Proyecto

import { escapeHtml, handleSelectChange, showToast } from '../utils.js';
import { getProyectoActivo } from './selectorProyectos.js';

export async function cargarAprendizajes() {
  const proyectoActual = getProyectoActivo();
  try {
    const respuesta = await fetch(`/api/learnings?project=${encodeURIComponent(proyectoActual)}`);
    const lista = await respuesta.json();
    const contenedor = document.getElementById('learnings-container');
    if (!contenedor) return;
    contenedor.innerHTML = '';

    if (lista.length === 0) {
      contenedor.innerHTML = `<p class="text-muted">No hay reglas registradas aún para el proyecto '${escapeHtml(proyectoActual)}'.</p>`;
      return;
    }

    lista.forEach(item => {
      const tarjeta = document.createElement('div');
      tarjeta.className = 'learning-card';
      const esGlobal = item.project_name === 'global';
      const badgeProyecto = esGlobal ? '🌐 Global' : `📁 ${escapeHtml(item.project_name || proyectoActual)}`;

      tarjeta.innerHTML = `
        <div class="learning-header">
          <div>
            <span class="learning-cat">${escapeHtml(item.category)}</span>
            <span class="learning-title">${escapeHtml(item.topic)}</span>
            <span style="font-size: 0.75rem; background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; margin-left: 6px;">${badgeProyecto}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span class="learning-meta">Relevancia: ${item.importance}/5</span>
            <button class="btn-delete" data-id="${item.id}" title="Eliminar regla">🗑️ Eliminar</button>
          </div>
        </div>
        <p class="learning-rule">${escapeHtml(item.rule)}</p>
        <div class="learning-meta">Registrado: ${item.created_at}</div>
      `;
      tarjeta.querySelector('.btn-delete').addEventListener('click', () => eliminarAprendizaje(item.id));
      contenedor.appendChild(tarjeta);
    });
  } catch (err) {
    showToast('Error cargando aprendizajes', true);
  }
}

export async function agregarAprendizaje() {
  const proyectoActual = getProyectoActivo();
  const elementoSelect = document.getElementById('learn-category-select');
  const elementoEntradaPersonalizada = document.getElementById('learn-category-custom');
  if (!elementoSelect || !elementoEntradaPersonalizada) return;

  let categoria = elementoSelect.value === 'Otro' ? elementoEntradaPersonalizada.value.trim() : elementoSelect.value;
  
  const elementoTema = document.getElementById('learn-topic');
  const elementoRegla = document.getElementById('learn-rule');
  const elementoImportancia = document.getElementById('learn-importance');

  const tema = elementoTema ? elementoTema.value.trim() : '';
  const regla = elementoRegla ? elementoRegla.value.trim() : '';
  const importancia = elementoImportancia ? parseInt(elementoImportancia.value) || 3 : 3;

  if (!categoria || !tema || !regla) {
    showToast('Por favor completa todos los campos del aprendizaje', true);
    return;
  }

  try {
    const respuesta = await fetch('/api/learnings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_name: proyectoActual,
        category: categoria,
        topic: tema,
        rule: regla,
        importance: importancia
      })
    });
    if (respuesta.ok) {
      showToast(`Regla registrada para '${proyectoActual}'`);
      elementoSelect.value = '';
      elementoEntradaPersonalizada.value = '';
      elementoEntradaPersonalizada.style.display = 'none';
      if (elementoTema) elementoTema.value = '';
      if (elementoRegla) elementoRegla.value = '';
      cargarAprendizajes();
    }
  } catch (err) {
    showToast('Error registrando regla', true);
  }
}

export async function eliminarAprendizaje(id) {
  const proyectoActual = getProyectoActivo();
  if (!confirm('¿Estás seguro de eliminar esta regla de la memoria?')) return;
  try {
    const respuesta = await fetch('/api/learnings/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, project_name: proyectoActual })
    });
    if (respuesta.ok) {
      showToast('Regla eliminada de la memoria');
      cargarAprendizajes();
    }
  } catch (err) {
    showToast('Error al eliminar la regla', true);
  }
}

export function inicializarEventosAprendizajes() {
  const elementoSelect = document.getElementById('learn-category-select');
  if (elementoSelect) {
    elementoSelect.addEventListener('change', (e) => handleSelectChange(e.target));
  }
}
