import os
import time
import urllib.parse
import ssl
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")
_cache = {"data": None, "ts": 0}
DATABASE_URL = os.getenv("DATABASE_URL")


def fetch_stats():
    import pg8000.native
    p = urllib.parse.urlparse(DATABASE_URL)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = pg8000.native.Connection(
        host=p.hostname,
        port=p.port or 5432,
        database=p.path.lstrip("/"),
        user=p.username,
        password=p.password,
        ssl_context=ctx
    )
    rows = conn.run("SELECT total_puzzles_solved, total_interactions FROM bot_stats WHERE id = 1")
    conn.close()
    if rows:
        return {"total_puzzles_solved": rows[0][0], "total_interactions": rows[0][1]}
    return {}


@app.route("/api/stats")
def stats():
    now = time.time()
    if _cache["data"] is None or now - _cache["ts"] > 60:
        try:
            _cache["data"] = fetch_stats()
            _cache["ts"] = now
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify(_cache["data"])


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/tos")
def tos():
    return send_from_directory(".", "tos.html")


@app.route("/privacy")
def privacy():
    return send_from_directory(".", "privacy.html")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
