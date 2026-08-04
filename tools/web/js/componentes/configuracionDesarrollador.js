// componentes/configuracionDesarrollador.js — Configuración del Desarrollador y LocalStorage

import { DEVELOPER_FIELDS_SCHEMA } from '../config.js';
import { escapeHtml, findMatchingOption, handleSelectChange, showToast } from '../utils.js';

export async function cargarConfiguracionDesarrollador() {
  try {
    let datosBD = {};
    try {
      const respuesta = await fetch('/api/config/developer');
      if (respuesta.ok) datosBD = await respuesta.json();
    } catch (e) {
      console.warn("API server no disponible, cargando de localStorage");
    }

    const guardadoLocal = JSON.parse(localStorage.getItem('lpm_developer_config') || '{}');
    const datosFinales = { ...datosBD, ...guardadoLocal };

    const formulario = document.getElementById('form-developer');
    if (!formulario) return;
    formulario.innerHTML = '';

    for (const [clave, esquema] of Object.entries(DEVELOPER_FIELDS_SCHEMA)) {
      let valorBruto = datosFinales[clave] || '';
      
      if (valorBruto === 'Desarrollador' || valorBruto === 'Agente-AI') {
        valorBruto = '';
      }

      const grupo = document.createElement('div');
      grupo.className = 'form-group';

      if (esquema.free) {
        const placeholderTexto = esquema.placeholder || "[Escribe aquí tu configuración...]";
        grupo.innerHTML = `
          <label>${clave}</label>
          <input type="text" name="${clave}" value="${escapeHtml(valorBruto)}" placeholder="${placeholderTexto}">
        `;
        grupo.querySelector('input').addEventListener('input', autoGuardarLocalDesarrollador);
      } else {
        let valorBruto = guardadoLocal[clave] || '';
        const opcionCoincidente = findMatchingOption(valorBruto, esquema.options);
        
        let opcionSeleccionada = '';
        if (!valorBruto) {
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

        const valorEntradaPersonalizada = opcionSeleccionada === 'Otro' ? valorBruto : '';
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
                 placeholder="[Escribe tu opción personalizada aquí...]" 
                 style="${estiloPersonalizado} margin-top: 0.5rem;">
        `;

        const elementoSelect = grupo.querySelector('select');
        const elementoEntradaPersonalizada = grupo.querySelector('.custom-input-other');
        
        elementoSelect.addEventListener('change', (e) => {
          handleSelectChange(e.target);
          autoGuardarLocalDesarrollador();
        });
        elementoEntradaPersonalizada.addEventListener('input', autoGuardarLocalDesarrollador);
      }
      formulario.appendChild(grupo);
    }
  } catch (err) {
    showToast('Error cargando configuración del desarrollador', true);
  }
}

export async function guardarConfiguracionDesarrollador() {
  const formulario = document.getElementById('form-developer');
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

  localStorage.setItem('lpm_developer_config', JSON.stringify(datos));

  try {
    const respuesta = await fetch('/api/config/developer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos)
    });
    if (respuesta.ok) {
      showToast('Configuración del Desarrollador guardada (LocalStorage & SQLite)');
    } else {
      showToast('Guardado en LocalStorage (Prueba Local)');
    }
  } catch (err) {
    showToast('Guardado localmente en LocalStorage (API no disponible)', false);
  }
}

export function autoGuardarLocalDesarrollador() {
  const formulario = document.getElementById('form-developer');
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

  localStorage.setItem('lpm_developer_config', JSON.stringify(datos));
}
