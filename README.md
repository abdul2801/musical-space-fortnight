# Soundverse 

This is a backend service built with **FastAPI** that allows users to stream audio clips and tracks the number of times each clip has been played. The system is also integrated with **Prometheus** for monitoring and **Grafana** for visualization.

---

## Features

- Stream audio clips via HTTP
- Track play counts for each audio clip
- Expose Prometheus-compatible metrics
- Visualize metrics using Grafana dashboards

---

## ⚙️ Getting Started

### 2. Start Services with Docker

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
docker-compose up --build
```

This will spin up:
- FastAPI app on `http://localhost:8000`
- Prometheus on `http://localhost:9090`
- Grafana on `http://localhost:3000`

---

## API Endpoints

| Method | Endpoint                    | Description                              |
|--------|-----------------------------|------------------------------------------|
| GET    | `/clips`                   | List all available audio clips           |
| POST   | `/clips`                   | Create a new audio clip entry            |
| GET    | `/clips/{clip_id}/stream` | Stream the audio clip                    |
| GET    | `/clips/{clip_id}/stats`  | Get play count and clip metadata         |
| GET    | `/metrics`                | Prometheus metrics export                |

---

## 📊 Monitoring

### Prometheus
- **URL:** `http://localhost:9090`

### Grafana
- **URL:** `http://localhost:3000`
- **Default credentials:** `admin` / `admin`

Add Prometheus as a data source in Grafana to start visualizing metrics.

---

