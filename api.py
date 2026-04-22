"""
api.py — Oslo Stats Webpage Server
Serves the static webpage and a /api/stats endpoint
that pulls live data from the same PostgreSQL DB as the bot.

Deploy separately on Railway as a Web service.
Required env vars: DATABASE_URL
"""

import asyncpg
import asyncio
import os
import time
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")
DATABASE_URL = os.getenv("DATABASE_URL")

# Cache stats for 60 seconds — avoid hammering the DB on every request
_cache = {"data": None, "ts": 0}


def fetch_stats_sync():
    """Run async DB fetch in a fresh event loop — safe with Gunicorn."""
    async def _fetch():
        conn = await asyncpg.connect(DATABASE_URL)
        row  = await conn.fetchrow("SELECT * FROM bot_stats WHERE id = 1")
        await conn.close()
        return dict(row) if row else {}
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(_fetch())
    finally:
        loop.close()


@app.route("/api/stats")
def stats():
    now = time.time()
    if _cache["data"] is None or now - _cache["ts"] > 60:
        try:
            _cache["data"] = fetch_stats_sync()
            _cache["ts"]   = now
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
