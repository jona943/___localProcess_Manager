// componentes/aprendizajes.js — Gestión de Aprendizajes Clave y Reglas Persistentes

import { escapeHtml, handleSelectChange, showToast } from '../utils.js';

export async function cargarAprendizajes() {
  try {
    const respuesta = await fetch('/api/learnings');
    const lista = await respuesta.json();
    const contenedor = document.getElementById('learnings-container');
    if (!contenedor) return;
    contenedor.innerHTML = '';

    if (lista.length === 0) {
      contenedor.innerHTML = '<p class="text-muted">No hay reglas registradas aún.</p>';
      return;
    }

    lista.forEach(item => {
      const tarjeta = document.createElement('div');
      tarjeta.className = 'learning-card';
      tarjeta.innerHTML = `
        <div class="learning-header">
          <div>
            <span class="learning-cat">${escapeHtml(item.category)}</span>
            <span class="learning-title">${escapeHtml(item.topic)}</span>
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
      body: JSON.stringify({ category: categoria, topic: tema, rule: regla, importance: importancia })
    });
    if (respuesta.ok) {
      showToast('Regla clave registrada exitosamente');
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
  if (!confirm('¿Estás seguro de eliminar esta regla de la memoria?')) return;
  try {
    const respuesta = await fetch('/api/learnings/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
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
