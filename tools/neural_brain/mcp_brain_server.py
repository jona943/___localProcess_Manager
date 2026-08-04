#!/usr/bin/env python3
"""
mcp_brain_server.py — Servidor MCP (Model Context Protocol) para el Segundo Cerebro Neuronal
Conecta el Neural Memory Engine (NME) de forma transparente y autónoma con Antigravity CLI
y cualquier cliente compatible con MCP a través de comunicación stdio / JSON-RPC 2.0.
"""

import sys
import json
import logging
from pathlib import Path

# Agregar directorio neural_brain al path
BRAIN_DIR = Path(__file__).resolve().parent
sys.path.append(str(BRAIN_DIR))

from vector_store import NeuralVectorStore

# Configurar logging hacia stderr (para no interferir con stdout JSON-RPC)
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[MCP-NME] %(asctime)s - %(levelname)s - %(message)s"
)

store = NeuralVectorStore()


def send_jsonrpc_response(response: dict):
    """Envía respuesta JSON-RPC por stdout."""
    payload = json.dumps(response, ensure_ascii=False)
    sys.stdout.write(payload + "\n")
    sys.stdout.flush()


def handle_initialize(request_id: str):
    """Responde a la solicitud de inicialización del protocolo MCP."""
    send_jsonrpc_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "segundo-cerebro-nme",
                "version": "1.0.0"
            }
        }
    })


def handle_tools_list(request_id: str):
    """Devuelve la lista de herramientas disponibles en el Segundo Cerebro Neuronal."""
    tools = [
        {
          "name": "consultar_memoria_neuronal",
          "description": "Busca semánticamente en el Segundo Cerebro Neuronal (sub-milisegundo). Recupera los fragmentos de código, reglas o arquitectura más relevantes sin consumir tokens excesivos.",
          "inputSchema": {
            "type": "object",
            "properties": {
              "consulta": {
                "type": "string",
                "description": "Consulta o pregunta semántica sobre el proyecto o las reglas del desarrollador."
              },
              "limite": {
                "type": "integer",
                "description": "Número de resultados principales a recuperar (por defecto 3).",
                "default": 3
              }
            },
            "required": ["consulta"]
          }
        },
        {
          "name": "guardar_memoria_neuronal",
          "description": "Guarda e indexa un nuevo conocimiento, regla de código o aprendizaje relevante en el espacio vectorial del Segundo Cerebro.",
          "inputSchema": {
            "type": "object",
            "properties": {
              "contenido": {
                "type": "string",
                "description": "Texto o fragmento de código a recordar."
              },
              "categoria": {
                "type": "string",
                "description": "Categoría opcional (ej. arquitectura, api, regla, frontend).",
                "default": "general"
              }
            },
            "required": ["contenido"]
          }
        },
        {
          "name": "limpiar_memoria_neuronal",
          "description": "Limpia el índice vectorial del Segundo Cerebro Neuronal.",
          "inputSchema": {
            "type": "object",
            "properties": {}
          }
        }
    ]

    send_jsonrpc_response({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": tools
        }
    })


def handle_tools_call(request_id: str, params: dict):
    """Ejecuta una herramienta solicitada por el agente CLI (Antigravity)."""
    tool_name = params.get("name")
    args = params.get("arguments", {})

    try:
        if tool_name == "consultar_memoria_neuronal":
            query = args.get("consulta", "")
            top_k = int(args.get("limite", 3))
            
            resultados = store.search_similar(query, top_k=top_k)
            
            if resultados:
                texto_salida = f"🧠 Resumen Neuronal ({len(resultados)} coincidencia(s)):\n\n"
                for idx, item in enumerate(resultados, 1):
                    texto_salida += f"[{idx}] (Similitud: {item['similarity']} | {item['search_latency_ms']} ms)\n"
                    texto_salida += f"    {item['content']}\n\n"
            else:
                texto_salida = "No se encontraron memorias vectoriales relevantes."

            send_jsonrpc_response({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": texto_salida
                        }
                    ]
                }
            })

        elif tool_name == "guardar_memoria_neuronal":
            contenido = args.get("contenido", "")
            categoria = args.get("categoria", "general")
            
            if not contenido:
                raise ValueError("El contenido no puede estar vacío.")

            row_id = store.add_memory(contenido, {"categoria": categoria})
            send_jsonrpc_response({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"✅ Memoria vectorial indexada correctamente con ID #{row_id}."
                        }
                    ]
                }
            })

        elif tool_name == "limpiar_memoria_neuronal":
            store.clear_memory()
            send_jsonrpc_response({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": "🧹 Índice de memoria neuronal limpiado con éxito."
                        }
                    ]
                }
            })

        else:
            send_jsonrpc_response({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Herramienta no encontrada: {tool_name}"
                }
            })

    except Exception as e:
        logging.error(f"Error ejecutando herramienta {tool_name}: {str(e)}")
        send_jsonrpc_response({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32603,
                "message": f"Error interno: {str(e)}"
            }
        })


def main():
    """Bucle principal de escucha stdio JSON-RPC."""
    logging.info("Iniciando Servidor MCP — Segundo Cerebro Neuronal (STDIO)...")

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue

            request = json.loads(line)
            method = request.get("method")
            req_id = request.get("id")

            logging.info(f"Petición MCP recibida: {method} [ID: {req_id}]")

            if method == "initialize":
                handle_initialize(req_id)

            elif method == "notifications/initialized":
                # Notificación sin respuesta requerida
                continue

            elif method == "tools/list":
                handle_tools_list(req_id)

            elif method == "tools/call":
                handle_tools_call(req_id, request.get("params", {}))

            elif method == "ping":
                send_jsonrpc_response({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {}
                })

            else:
                if req_id is not None:
                    send_jsonrpc_response({
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32601,
                            "message": f"Método no soportado: {method}"
                        }
                    })

        except Exception as err:
            logging.error(f"Error procesando mensaje stdin: {str(err)}")


if __name__ == "__main__":
    main()
