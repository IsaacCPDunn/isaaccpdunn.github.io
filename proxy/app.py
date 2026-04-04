from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

MAX_BYTES = 1_000_000


def _is_public_host(hostname: str) -> bool:
    """Block localhost/private targets to reduce SSRF risk."""
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False

    for info in infos:
        ip = info[4][0]
        addr = ipaddress.ip_address(ip)
        if (
            addr.is_private
            or addr.is_loopback
            or addr.is_link_local
            or addr.is_multicast
            or addr.is_reserved
            or addr.is_unspecified
        ):
            return False

    return True


def _validate_url(raw_url: str) -> tuple[bool, str]:
    parsed = urlparse(raw_url)
    if parsed.scheme not in {"http", "https"}:
        return False, "Only http:// and https:// URLs are allowed."
    if not parsed.hostname:
        return False, "The URL must include a valid hostname."
    if not _is_public_host(parsed.hostname):
        return False, "The hostname is not allowed."
    return True, ""


@app.get("/")
def index():
    return send_from_directory(app.root_path, "index.html")


@app.get("/api/fetch")
def api_fetch():
    target_url = request.args.get("url", "").strip()
    if not target_url:
        return jsonify({"ok": False, "error": "Missing url query parameter."}), 400

    valid, msg = _validate_url(target_url)
    if not valid:
        return jsonify({"ok": False, "error": msg}), 400

    try:
        response = requests.get(
            target_url,
            timeout=10,
            allow_redirects=True,
            headers={"User-Agent": "proxy-viewer/1.0"},
            stream=True,
        )
        response.raise_for_status()

        chunks: list[bytes] = []
        total = 0
        for chunk in response.iter_content(chunk_size=8192):
            if not chunk:
                continue
            total += len(chunk)
            if total > MAX_BYTES:
                return (
                    jsonify({"ok": False, "error": "Response too large (over 1 MB)."}),
                    413,
                )
            chunks.append(chunk)

        body = b"".join(chunks)
        text = body.decode(response.encoding or "utf-8", errors="replace")

        return jsonify(
            {
                "ok": True,
                "final_url": response.url,
                "status_code": response.status_code,
                "content_type": response.headers.get("content-type", "unknown"),
                "body": text,
            }
        )
    except requests.RequestException as exc:
        return jsonify({"ok": False, "error": f"Fetch failed: {exc}"}), 502


if __name__ == "__main__":
    app.run(debug=True)
