# 🌐 Oslo Web

### Stats Webpage & API for Oslo Discord Chess Trainer

A lightweight Flask web service that serves Oslo's public landing page and exposes a live stats API — pulling real-time data from the same PostgreSQL database as the bot.

---

## 🔗 Pages

| Route | Description |
|-------|-------------|
| `/` | Landing page — hero, live stats, features, Ko-fi support |
| `/api/stats` | Live bot statistics as JSON |
| `/tos` | Terms of Service |
| `/privacy` | Privacy Policy |

---

## 📊 Live Stats API

`GET /api/stats` returns:

```json
{
  "total_puzzles_solved": 1079,
  "total_interactions": 3237
}
```

Stats are cached for 60 seconds to avoid unnecessary database load.

---

## 🛠️ Stack

- **Flask** — lightweight Python web framework
- **asyncpg** — async PostgreSQL client
- **Gunicorn** — production WSGI server
- **PostgreSQL** — shared database with the Oslo bot

---

## 🚀 Deployment

Requires one environment variable:

```
DATABASE_URL — PostgreSQL connection string (same instance as the bot)
```

The `Procfile` handles the rest:

```
web: gunicorn api:app
```

---

## 🤝 Related

- **Oslo Bot** — [github.com/Dev-NightWing/oslo-chess-trainer](https://github.com/Dev-NightWing/oslo-chess-trainer)

---

*© 2026 Night Wing. All rights reserved.*
