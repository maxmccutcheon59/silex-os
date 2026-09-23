from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from silex.errors import SilexError
from silex.plant import Plant

STATIC = Path(__file__).parent / "static"
PLANT = Plant()

ROUTES = {
    "/api/reset": lambda body: (PLANT.reset(bool(body.get("quality_pass", True))), PLANT.snapshot())[1],
    "/api/quality": lambda body: PLANT.set_quality(bool(body.get("pass", True))),
    "/api/propose": lambda body: PLANT.propose(str(body.get("text", ""))),
    "/api/submit": lambda body: PLANT.submit(body.get("goal"), body.get("steps")),
    "/api/issue": lambda body: PLANT.issue(body.get("actions")),
    "/api/revoke": lambda _body: PLANT.revoke(),
    "/api/tick": lambda _body: PLANT.tick(),
    "/api/run": lambda _body: PLANT.run(),
}


def _send(handler: BaseHTTPRequestHandler, code: int, payload: dict) -> None:
    raw = json.dumps(payload).encode()
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/state":
            _send(self, 200, PLANT.snapshot())
            return
        if path in {"/", "/index.html"}:
            self._file(STATIC / "index.html", "text/html; charset=utf-8")
            return
        self.send_error(404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        fn = ROUTES.get(path)
        if fn is None:
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        body = json.loads(self.rfile.read(length) or b"{}") if length else {}
        try:
            _send(self, 200, fn(body))
        except SilexError as exc:
            _send(self, 400, {"error": str(exc), **PLANT.snapshot()})
        except Exception as exc:
            _send(self, 500, {"error": str(exc), **PLANT.snapshot()})

    def _file(self, path: Path, content_type: str) -> None:
        raw = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def serve(host: str = "127.0.0.1", port: int = 8080) -> None:
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"Silex console  http://{host}:{port}")
    httpd.serve_forever()
