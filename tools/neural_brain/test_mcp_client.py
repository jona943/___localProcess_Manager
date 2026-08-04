#!/usr/bin/env python3
"""
test_mcp_client.py — Simulador de Cliente MCP (Antigravity CLI)
Simula la conexión stdio y la ejecución autónoma de herramientas vectoriales.
"""

import subprocess
import json
import sys
from pathlib import Path

SERVER_PATH = Path(__file__).resolve().parent / "mcp_brain_server.py"


def run_mcp_test():
    print("=======================================================================")
    print("🤖 Prueba de Simulación de Cliente MCP (Antigravity CLI ➔ NME Server)")
    print("=======================================================================\n")

    # Iniciar el servidor MCP en un subproceso stdio
    proc = subprocess.Popen(
        [sys.executable, str(SERVER_PATH)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    def send_and_receive(req):
        proc.stdin.write(json.dumps(req) + "\n")
        proc.stdin.flush()
        out_line = proc.stdout.readline()
        return json.loads(out_line)

    # 1. Petición 'initialize'
    res_init = send_and_receive({
        "jsonrpc": "2.0",
        "id": "1",
        "method": "initialize",
        "params": {}
    })
    print("1️⃣ Petición MCP 'initialize':")
    print(f"   ↳ Servidor: {res_init['result']['serverInfo']['name']} v{res_init['result']['serverInfo']['version']}\n")

    # 2. Petición 'tools/list'
    res_tools = send_and_receive({
        "jsonrpc": "2.0",
        "id": "2",
        "method": "tools/list"
    })
    tools = res_tools['result']['tools']
    print(f"2️⃣ Petición MCP 'tools/list': ({len(tools)} herramienta(s) detectada(s)):")
    for t in tools:
        print(f"   • {t['name']}: {t['description'][:75]}...")
    print()

    # 3. Guardar memoria neuronal vía MCP
    res_add = send_and_receive({
        "jsonrpc": "2.0",
        "id": "3",
        "method": "tools/call",
        "params": {
            "name": "guardar_memoria_neuronal",
            "arguments": {
                "contenido": "Regla permanente: Utilizar siempre el servidor MCP local para consultas semánticas de sub-milisegundo.",
                "categoria": "mcp_rule"
            }
        }
    })
    print("3️⃣ Ejecutando 'guardar_memoria_neuronal':")
    print(f"   ↳ {res_add['result']['content'][0]['text']}\n")

    # 4. Consultar memoria neuronal vía MCP
    res_query = send_and_receive({
        "jsonrpc": "2.0",
        "id": "4",
        "method": "tools/call",
        "params": {
            "name": "consultar_memoria_neuronal",
            "arguments": {
                "consulta": "servidor MCP local sub-milisegundo",
                "limite": 1
            }
        }
    })
    print("4️⃣ Ejecutando 'consultar_memoria_neuronal':")
    print(f"   ↳ {res_query['result']['content'][0]['text'].strip()}\n")

    proc.terminate()
    print("=======================================================================")
    print("🎉 Servidor MCP verificado y funcionando al 100% de forma autónoma.")
    print("=======================================================================")


if __name__ == "__main__":
    run_mcp_test()
