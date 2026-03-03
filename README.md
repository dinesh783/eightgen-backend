## Api-service

Backend service that sits in front of internal APIs and exposes them safely to external partners.  
Built with FastAPI, MySQL, and Docker, it adds **API key authentication**, **per-partner rate limiting**, and a **proxy layer** to JSONPlaceholder (simulating internal microservices).

---

### 🚀 Features

- **API Gateway / Management layer**
  - Partners call this backend instead of the internal services directly.
  - Proxies requests to JSONPlaceholder (`/users`, `/users/{id}`) as example internal services.

- **Partner onboarding & API keys**
  - `POST /partners` to create a partner and issue an API key.
  - `GET /partners` to list partners (for debugging/demo).
  - All proxy endpoints require `X-API-Key`.

- **Per-partner rate limiting**
  - Configurable `rate_limit_per_minute` per partner.
  - In-memory per-minute counter (simple but clear for a PoC).
  - Returns **429 Too Many Requests** when a partner exceeds their quota.

- **Chat + AI history (extra feature)**
  - `POST /chat` endpoint calling an AI service (mock/OpenAI-ready).
  - Stores user messages and AI responses into MySQL.

- **Production-ready basics**
  - Clear separation of concerns: models, schemas, database, CRUD, API.
  - Environment-based configuration (via `.env` or Docker env vars).
  - Dockerfile for containerized deployment.

---

### 🛠 Tech Stack

- **Language**: Python 3.11
- **Framework**: FastAPI
- **Database**: MySQL (via SQLAlchemy)
- **HTTP client**: httpx
- **Containerization**: Docker
- **Other**: Pydantic v2, Uvicorn

---

### 🔧 Local Development

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
```
#### 2. Run the app

```bash
uvicorn app.main:app --reload
```

- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

---

### 🐳 Run with Docker

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

Chat request:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Hello\"}"
```

Chat response:

```json
{
  "response": "..."
}
```

### 📡 Example Flows

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

- `GET /proxy/users` → proxies to `https://jsonplaceholder.typicode.com/users`
- `GET /proxy/users/{user_id}` → proxies to `.../users/{id}`

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

### 📂 Project Structure

```text
app/
  ai_service.py    # AI response provider (mock/OpenAI-ready)
  config.py        # configuration helpers (if needed)
  crud.py          # DB operations (e.g. save chat)
  database.py      # SQLAlchemy engine/session
  main.py          # FastAPI application + routes
  models.py        # SQLAlchemy models (ChatHistory, Partner)
  schemas.py       # Pydantic schemas (ChatRequest, PartnerCreate, PartnerOut)
Dockerfile         # container build instructions
requirements.txt   # Python dependencies
```

---

### 💡 What this project demonstrates

- Designing an **API Management layer** with:
  - Partner onboarding
  - API key authentication
  - Multi-tenant rate limiting
  - Backend proxying to internal services
- Clean Python/FastAPI architecture and containerization.
