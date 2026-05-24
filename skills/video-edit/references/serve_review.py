"""Local review server for the video-edit pipeline.

Spawned by the agent after transcribe + corrections. Serves the transcript
editor webapp at http://localhost:<port>, pre-loaded with the project's
transcript.json + source video. Blocks until the user clicks
"Approve & Render" in the editor — at that point it writes
transcript_review.txt to the project directory and exits cleanly with
code 0. The agent's background-task notification then fires; the agent
runs apply_review.py + gen_body.py + render automatically.

Usage:
    python serve_review.py <project_dir>           # auto-pick free port + open browser
    python serve_review.py <project_dir> --port 8765 --no-browser
"""

import argparse
import json
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Editor lives at  ../transcript-editor/index.html  (relative to this script).
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
EDITOR_DIR = os.path.join(SKILL_DIR, "transcript-editor")


def find_video(project_dir):
    """Locate the source video — prefer source.mp4 > footage.mp4 > any other."""
    for name in ("source.mp4", "footage.mp4"):
        path = os.path.join(project_dir, name)
        if os.path.exists(path):
            return path
    for name in os.listdir(project_dir):
        low = name.lower()
        if low.endswith((".mp4", ".mov", ".mkv", ".webm", ".m4v")):
            return os.path.join(project_dir, name)
    return None


class ReviewHandler(BaseHTTPRequestHandler):
    project_dir = None
    transcript_path = None
    video_path = None
    approved_event = None
    server_ref = None

    def log_message(self, fmt, *args):
        # Suppress default access logging — the agent only cares about REVIEW_URL.
        return

    # ── GET ───────────────────────────────────────────────────────────────
    def do_GET(self):
        if self.path in ("/", "/editor", "/index.html"):
            self._serve_file(os.path.join(EDITOR_DIR, "index.html"), "text/html; charset=utf-8")
        elif self.path == "/api/project":
            with open(self.transcript_path, encoding="utf-8") as f:
                transcript = json.load(f)
            payload = {
                "serverMode": True,
                "projectName": os.path.basename(os.path.abspath(self.project_dir)),
                "videoUrl": "/video",
                "transcript": transcript,
            }
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/video":
            self._serve_video()
        else:
            self.send_response(404)
            self.end_headers()

    # ── POST ──────────────────────────────────────────────────────────────
    def do_POST(self):
        if self.path == "/approve":
            length = int(self.headers.get("Content-Length", 0))
            content = self.rfile.read(length).decode("utf-8", errors="replace")
            out_path = os.path.join(self.project_dir, "transcript_review.txt")
            try:
                with open(out_path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(content)
            except Exception as exc:
                self._json(500, {"ok": False, "error": str(exc)})
                return
            self._json(200, {"ok": True, "path": out_path})
            # Signal the main thread to shut the server down + exit 0.
            self.approved_event.set()
        else:
            self.send_response(404)
            self.end_headers()

    # ── helpers ───────────────────────────────────────────────────────────
    def _json(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, path, mime):
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _serve_video(self):
        size = os.path.getsize(self.video_path)
        range_header = self.headers.get("Range", "")
        ext = os.path.splitext(self.video_path)[1].lower()
        mime = {
            ".mp4": "video/mp4", ".mov": "video/quicktime", ".mkv": "video/x-matroska",
            ".webm": "video/webm", ".m4v": "video/mp4",
        }.get(ext, "application/octet-stream")

        if range_header.startswith("bytes="):
            try:
                rng = range_header[6:].split("-", 1)
                start = int(rng[0]) if rng[0] else 0
                end = int(rng[1]) if len(rng) > 1 and rng[1] else size - 1
                end = min(end, size - 1)
                length = max(end - start + 1, 0)
            except ValueError:
                self.send_response(416)
                self.end_headers()
                return
            self.send_response(206)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(length))
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            with open(self.video_path, "rb") as f:
                f.seek(start)
                remaining = length
                while remaining > 0:
                    chunk = f.read(min(64 * 1024, remaining))
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        return
                    remaining -= len(chunk)
        else:
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(size))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            with open(self.video_path, "rb") as f:
                while True:
                    chunk = f.read(64 * 1024)
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        return


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--port", type=int, default=0, help="0 = auto-pick free port")
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    project_dir = os.path.abspath(args.project_dir)
    transcript_path = os.path.join(project_dir, "transcript.json")
    if not os.path.exists(transcript_path):
        print(f"ERROR: transcript.json not found in {project_dir}", file=sys.stderr)
        sys.exit(2)

    video_path = find_video(project_dir)
    if not video_path:
        print(f"ERROR: no video file (.mp4/.mov/.mkv/.webm/.m4v) in {project_dir}", file=sys.stderr)
        sys.exit(2)

    if not os.path.exists(os.path.join(EDITOR_DIR, "index.html")):
        print(f"ERROR: editor not found at {EDITOR_DIR}/index.html", file=sys.stderr)
        sys.exit(2)

    approved_event = threading.Event()
    ReviewHandler.project_dir = project_dir
    ReviewHandler.transcript_path = transcript_path
    ReviewHandler.video_path = video_path
    ReviewHandler.approved_event = approved_event

    server = ThreadingHTTPServer(("127.0.0.1", args.port), ReviewHandler)
    port = server.server_port
    url = f"http://localhost:{port}/"

    # Machine-readable line for the agent to grep:
    print(f"REVIEW_URL={url}", flush=True)
    # Human-readable context:
    print(f"Project: {project_dir}", flush=True)
    print(f"Video:   {os.path.basename(video_path)}", flush=True)
    print(f"\n👉 Open {url} to review the transcript.", flush=True)
    print(f"   Click 'Approve & Render' when done — the agent will continue automatically.\n", flush=True)

    if not args.no_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()

    threading.Thread(target=server.serve_forever, daemon=True).start()

    try:
        approved_event.wait()
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        server.shutdown()
        server.server_close()
        sys.exit(130)

    out_path = os.path.join(project_dir, "transcript_review.txt")
    print(f"\n✓ Approved. Wrote {out_path}", flush=True)
    # Brief grace period so the response actually flushes to the browser.
    threading.Timer(0.4, lambda: (server.shutdown(), server.server_close())).start()
    threading.Event().wait(0.6)
    sys.exit(0)


if __name__ == "__main__":
    main()
