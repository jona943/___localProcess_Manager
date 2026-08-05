// utils.js — Funciones auxiliares globales del Dashboard UI

export function showToast(message, isError = false) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.innerText = message;
  toast.style.backgroundColor = isError ? 'var(--danger)' : 'var(--accent-cyan)';
  toast.style.color = isError ? '#fff' : '#0d131a';
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

export function escapeHtml(str) {
  if (typeof str !== 'string') return str;
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

export function findMatchingOption(currentVal, options) {
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

export function handleSelectChange(selectElem) {
  const group = selectElem.closest('.form-group');
  if (!group) return;
  const customInput = group.querySelector('.custom-input-other');
  if (!customInput) return;
  
  if (selectElem.value === 'Otro') {
    customInput.style.display = 'block';
    customInput.focus();
  } else {
    customInput.style.display = 'none';
  }
}

export function limpiarLocalStorage(onSuccessCallback) {
  if (confirm("¿Estás seguro de eliminar el respaldo temporal en LocalStorage?\n\n(Nota: Esto NO afectará los datos guardados en la base de datos SQLite memory.db)")) {
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith('lpm_')) {
        localStorage.removeItem(key);
      }
    });
    showToast("LocalStorage borrado correctamente");
    if (typeof onSuccessCallback === 'function') {
      onSuccessCallback();
    }
  }
}

