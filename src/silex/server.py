from __future__ import annotations

import json
import os
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from silex.auth import parse_role, require
from silex.errors import SilexError
from silex.plant import Plant

STATIC = Path(__file__).parent / "static"
PLANT = Plant()
MAX_BODY = 16_384


def _boot_token() -> str:
    preset = os.environ.get("SILEX_CONSOLE_TOKEN")
    if preset:
        if len(preset) < 16:
            raise SilexError("SILEX_CONSOLE_TOKEN is too short")
        return preset
    return secrets.token_urlsafe(24)


TOKEN = _boot_token()

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
    "Content-Security-Policy": "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'",
}

ROUTES = {
    "/api/reset": lambda body: (PLANT.reset(bool(body.get("quality_pass", True))), PLANT.snapshot())[1],
    "/api/quality": lambda body: PLANT.set_quality(bool(body.get("pass", True))),
    "/api/propose": lambda body: PLANT.propose(str(body.get("text", ""))[:500]),
    "/api/submit": lambda body: PLANT.submit(body.get("goal"), body.get("steps")),
    "/api/issue": lambda body: PLANT.issue(body.get("actions")),
    "/api/revoke": lambda _body: PLANT.revoke(),
    "/api/tick": lambda _body: PLANT.tick(),
    "/api/run": lambda _body: PLANT.run(),
}


def _authorized(handler: BaseHTTPRequestHandler) -> bool:
    offered = handler.headers.get("X-Silex-Token", "")
    return bool(offered) and secrets.compare_digest(offered, TOKEN)


def _send(handler: BaseHTTPRequestHandler, code: int, payload: dict) -> None:
    raw = json.dumps(payload).encode()
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(raw)))
    for key, value in SECURITY_HEADERS.items():
        handler.send_header(key, value)
    handler.end_headers()
    handler.wfile.write(raw)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/state":
            if not _authorized(self):
                _send(self, 401, {"error": "missing token"})
                return
            try:
                require(path, parse_role(self.headers.get("X-Silex-Role") or "admin"))
            except SilexError as exc:
                _send(self, 403, {"error": str(exc)})
                return
            _send(self, 200, PLANT.snapshot())
            return
        if path in {"/", "/index.html"}:
            html = (STATIC / "index.html").read_text().replace("__SILEX_TOKEN__", TOKEN)
            raw = html.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            for key, value in SECURITY_HEADERS.items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(raw)
            return
        self.send_error(404)

    def do_POST(self) -> None:
        if not _authorized(self):
            _send(self, 401, {"error": "missing token"})
            return
        path = urlparse(self.path).path
        fn = ROUTES.get(path)
        if fn is None:
            self.send_error(404)
            return
        try:
            require(path, parse_role(self.headers.get("X-Silex-Role") or "admin"))
        except SilexError as exc:
            _send(self, 403, {"error": str(exc)})
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length > MAX_BODY:
            _send(self, 413, {"error": "payload too large"})
            return
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw or b"{}")
            if not isinstance(body, dict):
                raise ValueError("object required")
        except (json.JSONDecodeError, ValueError):
            _send(self, 400, {"error": "invalid json"})
            return
        try:
            _send(self, 200, fn(body))
        except SilexError as exc:
            _send(self, 400, {"error": str(exc), **PLANT.snapshot()})
        except Exception:
            _send(self, 500, {"error": "internal error"})


def serve(host: str = "127.0.0.1", port: int = 8080) -> None:
    remote = host not in {"127.0.0.1", "localhost", "::1"}
    if remote and os.environ.get("SILEX_ALLOW_REMOTE") != "1":
        raise SilexError("refusing non-local bind; set SILEX_ALLOW_REMOTE=1 to override")
    if remote and not os.environ.get("SILEX_CONSOLE_TOKEN"):
        raise SilexError("remote bind requires SILEX_CONSOLE_TOKEN")
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"Silex console  http://{host}:{port}")
    httpd.serve_forever()
