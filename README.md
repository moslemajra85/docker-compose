# Multi-Container Flask + Redis App

A simple multi-container project that demonstrates how a Flask web application can communicate with a Redis container using Docker Compose.

## Project Purpose

This project is meant to show:

- How to run multiple services together with Docker Compose
- How containers communicate over an internal Docker network
- How to use Redis as a shared counter backend for a Python web app

When you open the app in a browser, it increments and displays a visit counter stored in Redis.

## How It Works

The app has **2 services**:

1. **`web`**: A Flask application running on port `5000`
2. **`redis`**: A Redis database used to store the `hits` counter

Flow:

1. Browser sends a request to `http://localhost:5000`
2. Flask route `/` calls `cache.incr("hits")`
3. Redis increments and returns the counter value
4. Flask renders an HTML page showing:
   - Current hit count
   - Web container hostname
   - Redis info

## Architecture

```text
Browser -> localhost:5000 -> web (Flask container) -> redis (Redis container)
```

- Both services are attached to the same Docker network: `mynetwork`
- `web` connects to Redis using `REDIS_HOST=redis` (service name)

## Files Explained

- `app.py`
  - Flask app entry point
  - Reads Redis host from `REDIS_HOST` (default: `redis`)
  - Increments `hits` key on each `/` request
  - Returns a styled HTML response

- `Dockerfile`
  - Builds the Python app image from `python:3.11-slim`
  - Installs dependencies from `requirements.txt`
  - Copies `app.py`
  - Exposes port `5000`
  - Starts app with `python app.py`

- `docker-compose.yml`
  - Defines the `web` and `redis` services
  - Builds `web` from local `Dockerfile`
  - Maps host `5000` to container `5000`
  - Sets network and dependency order (`web` depends on `redis`)

- `requirements.txt`
  - Python package dependencies:
    - `flask==3.0.0`
    - `redis==5.0.1`

## Prerequisites

- Docker
- Docker Compose (v2, usually available as `docker compose`)

## How to Run

From the project directory:

```bash
docker compose up --build
```

Then open:

- `http://localhost:5000`

To run in detached mode:

```bash
docker compose up --build -d
```

## Useful Commands

- Start services:

  ```bash
  docker compose up
  ```

- Build and start services:

  ```bash
  docker compose up --build
  ```

- View running services:

  ```bash
  docker compose ps
  ```

- View logs:

  ```bash
  docker compose logs
  ```

- Follow logs live:

  ```bash
  docker compose logs -f
  ```

- Stop services:

  ```bash
  docker compose stop
  ```

- Stop and remove containers/network:

  ```bash
  docker compose down
  ```

- Stop and remove containers/network + volumes:

  ```bash
  docker compose down -v
  ```

- Rebuild only web image:

  ```bash
  docker compose build web
  ```

- Open shell inside web container:

  ```bash
  docker compose exec web sh
  ```

- Open Redis CLI:

  ```bash
  docker compose exec redis redis-cli
  ```

## Notes

- The counter is stored in Redis under key `hits`.
- If you run `docker compose down -v`, Redis data is removed and the counter resets.
- Flask is started in debug mode in `app.py` (`debug=True`), which is fine for local development but not recommended for production.

## Quick Troubleshooting

- Port `5000` already in use:
  - Stop the process using that port, or change port mapping in `docker-compose.yml`.

- Web container cannot reach Redis:
  - Make sure both services are running: `docker compose ps`
  - Check logs: `docker compose logs web redis`

- Changes in Python code not reflected:
  - Rebuild image: `docker compose up --build`
