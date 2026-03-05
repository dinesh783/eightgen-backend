## Api-service

Backend service that sits in front of internal APIs and exposes them safely to external partners.  
Built with FastAPI, MySQL, and Docker, it adds **API key authentication**, **per-partner rate limiting**, and a **proxy layer** to JSONPlaceholder (simulating internal microservices).

---

### Features

- **API Gateway / Management layer**
  - Partners call this backend instead of the internal services directly.
  - Proxies requests to JSONPlaceholder (`/users`, `/posts`, `/comments`, `/todos`, `/albums`, `/photos` and `/{id}` variants).

- **Partner onboarding & API keys**
  - `POST /partners` to create a partner and issue an API key.
  - `GET /partners` to list partners (for debugging/demo).
  - API keys are stored as hashes in DB (not plaintext).
  - All proxy endpoints require `X-API-Key`.

- **Per-partner rate limiting**
  - Configurable `rate_limit_per_minute` per partner.
  - In-memory per-minute counter (simple but clear for a PoC).
  - Returns **429 Too Many Requests** when a partner exceeds their quota.

- **Request observability**
  - Stores request logs for proxy calls; view with `GET /requests`.

- **Production-ready basics**
  - Clear separation of concerns: models, schemas, database, CRUD, API.
  - Environment-based configuration (via `.env` or Docker env vars).
  - Dockerfile for containerized deployment.

---

### Tech Stack

- **Language**: Python 3.11
- **Framework**: FastAPI
- **Database**: MySQL (via SQLAlchemy Async Engine + `aiomysql`)
- **HTTP client**: httpx
- **Containerization**: Docker
- **Other**: Pydantic v2, Uvicorn

---

### Local Development

#### 1. Setup

```bash
git clone https://github.com/dinesh783/api-service.git
cd api-service

python -m venv venv
venv\Scripts\activate   # on Windows

pip install -r requirements.txt
```

Create a `.env` file (not committed to git):

```env
DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=eightgen
JSONPLACEHOLDER_BASE_URL=https://jsonplaceholder.typicode.com
API_KEY_PEPPER=your_strong_secret_pepper
```
#### 2. Run the app

```bash
uvicorn app.main:app --reload
```

- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

---

### Run with Docker

Build the image:

```bash
docker build -t Api-service .
```

Run the container (DB running on the host):

```bash
docker run -p 8001:8000 ^
  -e DB_HOST=host.docker.internal ^
  -e DB_USER=your_user ^
  -e DB_PASSWORD=your_password ^
  -e DB_NAME=eightgen ^
  -e JSONPLACEHOLDER_BASE_URL=https://jsonplaceholder.typicode.com ^
  Api-service
```

- Health: `http://127.0.0.1:8001/health`
- Docs: `http://127.0.0.1:8001/docs`

---

### Example Request and Response

Health check request:

```bash
curl -X GET http://127.0.0.1:8000/health
```

Health check response:

```json
{
  "status": "Running"
}
```

###  Example Flows

#### 1. Create a partner & get API key

- `POST /partners`

Request body:

```json
{
  "name": "test-partner",
  "rate_limit_per_minute": 5
}
```

Response:

```json
{
  "id": 1,
  "name": "test-partner",
  "rate_limit_per_minute": 5,
  "api_key": "xxxxxxxxxxxxxxxx"
}
```

#### 2. Call protected proxy endpoints

Use the returned `api_key` in the `X-API-Key` header.

- `GET /proxy/users`, `GET /proxy/users/{id}`
- `GET /proxy/posts`, `GET /proxy/posts/{id}`
- `GET /proxy/comments`, `GET /proxy/comments/{id}`
- `GET /proxy/todos`, `GET /proxy/todos/{id}`
- `GET /proxy/albums`, `GET /proxy/albums/{id}`
- `GET /proxy/photos`, `GET /proxy/photos/{id}`

Example header:

```http
X-API-Key: xxxxxxxxxxxxxxxx
```

#### 3. Rate limiting behavior

- Each partner has their own limit (`rate_limit_per_minute`).
- After N requests in the same minute, further calls return:

```json
{
  "detail": "Rate limit exceeded"
}
```

Status: **429**.

---

### Table Models

#### `partners`

| Column | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `name` | String(255) | Partner name |
| `api_key` | String(64) | Stores **hashed** API key (unique, indexed) |
| `rate_limit_per_minute` | Integer | Per-partner request limit |

#### `request_logs`

| Column | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `method` | String(10) | HTTP method |
| `endpoint` | String(255) | API endpoint path |
| `partner_id` | Integer | FK to `partners.id` (nullable) |
| `status_code` | Integer | Response status code |
| `request_payload` | Text | Optional payload summary |
| `response_summary` | Text | Optional response summary |
| `created_at` | DateTime | UTC timestamp |

---
### 📂 Project Structure

```text
app/
  api/
    deps.py        # shared API dependencies (auth)
    routes/        # route modules by domain
    router.py      # main router composition
  core/
    config.py      # settings/env configuration
  db/
    base.py        # SQLAlchemy Base
    session.py     # engine/session dependency
  models/          # SQLAlchemy models
  repositories/    # DB access layer
  services/        # business logic layer
  app.py           # app factory + startup wiring
  main.py          # ASGI entrypoint (uvicorn app.main:app)
Dockerfile         # container build instructions
requirements.txt   # Python dependencies
```

---

### What this project demonstrates

- Designing an **API Management layer** with:
  - Partner onboarding
  - API key authentication
  - Multi-tenant rate limiting
  - Backend proxying to internal services
- Clean Python/FastAPI architecture and containerization.

