"""Loopback-only HTTP interface for independent blank-form gold annotation."""

from __future__ import annotations

import argparse
import json
import secrets
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from annotation.gold import AnnotationError, GoldWorkspace
from pipeline.fulltext import FullTextError

STATIC = Path(__file__).parent / "static"
FILES = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"),
         "/style.css": ("style.css", "text/css")}


class Handler(BaseHTTPRequestHandler):
    server: "GoldServer"

    def respond(self, status: int, data: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)

    def json(self, status: int, data: object) -> None:
        self.respond(status, json.dumps(data, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def route(self) -> tuple[str | None, str | None]:
        parts = urlsplit(self.path)
        if parts.query or parts.fragment:
            return None, None
        path = unquote(parts.path)
        segments = path.split("/")
        if len(segments) == 4 and segments[:3] == ["", "api", "article"]:
            return segments[3], "article"
        if len(segments) == 5 and segments[:3] == ["", "api", "article"] and segments[4] == "pdf":
            return segments[3], "pdf"
        return None, None

    def trusted_host(self) -> bool:
        return self.headers.get("Host") == f"127.0.0.1:{self.server.server_port}"

    def do_GET(self) -> None:
        if not self.trusted_host():
            self.json(403, {"error": "Open this site at its 127.0.0.1 address"})
            return
        try:
            key, kind = self.route()
            if key is not None and kind == "article":
                self.json(200, self.server.workspace.article(key))
            elif key is not None and kind == "pdf":
                pdf = self.server.workspace.pdfs.get(key)
                if pdf is None:
                    raise AnnotationError("Unknown held-out article")
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Length", str(pdf.stat().st_size))
                self.send_header("Content-Disposition", "inline")
                self.send_header("Cache-Control", "no-store")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.end_headers()
                with pdf.open("rb") as handle:
                    import shutil
                    shutil.copyfileobj(handle, self.wfile)
            elif self.path == "/api/articles":
                self.json(200, {"reviewer_id": self.server.workspace.reviewer,
                                "articles": self.server.workspace.articles(), "token": self.server.token})
            elif self.path in FILES:
                name, mime = FILES[self.path]
                self.respond(200, (STATIC / name).read_bytes(), mime + "; charset=utf-8")
            else:
                self.json(404, {"error": "Not found"})
        except AnnotationError as error:
            self.json(404, {"error": str(error)})

    def do_POST(self) -> None:
        self.change()

    def do_PUT(self) -> None:
        self.change()

    def change(self) -> None:
        if not self.trusted_host() or self.headers.get("Origin") != f"http://127.0.0.1:{self.server.server_port}" or self.headers.get("X-Annotation-Token") != self.server.token:
            self.json(403, {"error": "Invalid local request"})
            return
        key, kind = self.route()
        if kind != "article" or key is None or self.command not in {"PUT", "POST"}:
            self.json(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length < 2_000_000:
                raise AnnotationError("Invalid annotation size")
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict) or set(body) != ({"revision", "annotation"} if self.command == "PUT" else {"revision", "action"}):
                raise AnnotationError("Invalid request shape")
            session = self.server.workspace.update(key, body["revision"],
                                                    annotation=body.get("annotation"), action=body.get("action"))
            self.json(200, session)
        except (ValueError, TypeError, json.JSONDecodeError, AnnotationError) as error:
            status = 409 if "Revision conflict" in str(error) else 400
            self.json(status, {"error": str(error)})


class GoldServer(ThreadingHTTPServer):
    def __init__(self, workspace: GoldWorkspace, port: int):
        self.workspace = workspace
        self.token = secrets.token_urlsafe(32)
        super().__init__(("127.0.0.1", port), Handler)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--prepared-dir", required=True, type=Path, help="Directory with <corpus-id>/document.md and preparation sidecars")
    parser.add_argument("--output-dir", required=True, type=Path, help="Local reviewer-isolated JSON drafts (keep private)")
    parser.add_argument("--reviewer", required=True, help="Independent reviewer ID; use a separate process for each reviewer")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    try:
        workspace = GoldWorkspace(args.manifest, args.prepared_dir, args.output_dir, args.reviewer)
        with GoldServer(workspace, args.port) as server:
            print(f"Gold annotation for {args.reviewer}: http://127.0.0.1:{server.server_port}/")
            server.serve_forever()
    except (AnnotationError, FullTextError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
