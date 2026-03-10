# 🚀 ISRO Mission Control Dashboard


![ISRO Dashboard](https://img.shields.io/badge/ISRO-Mission%20Control-blueviolet?style=for-the-badge&logo=rocket&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Charts-orange?style=for-the-badge&logo=plotly&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A full-stack, real-time web dashboard tracking every spacecraft, satellite, rocket and mission ever launched by the Indian Space Research Organisation — from Aryabhata (1975) to Aditya-L1 (2023).**



---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [Pages & Sections](#-pages--sections)
- [Database Models](#-database-models)
- [GitHub Actions CI/CD](#-github-actions-cicd)
- [Docker Deployment](#-docker-deployment)
- [Cloud Deployment](#-cloud-deployment)
- [Data Sources](#-data-sources)
- [Author](#-author)
- [License](#-license)

---

## 🌌 About the Project

India's space programme is one of the most remarkable achievements in modern science. From launching **Aryabhata** in 1975 on a borrowed Soviet rocket, to landing on the **lunar south pole** in 2023 — ISRO has consistently achieved the extraordinary on a budget that rivals no major space agency.

This project was built to make all of that data **accessible, searchable, and beautiful**.

The **ISRO Mission Control Dashboard** is a production-grade full-stack web application that:

- Fetches live data from the **ISRO Open API** and caches it in SQLite
- Displays spacecraft, launchers, customer satellites, and ISRO research centres
- Visualises trends with **5 interactive Plotly.js charts**
- Shows ISRO's global footprint on a **live Leaflet.js map** with orbital overlays
- Supports **user authentication** (register/login) and a personal **Favourites** system
- Ships with **Docker** and a full **GitHub Actions CI/CD pipeline**

> Built with Python (Flask), vanilla JavaScript, and a deep love for space. 🛸

---

## ✨ Features

### 🌠 Cosmic Landing Page
- 240 animated twinkling stars with random durations
- 3 rotating orbital rings with glowing satellite dots
- Purple / black / deep-blue animated nebula clouds
- Scroll-reveal animations on every section
- Live animated stat counters
- ISRO milestones timeline (1975 → 2023)
- Cosmos info cards: Earth, LEO, GEO, Moon, Mars, Sun-L1

### 🛸 Spacecraft Explorer
- Complete catalogue of every ISRO spacecraft ever launched
- Live search by name or launch vehicle
- Filter by launch year (auto-populated dropdown)
- Full detail modal on card click
- Save to Favourites with one click (⭐)

### 🚀 Launcher Library
- Full profiles for all 6 rocket families: SLV · ASLV · PSLV · GSLV Mk I · GSLV Mk II · LVM3 · SSLV
- Shows flight count, thrust (kN), stages, current status
- Operational vs Retired badges

### 🛰️ Customer Satellites Table
- International satellites launched by ISRO for 30+ countries
- Filter by country, search by satellite name
- Columns: Name · Country · Launch Date · Vehicle · Orbit

### 🗺️ Live Orbital Map
- Leaflet.js map with dark CartoDB tiles
- All ISRO centres plotted with custom markers
- Both launch sites (SHAR Sriharikota + Thumba)
- Orbital track overlays: LEO · GEO · SSO · Inclined
- Simulated real-time satellite dot on LEO track
- Layer toggle controls (centres / sites / orbits)

### 📊 Analytics Charts (5 Plotly Charts)
1. **Launches by Year** — bar chart, colour-scaled
2. **Launcher Flights** — horizontal bar comparing all rocket families
3. **Customer Satellites by Country** — top 10 nations
4. **Mission Type Breakdown** — donut (Earth Obs / Comms / Nav / Science / Tech Demo)
5. **Cumulative Launches** — line chart with area fill

### 🔐 User Authentication
- Register with username + email + password (min 6 chars)
- Login with username OR email
- Passwords hashed with Werkzeug PBKDF2
- Session management via Flask-Login
- Duplicate username/email protection

### ⭐ Personal Favourites
- Save any spacecraft, launcher, or satellite
- Persists in SQLite across server restarts
- Filter by item type · Remove any item
- Shows save timestamp for each item

### 🏭 ISRO Centres
- Cards for all 8 major research facilities
- Full name, location, description for each

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python 3.11 + Flask 3.0 | Web server & REST API |
| Database | SQLite + SQLAlchemy 2.0 | Users, favourites, API cache |
| Auth | Flask-Login + Werkzeug | Sessions & password hashing |
| Frontend | Vanilla HTML5 + CSS3 + JS | UI without framework overhead |
| Charts | Plotly.js 2.26 | Interactive analytics |
| Maps | Leaflet.js 1.9 | Live orbital map |
| Fonts | Orbitron · Share Tech Mono · Syne | Cosmic aesthetic |
| API | isro.vercel.app | Live spacecraft & launch data |
| Caching | SQLite LaunchCache (30-min TTL) | Offline fallback + speed |
| CI/CD | GitHub Actions | Automated testing & deployment |
| Container | Docker + Gunicorn | Production deployment |

---

## 📁 Project Structure

```
isro-mission-control/
│
├── run.py                      # App entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container config
│
├── backend/
│   ├── __init__.py             # Flask app factory (create_app)
│   ├── models/
│   │   └── __init__.py         # User, Favourite, LaunchCache models
│   ├── routes/
│   │   ├── auth.py             # /auth/* endpoints
│   │   ├── api.py              # /api/* endpoints
│   │   └── pages.py            # HTML page routes
│   └── utils/
│       └── isro_api.py         # API fetcher + cache + fallback data
│
├── frontend/
│   └── templates/
│       ├── base.html           # Shared nav, auth modal, toast
│       ├── landing.html        # Cosmic home page
│       ├── index.html          # Main dashboard
│       ├── map.html            # Live Leaflet map
│       └── favourites.html     # Saved items page
│
└── .github/
    └── workflows/
        └── ci.yml              # GitHub Actions pipeline
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ → [python.org](https://www.python.org/downloads/)
- Git → [git-scm.com](https://git-scm.com/)
- VSCode (recommended) → [code.visualstudio.com](https://code.visualstudio.com/)

### Installation

```bash
# 1. Clone
git clone https://github.com/YOUR-USERNAME/isro-dashboard.git
cd isro-dashboard

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
python run.py
```

Open **http://127.0.0.1:5000** in your browser.

The SQLite database (`instance/isro.db`) is created automatically on first run.

---

## 🔌 API Endpoints

### Public

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/stats` | Summary counts |
| GET | `/api/spacecrafts?q=&year=` | Spacecraft list (searchable) |
| GET | `/api/launchers?q=` | Launch vehicles |
| GET | `/api/customer_satellites?q=&country=` | International satellites |
| GET | `/api/centres` | ISRO centres with coordinates |
| GET | `/api/analytics` | Aggregated chart data |
| GET | `/api/countries` | Country list for filters |

### Auth

| Method | Endpoint | Body |
|---|---|---|
| POST | `/auth/register` | `{ username, email, password }` |
| POST | `/auth/login` | `{ identifier, password }` |
| POST | `/auth/logout` | — |
| GET | `/auth/me` | Returns current user or null |

### Favourites (Login Required)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/favourites` | Get all saved items |
| POST | `/api/favourites` | Save an item |
| DELETE | `/api/favourites/<id>` | Remove an item |

---

## 📄 Pages & Sections

| URL | Page | Description |
|---|---|---|
| `/` | Landing | Cosmic home — stars, features, cosmos info, author |
| `/dashboard` | Dashboard | Spacecraft / Launchers / Satellites / Analytics |
| `/map` | Live Map | Leaflet map with orbital tracks |
| `/favourites` | Saved | Personal bookmarked missions |

---

## 🗄️ Database Models

### User
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | Auto-increment |
| username | String(80) | Unique |
| email | String(120) | Unique |
| password_hash | String(256) | PBKDF2 hashed |
| created_at | DateTime | UTC |

### Favourite
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | Auto-increment |
| user_id | FK → User | Owner |
| item_type | String(50) | spacecraft / launcher / satellite |
| item_name | String(200) | Display name |
| item_data | Text (JSON) | Full item blob |
| saved_at | DateTime | UTC |

### LaunchCache
| Column | Type | Notes |
|---|---|---|
| endpoint | String(200) | Unique API key |
| data | Text (JSON) | Cached response |
| fetched_at | DateTime | TTL = 30 minutes |

---

## ⚙️ GitHub Actions CI/CD

```
git push to main
      ↓
[Job 1: test]
  Install Python 3.11
  Test app factory imports
  Test all 9 API routes → HTTP 200
  Test register → login → bad login rejection
      ↓
[Job 2: build]  (main branch only)
  Build Docker image
  Start container + curl health check
      ↓
[Job 3: notify]
  Print deployment-ready summary
```

---

## 🐳 Docker Deployment

```bash
# Build
docker build -t isro-dashboard .

# Run
docker run -p 5000:5000 -e SECRET_KEY=your-secret isro-dashboard

# Open http://localhost:5000
```

---

## ☁️ Cloud Deployment (Free)

### Railway (Easiest)
1. Push to GitHub
2. [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add env var: `SECRET_KEY=your-secret`
4. Done — Railway auto-detects the Dockerfile ✅

### Render
1. [render.com](https://render.com) → New Web Service → Connect GitHub repo
2. Build: `pip install -r requirements.txt`
3. Start: `gunicorn run:app`
4. Add env var: `SECRET_KEY=your-secret`

---

## 🌐 Data Sources

| Source | URL | Data |
|---|---|---|
| ISRO Open API | [isro.vercel.app](https://isro.vercel.app) | Spacecraft, Launchers, Centres |
| ISRO Stats | [isrostats.in](https://isrostats.in) | Launch statistics |
| CartoDB | [carto.com](https://carto.com) | Dark map tiles |

> API responses are cached for 30 minutes. If the API is unreachable, the dashboard falls back to built-in sample data — it always works.

---

## 👨‍💻 Author

### Anjum A Khan

> *Developer · Space Enthusiast · Python Developer*

A passionate developer who built this dashboard to make India's extraordinary space programme more accessible and explorable for everyone. Combining a love for Python, data engineering, and the cosmos — this project tracks every rocket, satellite and mission ISRO has ever launched.

![Python](https://img.shields.io/badge/Python-Expert-3776AB?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=flat-square&logo=flask)
![Space](https://img.shields.io/badge/Space_Tech-Enthusiast-blueviolet?style=flat-square)
![ISRO](https://img.shields.io/badge/ISRO-Fan-orange?style=flat-square)

---

## 🙏 Acknowledgements

- [ISRO](https://www.isro.gov.in) — 50 years of extraordinary space exploration
- [isro.vercel.app](https://isro.vercel.app) — Open API for ISRO data
- [Plotly.js](https://plotly.com/javascript/) — Interactive chart library
- [Leaflet.js](https://leafletjs.com/) — Open-source maps
- [CartoDB](https://carto.com/) — Dark map tiles
- [Flask](https://flask.palletsprojects.com/) — Lightweight Python web framework

---

## 📄 License

MIT License — Copyright (c) 2024 **Anjum A Khan**

Free to use, modify, and distribute.

---


**Made with Passion, by Anjum A Khan**

*"Space is not just the final frontier — it is the infinite canvas of human potential."*

⭐ **Star this repo if you found it useful!**

</div>
