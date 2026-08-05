#!/usr/bin/env bash
# install.sh — Instalador Automático de Integración localProcess_Manager + Antigravity CLI (Linux)

set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SETTINGS_FILE="$HOME/.gemini/antigravity-cli/settings.json"

echo "======================================================================="
echo "🚀 Instalador Automático: localProcess_Manager ➔ Antigravity CLI (agy)"
echo "======================================================================="
echo ""

# 1. Configurar Servidor MCP en ~/.gemini/antigravity-cli/settings.json
echo "📦 1. Configurando Servidor MCP Neuronal en settings.json..."
python3 - <<EOF
import json, os

settings_path = os.path.expanduser("~/.gemini/antigravity-cli/settings.json")
base_dir = "$BASE_DIR"
mcp_script = os.path.join(base_dir, "tools", "neural_brain", "mcp_brain_server.py")

data = {}
if os.path.exists(settings_path):
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}

if "mcpServers" not in data or not isinstance(data["mcpServers"], dict):
    data["mcpServers"] = {}

data["mcpServers"]["localprocess-brain"] = {
    "command": "python3",
    "args": [mcp_script]
}

os.makedirs(os.path.dirname(settings_path), exist_ok=True)
with open(settings_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("   ✅ Servidor MCP 'localprocess-brain' registrado con éxito.")
EOF

# 2. Agregar función y alias a ~/.bashrc y ~/.zshrc
echo ""
echo "🔧 2. Configurando comandos de terminal (agy-ctx)..."
SHELL_CONFIGS=("$HOME/.bashrc" "$HOME/.zshrc")

BLOCK_START="# --- INICIO LOCALPROCESS_MANAGER AGY INTEGRATION ---"
BLOCK_END="# --- FIN LOCALPROCESS_MANAGER AGY INTEGRATION ---"

FUNCTION_BLOCK="
$BLOCK_START
function agy-context() {
    local current_folder=\"\$PWD\"
    python3 \"$BASE_DIR/tools/compilar_prompt.py\" --folder \"\$current_folder\" > /dev/null 2>&1
    agy --system-prompt \"$BASE_DIR/prompt.md\" \"\$@\"
}
alias agy-ctx='agy-context'
$BLOCK_END
"

for cfg in "${SHELL_CONFIGS[@]}"; do
    if [ -f "$cfg" ]; then
        if grep -q "LOCALPROCESS_MANAGER AGY INTEGRATION" "$cfg"; then
            # Eliminar bloque anterior para reescribir con rutas limpias
            sed -i "/$BLOCK_START/,/$BLOCK_END/d" "$cfg"
        fi
        echo "$FUNCTION_BLOCK" >> "$cfg"
        echo "   ✅ Comando 'agy-ctx' configurado en $cfg"
    fi
done

echo ""
echo "======================================================================="
echo "🎉 ¡Instalación de Integración Completada con Éxito!"
echo "======================================================================="
echo "Para activar los cambios en esta terminal ejecuta:"
echo "   source ~/.bashrc"
echo ""
echo "Desde ahora, en cualquier proyecto puedes ejecutar:"
echo "   agy-ctx"
echo "======================================================================="
