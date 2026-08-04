// Navigation & Tab Switching
document.querySelectorAll('.nav-item').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

    button.classList.add('active');
    const tabName = button.getAttribute('data-tab');
    document.getElementById(`tab-${tabName}`).classList.add('active');

    // Update Header Title
    const titles = {
      developer: ['Configuración del Desarrollador', 'Personalidad del agente, idioma y preferencias de didáctica'],
      project: ['Configuración del Proyecto', 'Estándares del proyecto, stack tecnológico y arquitectura'],
      learnings: ['Aprendizajes Clave & Reglas Persistentes', 'Memoria semántica registrada para evitar repetir errores'],
      tasks: ['Bitácora de Tareas & Interacciones', 'Historial cronológico de actividades completadas'],
      prompt: ['Visor de System Prompt (prompt.md)', 'Vista previa del prompt compilado inyectable a la IA']
    };
    if (titles[tabName]) {
      document.getElementById('page-title').innerText = titles[tabName][0];
      document.getElementById('page-subtitle').innerText = titles[tabName][1];
    }

    if (tabName === 'prompt') loadPromptPreview();
  });
});

// Load Initial Data
document.addEventListener('DOMContentLoaded', () => {
  loadDeveloperConfig();
  loadProjectConfig();
  loadLearnings();
  loadTasks();
});

// Schema for Developer Config Fields
const DEVELOPER_FIELDS_SCHEMA = {
  "Nombre del Programador": { free: true, placeholder: "ej: Alex / Tu Nombre o Usuario" },
  "Nombre del Agente": { free: true, placeholder: "ej: Asistente-AI / Nombre para tu Agente" },
  "Personalidad/Tono": {
    options: [
      "Profesional, didáctico y directo",
      "Español latino formal y estructurado",
      "Mentor técnico formal y estructurado",
      "Conciso, al grano y pragmático",
      "Didáctico y explicativo paso a paso"
    ]
  },
  "Idioma Principal": {
    options: [
      "Español",
      "Inglés",
      "Portugués",
      "Francés",
      "Alemán"
    ]
  },
  "Terminología Técnica": {
    options: [
      "1. Totalmente traducido al español",
      "2. Español con términos básicos en inglés",
      "3. Spanglish técnico estándar",
      "4. Términos técnicos en inglés con sintaxis nativa",
      "5. 100% Inglés técnico puro"
    ]
  },
  "Nivel de Didáctica": {
    options: [
      "1. Máximo / Didáctico (Explicar paso a paso)",
      "2. Alto (Explicar conceptos principales)",
      "3. Medio (Resúmenes breves y fragmentos directos)",
      "4. Avanzado (Respuestas concisas, explicar solo lo mínimo)",
      "5. Experto / Nulo (Sin explicaciones, solo código)"
    ]
  },
  "Comentarios en Código": {
    options: [
      "Instructivo y sencillo",
      "Solo lo necesario",
      "Sin comentarios"
    ]
  },
  "Frecuencia de Feedback": {
    options: [
      "Frecuente",
      "Ocasional",
      "Ninguno"
    ]
  }
};

// Helper to find matching standard option
function findMatchingOption(currentVal, options) {
  if (!currentVal) return null;
  const valLower = currentVal.toLowerCase().trim();
  // 1. Exact match
  const exact = options.find(opt => opt.toLowerCase() === valLower);
  if (exact) return exact;

  // 2. Flexible match
  const partial = options.find(opt => {
    const optLower = opt.toLowerCase();
    return optLower.includes(valLower) || 
           valLower.includes(optLower) ||
           (valLower.includes("paso a paso") && optLower.includes("paso a paso")) ||
           (valLower.includes("instructiv") && optLower.includes("instructiv"));
  });
  return partial || null;
}

// 1. Developer Config
async function loadDeveloperConfig() {
  try {
    const res = await fetch('/api/config/developer');
    const dbData = await res.json();
    const form = document.getElementById('form-developer');
    form.innerHTML = '';

    for (const [key, schema] of Object.entries(DEVELOPER_FIELDS_SCHEMA)) {
      const currentValue = dbData[key] || '';
      const group = document.createElement('div');
      group.className = 'form-group';

      if (schema.free) {
        const ph = schema.placeholder || "Escribe aquí...";
        group.innerHTML = `
          <label>${key}</label>
          <input type="text" name="${key}" value="${escapeHtml(currentValue)}" placeholder="${ph}">
        `;
      } else {
        const matchedOption = findMatchingOption(currentValue, schema.options);
        const hasValue = Boolean(currentValue);
        
        let selectedOption = '';
        if (!hasValue) {
          selectedOption = ''; // Select '-- Escoge una opción --'
        } else if (matchedOption) {
          selectedOption = matchedOption;
        } else {
          selectedOption = 'Otro';
        }

        let optionsHtml = `<option value="" ${selectedOption === '' ? 'selected' : ''}>-- Escoge una opción --</option>`;
        optionsHtml += schema.options.map(opt => 
          `<option value="${escapeHtml(opt)}" ${opt === selectedOption ? 'selected' : ''}>${escapeHtml(opt)}</option>`
        ).join('');
        optionsHtml += `<option value="Otro" ${selectedOption === 'Otro' ? 'selected' : ''}>✍️ Otro (Especificar personalizado)...</option>`;

        const customInputValue = selectedOption === 'Otro' ? currentValue : '';
        const customStyle = selectedOption === 'Otro' ? 'display: block;' : 'display: none;';

        group.innerHTML = `
          <label>${key}</label>
          <select data-key="${key}" onchange="handleSelectChange(this)">
            ${optionsHtml}
          </select>
          <input type="text" 
                 class="custom-input-other" 
                 data-key="${key}" 
                 value="${escapeHtml(customInputValue)}" 
                 placeholder="Escribe tu opción personalizada aquí..." 
                 style="${customStyle} margin-top: 0.5rem;">
        `;
      }
      form.appendChild(group);
    }
  } catch (err) {
    showToast('Error cargando configuración del desarrollador', true);
  }
}

function handleSelectChange(selectElem) {
  const group = selectElem.closest('.form-group');
  const customInput = group.querySelector('.custom-input-other');
  if (selectElem.value === 'Otro') {
    customInput.style.display = 'block';
    customInput.focus();
  } else {
    customInput.style.display = 'none';
  }
}

async function saveDeveloperConfig() {
  const form = document.getElementById('form-developer');
  const payload = {};

  // Parse Free Inputs
  form.querySelectorAll('input[type="text"][name]').forEach(input => {
    payload[input.name] = input.value.trim();
  });

  // Parse Selects with "Otro" logic
  form.querySelectorAll('select[data-key]').forEach(select => {
    const key = select.getAttribute('data-key');
    if (select.value === 'Otro') {
      const customInput = select.closest('.form-group').querySelector('.custom-input-other');
      payload[key] = customInput.value.trim() || 'Personalizado';
    } else {
      payload[key] = select.value;
    }
  });

  try {
    const res = await fetch('/api/config/developer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      showToast('Configuración del Desarrollador guardada y sincronizada a Markdown');
    }
  } catch (err) {
    showToast('Error guardando configuración', true);
  }
}

// Schema for Project Config Fields
const PROJECT_FIELDS_SCHEMA = {
  "Nombre del Proyecto": { free: true },
  "Directorio del Proyecto": { free: true },
  "Archivo de Contexto": { free: true },
  "Tecnologías Principales": {
    options: [
      "Node.js, JavaScript, HTML5",
      "Python 3, Fast-API / Flask",
      "React, TypeScript, TailwindCSS",
      "Next.js, React, Node.js",
      "Go (Golang), gRPC, Docker",
      "Java, Spring Boot",
      "C# (.NET Core)",
      "PHP, Laravel"
    ]
  },
  "Módulos": {
    options: [
      "ES Modules (import / export)",
      "CommonJS (require)",
      "Módulos Estándar de Python",
      "Go Modules",
      "Cargo / Rust Crates"
    ]
  },
  "Estilos (CSS)": {
    options: [
      "Vanilla CSS (Mover inline a externos)",
      "TailwindCSS (Clases de utilidad)",
      "Sass / SCSS",
      "CSS Modules",
      "Styled Components",
      "Bootstrap"
    ]
  },
  "Manejo de Asincronía": {
    options: [
      "Asíncrono puro (async/await, Promesas)",
      "Asyncio / Native SQLite",
      "Callbacks / Event Loop tradicional",
      "RxJS / Observables",
      "Multiprocesamiento / Threads"
    ]
  },
  "Arquitectura de Código": {
    options: [
      "Modular src/ (routes, controllers, services)",
      "Dual-Drive (SQLite + MCP + UI)",
      "Modelo-Vista-Controlador (MVC)",
      "Arquitectura Hexagonal / Clean Architecture",
      "Microservicios Decoplados"
    ]
  }
};

// 2. Project Config
async function loadProjectConfig() {
  try {
    const res = await fetch('/api/config/project');
    const dbData = await res.json();
    const form = document.getElementById('form-project');
    form.innerHTML = '';

    for (const [key, schema] of Object.entries(PROJECT_FIELDS_SCHEMA)) {
      const currentValue = dbData[key] || '';
      const group = document.createElement('div');
      group.className = 'form-group';

      if (schema.free) {
        group.innerHTML = `
          <label>${key}</label>
          <input type="text" name="${key}" value="${escapeHtml(currentValue)}" placeholder="Escribe aquí...">
        `;
      } else {
        const matchedOption = findMatchingOption(currentValue, schema.options);
        const hasValue = Boolean(currentValue);
        
        let selectedOption = '';
        if (!hasValue) {
          selectedOption = '';
        } else if (matchedOption) {
          selectedOption = matchedOption;
        } else {
          selectedOption = 'Otro';
        }

        let optionsHtml = `<option value="" ${selectedOption === '' ? 'selected' : ''}>-- Escoge una opción --</option>`;
        optionsHtml += schema.options.map(opt => 
          `<option value="${escapeHtml(opt)}" ${opt === selectedOption ? 'selected' : ''}>${escapeHtml(opt)}</option>`
        ).join('');
        optionsHtml += `<option value="Otro" ${selectedOption === 'Otro' ? 'selected' : ''}>✍️ Otro (Especificar personalizado)...</option>`;

        const customInputValue = selectedOption === 'Otro' ? currentValue : '';
        const customStyle = selectedOption === 'Otro' ? 'display: block;' : 'display: none;';

        group.innerHTML = `
          <label>${key}</label>
          <select data-key="${key}" onchange="handleSelectChange(this)">
            ${optionsHtml}
          </select>
          <input type="text" 
                 class="custom-input-other" 
                 data-key="${key}" 
                 value="${escapeHtml(customInputValue)}" 
                 placeholder="Escribe tu tecnología/opción aquí..." 
                 style="${customStyle} margin-top: 0.5rem;">
        `;
      }
      form.appendChild(group);
    }
  } catch (err) {
    showToast('Error cargando configuración del proyecto', true);
  }
}

async function saveProjectConfig() {
  const form = document.getElementById('form-project');
  const payload = {};

  // Parse Free Inputs
  form.querySelectorAll('input[type="text"][name]').forEach(input => {
    payload[input.name] = input.value.trim();
  });

  // Parse Selects with "Otro" logic
  form.querySelectorAll('select[data-key]').forEach(select => {
    const key = select.getAttribute('data-key');
    if (select.value === 'Otro') {
      const customInput = select.closest('.form-group').querySelector('.custom-input-other');
      payload[key] = customInput.value.trim() || 'Personalizado';
    } else {
      payload[key] = select.value;
    }
  });

  try {
    const res = await fetch('/api/config/project', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      showToast('Configuración del Proyecto guardada y sincronizada a Markdown');
    }
  } catch (err) {
    showToast('Error guardando configuración', true);
  }
}

// 3. Learnings
function handleLearningCategoryChange(selectElem) {
  const customInput = document.getElementById('learn-category-custom');
  if (selectElem.value === 'Otro') {
    customInput.style.display = 'block';
    customInput.focus();
  } else {
    customInput.style.display = 'none';
  }
}

async function loadLearnings() {
  try {
    const res = await fetch('/api/learnings');
    const list = await res.json();
    const container = document.getElementById('learnings-container');
    container.innerHTML = '';

    if (list.length === 0) {
      container.innerHTML = '<p class="text-muted">No hay reglas registradas aún.</p>';
      return;
    }

    list.forEach(item => {
      const card = document.createElement('div');
      card.className = 'learning-card';
      card.innerHTML = `
        <div class="learning-header">
          <div>
            <span class="learning-cat">${escapeHtml(item.category)}</span>
            <span class="learning-title">${escapeHtml(item.topic)}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span class="learning-meta">Relevancia: ${item.importance}/5</span>
            <button class="btn-delete" onclick="deleteLearning(${item.id})" title="Eliminar regla">🗑️ Eliminar</button>
          </div>
        </div>
        <p class="learning-rule">${escapeHtml(item.rule)}</p>
        <div class="learning-meta">Registrado: ${item.created_at}</div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    showToast('Error cargando aprendizajes', true);
  }
}

async function addLearning() {
  const selectElem = document.getElementById('learn-category-select');
  const customInput = document.getElementById('learn-category-custom');
  let category = selectElem.value === 'Otro' ? customInput.value.trim() : selectElem.value;
  
  const topic = document.getElementById('learn-topic').value.trim();
  const rule = document.getElementById('learn-rule').value.trim();
  const importance = parseInt(document.getElementById('learn-importance').value) || 3;

  if (!category || !topic || !rule) {
    showToast('Por favor completa todos los campos del aprendizaje', true);
    return;
  }

  try {
    const res = await fetch('/api/learnings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category, topic, rule, importance })
    });
    if (res.ok) {
      showToast('Regla clave registrada exitosamente');
      selectElem.value = '';
      customInput.value = '';
      customInput.style.display = 'none';
      document.getElementById('learn-topic').value = '';
      document.getElementById('learn-rule').value = '';
      loadLearnings();
    }
  } catch (err) {
    showToast('Error registrando regla', true);
  }
}

async function deleteLearning(id) {
  if (!confirm('¿Estás seguro de eliminar esta regla de la memoria?')) return;
  try {
    const res = await fetch('/api/learnings/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    });
    if (res.ok) {
      showToast('Regla eliminada de la memoria');
      loadLearnings();
    }
  } catch (err) {
    showToast('Error al eliminar la regla', true);
  }
}

// 4. Tasks
function setTaskPreset(text) {
  document.getElementById('task-input').value = text;
}

async function loadTasks() {
  try {
    const res = await fetch('/api/tasks');
    const list = await res.json();
    const container = document.getElementById('tasks-container');
    container.innerHTML = '';

    if (list.length === 0) {
      container.innerHTML = '<p class="text-muted">Bitácora vacía.</p>';
      return;
    }

    list.forEach(item => {
      const el = document.createElement('div');
      el.className = 'timeline-item';
      el.innerHTML = `
        <div class="timeline-time">${item.created_at}</div>
        <div class="timeline-text" style="flex: 1;">${escapeHtml(item.task_summary)}</div>
        <button class="btn-delete" onclick="deleteTaskLog(${item.id})" title="Eliminar entrada">🗑️</button>
      `;
      container.appendChild(el);
    });
  } catch (err) {
    showToast('Error cargando bitácora', true);
  }
}

async function addTaskLog() {
  const input = document.getElementById('task-input');
  const summary = input.value.trim();

  if (!summary) {
    showToast('Ingresa una descripción para el log', true);
    return;
  }

  try {
    const res = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task_summary: summary })
    });
    if (res.ok) {
      showToast('Entrada agregada a la bitácora');
      input.value = '';
      loadTasks();
    }
  } catch (err) {
    showToast('Error agregando log', true);
  }
}

async function deleteTaskLog(id) {
  if (!confirm('¿Deseas eliminar este registro de la bitácora?')) return;
  try {
    const res = await fetch('/api/tasks/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    });
    if (res.ok) {
      showToast('Entrada eliminada de la bitácora');
      loadTasks();
    }
  } catch (err) {
    showToast('Error al eliminar log', true);
  }
}

// 5. Prompt Preview & Compile
async function loadPromptPreview() {
  try {
    const res = await fetch('/api/prompt');
    const text = await res.text();
    document.getElementById('prompt-preview').innerText = text;
  } catch (err) {
    document.getElementById('prompt-preview').innerText = 'Error al cargar prompt.md';
  }
}

document.getElementById('btn-compile-prompt').addEventListener('click', async () => {
  try {
    const res = await fetch('/api/compile', { method: 'POST' });
    const data = await res.json();
    if (res.ok) {
      showToast('¡prompt.md compilado exitosamente!');
      loadPromptPreview();
    } else {
      showToast('Error compilando prompt: ' + data.error, true);
    }
  } catch (err) {
    showToast('Error enviando petición de compilación', true);
  }
});

function copyPrompt() {
  const text = document.getElementById('prompt-preview').innerText;
  navigator.clipboard.writeText(text);
  showToast('¡prompt.md copiado al portapapeles!');
}

// Helpers
function showToast(message, isError = false) {
  const toast = document.getElementById('toast');
  toast.innerText = message;
  toast.style.backgroundColor = isError ? 'var(--danger)' : 'var(--accent-cyan)';
  toast.style.color = isError ? '#fff' : '#0d131a';
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

function escapeHtml(str) {
  if (typeof str !== 'string') return str;
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}
