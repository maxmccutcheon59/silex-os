from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from silex.plant import Plant

STATIC = Path(__file__).parent / "static"
PLANT = Plant()


def _json(handler: BaseHTTPRequestHandler, code: int, payload: dict) -> None:
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
            _json(self, 200, PLANT.snapshot())
            return
        if path in {"/", "/index.html"}:
            self._file(STATIC / "index.html", "text/html; charset=utf-8")
            return
        self.send_error(404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", "0") or 0)
        body = json.loads(self.rfile.read(length) or b"{}") if length else {}
        try:
            if path == "/api/reset":
                PLANT.reset(quality_pass=bool(body.get("quality_pass", True)))
                _json(self, 200, PLANT.snapshot())
                return
            if path == "/api/quality":
                _json(self, 200, PLANT.set_quality(bool(body.get("pass", True))))
                return
            if path == "/api/propose":
                _json(self, 200, PLANT.propose(str(body.get("text", ""))))
                return
            if path == "/api/submit":
                _json(self, 200, PLANT.submit(body.get("goal"), body.get("steps")))
                return
            if path == "/api/issue":
                _json(self, 200, PLANT.issue(body.get("actions")))
                return
            if path == "/api/revoke":
                _json(self, 200, PLANT.revoke())
                return
            if path == "/api/tick":
                _json(self, 200, PLANT.tick())
                return
            if path == "/api/run":
                _json(self, 200, PLANT.run())
                return
        except Exception as exc:
            _json(self, 400, {"error": str(exc), **PLANT.snapshot()})
            return
        self.send_error(404)

    def _file(self, path: Path, content_type: str) -> None:
        raw = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def serve(host: str = "127.0.0.1", port: int = 8080) -> None:
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"silex console http://{host}:{port}")
    httpd.serve_forever()
