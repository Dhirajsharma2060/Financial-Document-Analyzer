# Financial Document Analyzer

## Project Overview

A robust, AI-powered system for analyzing financial documents (PDFs) using CrewAI agents.  
Features include:
- PDF upload and validation
- AI-driven financial analysis, investment recommendations, and risk assessment
- Results stored as JSON files and in a SQLite database
- Easily upgradable to PostgreSQL for production
- Ready for concurrent/multi-user scaling

---

## Features

- **Upload financial documents (PDF) via API**
- **AI-powered analysis** using CrewAI and Gemini LLM
- **Investment recommendations** and **risk assessment**
- **Results saved** as both JSON files (`outputs/`) and in a database (`app.db`)
- **Database integration** with SQLAlchemy (SQLite by default, easy to migrate to Postgres)
- **Concurrent request handling** (ASGI server, ready for scaling)
- **Extensible agent/task/tool design**

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/Dhirajsharma2060/Financial-Document-Analyzer.git
cd financial-document-analyzer-debug
```

### 2. Install Requirements

```sh
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

> **Note:**  
> This project uses Gemini as the default LLM provider, but you can use any supported LLM (such as OpenAI, Anthropic, or a local model) by updating the agent configuration and providing the appropriate API key or setup.  
>  
> For Gemini, create a `.env` file in the project root with your Gemini API key:

```
GEMINI_API_KEY=your-gemini-api-key-here
```

Get your key from [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key).

### 4. Add Sample Document (Optional)

Download Tesla's Q2 2025 update and save as `data/sample.pdf` or upload any PDF via the API.

---

## Running the Application

### Start the FastAPI Server

```sh
uvicorn main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

---

## API Usage

### Health Check

```http
GET /
```

### Analyze a Financial Document

```http
POST /analyze
Content-Type: multipart/form-data

Fields:
- file: (PDF file to upload)
- query: (Optional) Analysis query string
```

**Example using `curl`:**

```sh
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@data/sample.pdf" \
  -F "query=Analyze this financial document for investment insights"
```

**Response:**
```json
{
  "status": "success",
  "query": "...",
  "analysis": "...",
  "file_processed": "..."
}
```

---

## Output & Storage

- **JSON Output:** Each analysis is saved in `outputs/analysis_<timestamp>_<uuid>.json`
- **Database:** Results are stored in `app.db` (`analysis_results` table) with fields:
  - `id`, `timestamp`, `query`, `file_processed`, `analysis`, `result`, `file_id`, `created_at`

You can inspect the database using [DB Browser for SQLite](https://sqlitebrowser.org/).

---

## Database Schema

| Column         | Type      | Description                                  |
|----------------|-----------|----------------------------------------------|
| id             | Integer   | Primary key                                  |
| timestamp      | String    | Analysis timestamp (YYYYMMDD_HHMMSS)         |
| query          | Text      | User's analysis query                        |
| file_processed | String    | Uploaded PDF filename                        |
| analysis       | Text      | AI-generated analysis                        |
| result         | Text      | Status (e.g., "success")                     |
| file_id        | String    | Unique file/analysis UUID                    |
| created_at     | DateTime  | UTC datetime of record creation              |

---

## Scaling & Concurrency

- The app is ready for concurrent requests (ASGI server, multiple workers).
- For heavy workloads or production, consider:
  - Running with multiple Uvicorn/Gunicorn workers
  - Using Celery for background processing
  - Migrating to PostgreSQL (change `DATABASE_URL` in `db.py`)

---

## Customization & Extensibility

- **Agents:** Defined in `agents.py` (financial analyst, verifier, investment advisor, risk assessor)
- **Tasks:** Defined in `task.py`
- **Tools:** Defined in `tools.py` (PDF reader, search, etc.)
- **Database Models:** In `models.py` (easy to extend with Alembic for migrations)

---

## Troubleshooting

- **Database errors:** If you change the schema, update the database (delete `app.db` for dev, or use Alembic for migrations).
- **PDF errors:** Ensure uploaded files are valid PDFs.
- **API key errors:** Make sure your `.env` file is present and the key is correct.

---


## Acknowledgements

- [CrewAI](https://github.com/joaomdmoura/crewai)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Google Gemini API](https://ai.google.dev/gemini-api/docs/api-key)
