// componentes/configuracionProyecto.js — Configuración del Proyecto y LocalStorage Multi-Proyecto

import { PROJECT_FIELDS_SCHEMA } from '../config.js';
import { escapeHtml, findMatchingOption, handleSelectChange, showToast } from '../utils.js';
import { getProyectoActivo, cargarSelectorProyectos } from './selectorProyectos.js';

export async function cargarConfiguracionProyecto() {
  const proyectoActual = getProyectoActivo();
  try {
    let datosBD = {};
    try {
      const respuesta = await fetch(`/api/config/project?project=${encodeURIComponent(proyectoActual)}`);
      if (respuesta.ok) datosBD = await respuesta.json();
    } catch (e) {
      console.warn("API server no disponible, cargando de localStorage");
    }

    const guardadoLocal = JSON.parse(localStorage.getItem(`lpm_project_config_${proyectoActual}`) || '{}');
    const datosFinales = { ...datosBD, ...guardadoLocal };

    const formulario = document.getElementById('form-project');
    if (!formulario) return;
    formulario.innerHTML = '';

    for (const [clave, esquema] of Object.entries(PROJECT_FIELDS_SCHEMA)) {
      const valorBruto = datosFinales[clave] || '';
      const grupo = document.createElement('div');
      grupo.className = 'form-group';

      if (esquema.free) {
        let val = valorBruto;
        const placeholderTexto = esquema.placeholder || "[Coloca aquí la información del proyecto...]";
        grupo.innerHTML = `
          <label>${clave}</label>
          <input type="text" name="${clave}" value="${escapeHtml(val)}" placeholder="${placeholderTexto}">
        `;
        grupo.querySelector('input').addEventListener('input', autoGuardarLocalProyecto);
      } else {
        let val = datosFinales[clave] || '';
        const opcionCoincidente = findMatchingOption(val, esquema.options);
        
        let opcionSeleccionada = '';
        if (!val) {
          opcionSeleccionada = '';
        } else if (opcionCoincidente) {
          opcionSeleccionada = opcionCoincidente;
        } else {
          opcionSeleccionada = 'Otro';
        }

        let opcionesHtml = `<option value="" ${opcionSeleccionada === '' ? 'selected' : ''}>-- Escoge una opción --</option>`;
        opcionesHtml += esquema.options.map(opt => 
          `<option value="${escapeHtml(opt)}" ${opt === opcionSeleccionada ? 'selected' : ''}>${escapeHtml(opt)}</option>`
        ).join('');
        opcionesHtml += `<option value="Otro" ${opcionSeleccionada === 'Otro' ? 'selected' : ''}>✍️ Otro (Especificar personalizado)...</option>`;

        const valorEntradaPersonalizada = opcionSeleccionada === 'Otro' ? val : '';
        const estiloPersonalizado = opcionSeleccionada === 'Otro' ? 'display: block;' : 'display: none;';

        grupo.innerHTML = `
          <label>${clave}</label>
          <select data-key="${clave}">
            ${opcionesHtml}
          </select>
          <input type="text" 
                 class="custom-input-other" 
                 data-key="${clave}" 
                 value="${escapeHtml(valorEntradaPersonalizada)}" 
                 placeholder="[Escribe tu tecnología u opción aquí...]" 
                 style="${estiloPersonalizado} margin-top: 0.5rem;">
        `;

        const elementoSelect = grupo.querySelector('select');
        const elementoEntradaPersonalizada = grupo.querySelector('.custom-input-other');
        
        elementoSelect.addEventListener('change', (e) => {
          handleSelectChange(e.target);
          autoGuardarLocalProyecto();
        });
        elementoEntradaPersonalizada.addEventListener('input', autoGuardarLocalProyecto);
      }
      formulario.appendChild(grupo);
    }
  } catch (err) {
    showToast('Error cargando configuración del proyecto', true);
  }
}

export async function guardarConfiguracionProyecto() {
  const proyectoActual = getProyectoActivo();
  const formulario = document.getElementById('form-project');
  if (!formulario) return;
  const datos = {};

  formulario.querySelectorAll('input[type="text"][name]').forEach(input => {
    datos[input.name] = input.value.trim();
  });

  formulario.querySelectorAll('select[data-key]').forEach(select => {
    const clave = select.getAttribute('data-key');
    if (select.value === 'Otro') {
      const entradaPersonalizada = select.closest('.form-group').querySelector('.custom-input-other');
      datos[clave] = entradaPersonalizada.value.trim() || 'Personalizado';
    } else {
      datos[clave] = select.value;
    }
  });

  localStorage.setItem(`lpm_project_config_${proyectoActual}`, JSON.stringify(datos));

  try {
    const respuesta = await fetch('/api/config/project', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_name: proyectoActual,
        config: datos
      })
    });
    if (respuesta.ok) {
      showToast(`Configuración de '${proyectoActual}' guardada en SQLite & LocalStorage`);
      await cargarSelectorProyectos();
    } else {
      showToast('Guardado en LocalStorage (Prueba Local)');
    }
  } catch (err) {
    showToast('Guardado localmente en LocalStorage (API no disponible)', false);
  }
}

export function autoGuardarLocalProyecto() {
  const proyectoActual = getProyectoActivo();
  const formulario = document.getElementById('form-project');
  if (!formulario) return;
  const datos = {};

  formulario.querySelectorAll('input[type="text"][name]').forEach(input => {
    if (input.value.trim()) datos[input.name] = input.value.trim();
  });

  formulario.querySelectorAll('select[data-key]').forEach(select => {
    const clave = select.getAttribute('data-key');
    if (select.value === 'Otro') {
      const entradaPersonalizada = select.closest('.form-group').querySelector('.custom-input-other');
      if (entradaPersonalizada.value.trim()) datos[clave] = entradaPersonalizada.value.trim();
    } else if (select.value) {
      datos[clave] = select.value;
    }
  });

  localStorage.setItem(`lpm_project_config_${proyectoActual}`, JSON.stringify(datos));
}
