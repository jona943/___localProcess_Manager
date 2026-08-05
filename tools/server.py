#!/usr/bin/env python3
"""
server.py — Servidor Web Local & Dashboard API Multi-Proyecto para localProcess_Manager (Fase 2)
Servidor HTTP ligero basado en la biblioteca estándar de Python (zero dependencies externas).
"""

import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Configuración de Rutas
TOOLS_DIR = Path(__file__).resolve().parent
BASE_DIR = TOOLS_DIR.parent
WEB_DIR = TOOLS_DIR / "web"
PROMPT_FILE = BASE_DIR / "prompt.md"

sys.path.append(str(TOOLS_DIR))

import memory_engine
import compilar_prompt


class LocalProcessHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """Silencia o simplifica los logs de la consola HTTP."""
        sys.stderr.write(f"[{self.log_date_time_string()}] {self.command} {self.path}\n")

    def send_json_response(self, data, status=200):
        """Helper para enviar respuestas JSON."""
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_text_response(self, text, mime_type="text/plain; charset=utf-8", status=200):
        """Helper para enviar texto o HTML/CSS/JS."""
        body = text.encode("utf-8") if isinstance(text, str) else text
        self.send_response(status)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def get_query_param(self, query_dict, key, default="default"):
        values = query_dict.get(key, [])
        return values[0] if values else default

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        project_name = self.get_query_param(query_params, "project", "default")

        # --- ROUTER API ---
        if path == "/api/projects":
            data = memory_engine.get_projects()
            self.send_json_response(data)

        elif path == "/api/config/developer":
            data = memory_engine.get_all_config("developer_config")
            self.send_json_response(data)

        elif path == "/api/config/project":
            data = memory_engine.get_all_config("project_config", project_name=project_name)
            self.send_json_response(data)

        elif path == "/api/learnings":
            data = memory_engine.get_learnings(project_name=project_name)
            self.send_json_response(data)

        elif path == "/api/tasks":
            data = memory_engine.get_task_logs(project_name=project_name)
            self.send_json_response(data)

        elif path == "/api/prompt":
            if PROMPT_FILE.exists():
                text = PROMPT_FILE.read_text(encoding="utf-8")
            else:
                text = "# prompt.md no compilado aún."
            self.send_text_response(text)

        # --- RECURSOS ESTÁTICOS (WEB UI MODULAR) ---
        else:
            rel_path = path.lstrip("/")
            if rel_path == "" or rel_path == "index.html":
                target = WEB_DIR / "index.html"
            else:
                target = WEB_DIR / rel_path

            if target.exists() and target.is_file():
                ext = target.suffix.lower()
                mime_map = {
                    ".html": "text/html; charset=utf-8",
                    ".css": "text/css; charset=utf-8",
                    ".js": "application/javascript; charset=utf-8",
                    ".mjs": "application/javascript; charset=utf-8",
                    ".json": "application/json; charset=utf-8",
                    ".svg": "image/svg+xml",
                    ".png": "image/png",
                    ".ico": "image/x-icon"
                }
                mime = mime_map.get(ext, "application/octet-stream")
                self.send_text_response(target.read_bytes(), mime)
            else:
                self.send_text_response("404 Not Found", status=404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            body = json.loads(post_data)
        except Exception:
            body = {}

        if path == "/api/projects":
            name = body.get("name")
            proj_path = body.get("path", "./")
            context_file = body.get("context_file", "README.md")
            if name:
                memory_engine.add_project(name, proj_path, context_file)
                self.send_json_response({"status": "ok", "project": name})
            else:
                self.send_json_response({"error": "Nombre de proyecto requerido"}, status=400)

        elif path == "/api/projects/delete":
            name = body.get("name")
            if name:
                memory_engine.delete_project(name)
                self.send_json_response({"status": "ok"})
            else:
                self.send_json_response({"error": "Nombre de proyecto requerido"}, status=400)

        elif path == "/api/config/developer":
            for k, v in body.items():
                memory_engine.set_config("developer_config", k, v)
            memory_engine.export_to_markdown()
            self.send_json_response({"status": "ok"})

        elif path == "/api/config/project":
            project_name = body.get("project_name", "default")
            config_data = body.get("config", body)
            for k, v in config_data.items():
                if k != "project_name":
                    memory_engine.set_config("project_config", k, v, project_name=project_name)
            memory_engine.export_to_markdown(project_name=project_name)
            self.send_json_response({"status": "ok"})

        elif path == "/api/learnings":
            project_name = body.get("project_name", "default")
            cat = body.get("category", "general")
            topic = body.get("topic", "Regla")
            rule = body.get("rule", "")
            importance = int(body.get("importance", 1))
            if rule:
                memory_engine.add_learning(cat, topic, rule, importance, project_name=project_name)
                memory_engine.export_to_markdown(project_name=project_name)
            self.send_json_response({"status": "ok"})

        elif path == "/api/tasks":
            project_name = body.get("project_name", "default")
            summary = body.get("task_summary", "")
            if summary:
                memory_engine.add_task_log(summary, project_name=project_name)
                memory_engine.export_to_markdown(project_name=project_name)
            self.send_json_response({"status": "ok"})

        elif path == "/api/learnings/delete":
            learning_id = body.get("id")
            project_name = body.get("project_name", "default")
            if learning_id:
                memory_engine.delete_learning(int(learning_id))
                memory_engine.export_to_markdown(project_name=project_name)
            self.send_json_response({"status": "ok"})

        elif path == "/api/tasks/delete":
            task_id = body.get("id")
            project_name = body.get("project_name", "default")
            if task_id:
                memory_engine.delete_task_log(int(task_id))
                memory_engine.export_to_markdown(project_name=project_name)
            self.send_json_response({"status": "ok"})

        elif path == "/api/compile":
            project_name = body.get("project_name", "default")
            try:
                compilar_prompt.compilar(project_name=project_name)
                self.send_json_response({"status": "ok"})
            except Exception as e:
                self.send_json_response({"error": str(e)}, status=500)

        else:
            self.send_json_response({"error": "Ruta POST no encontrada"}, status=404)


def run_server(port=8000):
    memory_engine.seed_initial_data()
    
    for try_port in range(port, port + 10):
        try:
            server_address = ("127.0.0.1", try_port)
            HTTPServer.allow_reuse_address = True
            httpd = HTTPServer(server_address, LocalProcessHandler)
            print(f"\n=======================================================")
            print(f"🚀 Dashboard Web localProcess_Manager Multi-Proyecto Activo (Fase 2)")
            print(f"🌐 Abre en tu navegador: http://localhost:{try_port}")
            print(f"=======================================================\n")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServidor detenido por el usuario.")
                httpd.server_close()
            break
        except OSError as e:
            if try_port == port + 9:
                raise e
            continue


if __name__ == "__main__":
    run_server()
