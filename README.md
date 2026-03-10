# 🚀 ISRO Mission Control — Full Stack Dashboard

> Production-grade full stack web app: Flask backend · SQLite DB · User auth · Live map · Plotly charts · Docker · GitHub Actions CI/CD

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (Frontend)                        │
│  Dashboard · Live Map (Leaflet) · Favourites · Auth Modal   │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP (fetch API)
┌───────────────────────▼─────────────────────────────────────┐
│                  FLASK BACKEND (Python)                      │
│                                                             │
│  /auth/register   /auth/login   /auth/logout  /auth/me      │
│  /api/stats       /api/spacecrafts             /api/launchers│
│  /api/customer_satellites        /api/centres               │
│  /api/analytics   /api/countries               /api/favourites│
│                                                             │
│  ┌──────────────┐   ┌─────────────────────────────┐        │
│  │  SQLite DB   │   │  ISRO External API Cache    │        │
│  │  users       │   │  (30-min TTL, fallback data)│        │
│  │  favourites  │   └─────────────────────────────┘        │
│  │  launch_cache│                                           │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
                        │
        ┌───────────────▼────────────────┐
        │   External ISRO API            │
        │   https://isro.vercel.app      │
        └────────────────────────────────┘
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 **User Auth** | Register / Login / Logout with hashed passwords |
| ⭐ **Favourites** | Save spacecraft, launchers & satellites to your profile |
| 📊 **5 Analytics Charts** | Bar, pie, scatter, cumulative — all Plotly dark-themed |
| 🗺️ **Live Map** | Leaflet map with ISRO centres, launch sites & orbital tracks |
| 🛸 **Spacecraft Explorer** | Searchable + filterable cards with full detail modal |
| 🚀 **Launcher Library** | All ISRO rockets with flight stats |
| 🛰️ **Satellite Table** | International customers with country filter |
| 🏭 **Centres** | ISRO research facilities with locations |
| 🔄 **API Caching** | 30-min SQLite cache — works offline with fallback data |
| 🐳 **Docker Ready** | One command to containerize |
| 🤖 **GitHub Actions** | CI with route tests + auth tests + Docker build |

---

## 🚀 Quick Start (VSCode — Recommended)

### Step 1 — Clone & Open

```bash
git clone https://github.com/YOUR-USERNAME/isro-dashboard.git
cd isro-dashboard
code .
```

### Step 2 — Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run

```bash
python run.py
```

Open **http://127.0.0.1:5000** 🎉

---

## 📁 Project Structure

```
isro-fullstack/
│
├── run.py                          # Entry point
├── requirements.txt
├── Dockerfile
│
├── backend/
│   ├── __init__.py                 # Flask app factory
│   ├── models/
│   │   └── __init__.py             # User, Favourite, LaunchCache models
│   ├── routes/
│   │   ├── auth.py                 # /auth/* endpoints
│   │   ├── api.py                  # /api/* endpoints
│   │   └── pages.py                # HTML page routes
│   └── utils/
│       └── isro_api.py             # ISRO API fetcher + cache + fallback
│
├── frontend/
│   ├── templates/
│   │   ├── base.html               # Shared layout, nav, auth modal
│   │   ├── index.html              # Main dashboard
│   │   ├── map.html                # Live map
│   │   └── favourites.html         # Saved items
│   └── static/                     # (CSS/JS if extracted)
│
└── .github/
    └── workflows/
        └── ci.yml                  # GitHub Actions CI/CD
```

---

## 🔌 API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | — | Create account |
| POST | `/auth/login` | — | Login |
| POST | `/auth/logout` | ✅ | Logout |
| GET  | `/auth/me` | — | Current user info |
| GET  | `/api/stats` | — | Dashboard summary counts |
| GET  | `/api/spacecrafts?q=&year=` | — | Spacecraft list (filtered) |
| GET  | `/api/launchers?q=` | — | Launchers list |
| GET  | `/api/customer_satellites?q=&country=` | — | International satellites |
| GET  | `/api/centres` | — | ISRO centres |
| GET  | `/api/analytics` | — | Chart data for all graphs |
| GET  | `/api/countries` | — | Country list for filter |
| GET  | `/api/favourites` | ✅ | Get user's favourites |
| POST | `/api/favourites` | ✅ | Add to favourites |
| DELETE | `/api/favourites/<id>` | ✅ | Remove favourite |

---

## ⚙️ GitHub Actions Pipeline

```
On every git push:
  ↓
[Job 1: test]
  → Install dependencies
  → Check app factory imports
  → Test all 9 API routes return 200
  → Test register → login → bad-login flow
  ↓ (only on main branch push)
[Job 2: build]
  → Build Docker image
  → Start container, curl health check
  ↓
[Job 3: notify]
  → Print deployment summary
```

To view: GitHub Repo → **Actions** tab.

---

## 🐳 Docker

```bash
# Build
docker build -t isro-dashboard .

# Run
docker run -p 5000:5000 isro-dashboard

# Open http://localhost:5000
```

---

## ☁️ Deploy to Cloud (Free)

### Railway (easiest)
1. Push to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Set env var: `SECRET_KEY=your-secret-here`
4. Done — Railway auto-detects Dockerfile

### Render
1. Go to [render.com](https://render.com) → New Web Service
2. Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn run:app`

---

## 🛠️ VSCode Extensions Recommended

- **Python** (Microsoft) — syntax, linting
- **Pylance** — IntelliSense
- **Thunder Client** — test your API endpoints
- **GitLens** — visualize git history
- **SQLite Viewer** — view `isro.db` visually

---

## 📝 Environment Variables

Create a `.env` file (optional):

```env
SECRET_KEY=your-super-secret-key
DATABASE_URL=sqlite:///isro.db
FLASK_ENV=development
```

---

## 🤝 Data Credits

- [ISRO Open API](https://isro.vercel.app) — spacecraft, launchers, centres
- [isrostats.in](https://isrostats.in) — statistics
- Map tiles: CARTO Dark Matter
