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

## Bugs Found and How They Were Fixed

### main.py

- **Unused file_path in analysis:**  
  *Bug:* The uploaded file's path was not passed to the agent/task, so the default `'data/sample.pdf'` was always used.  
  *Fix:* The uploaded file's unique path is now passed through the workflow and used by the analysis tool.

- **Function name shadowing:**  
  *Bug:* The `analyze_financial_document` function in `main.py` shadowed the imported `analyze_financial_document` from `task.py`.  
  *Fix:* Ensured unique function names and clear imports to avoid confusion.

- **No PDF parsing in workflow:**  
  *Bug:* The PDF was saved and deleted, but never actually read or parsed.  
  *Fix:* The tool now reads and parses the actual uploaded PDF using the correct file path.

- **Synchronous/async mismatch:**  
  *Bug:* Async endpoints called a synchronous `run_crew` function, risking blocking.  
  *Fix:* Ensured all I/O and analysis steps are properly async or run in a thread.

- **No error handling for file read:**  
  *Bug:* No validation for file type or PDF header.  
  *Fix:* Added checks for file extension and PDF magic header, with clear error messages.

- **Potential race condition:**  
  *Bug:* The file was deleted in a `finally` block, risking deletion before analysis completed.  
  *Fix:* File is now deleted only after all processing and saving is complete.

---

### task.py

- **Missing Import for Pdf:**  
  *Bug:* `Pdf` was referenced but not imported or defined.  
  *Fix:* Switched to using `PyPDFLoader` from `langchain_community.document_loaders`.

- **Incorrect Use of async for File I/O:**  
  *Bug:* `read_data_tool` was async but used no async I/O.  
  *Fix:* Made the function synchronous, or used `asyncio.to_thread` for sync code.

- **Incorrect Method Definition (Missing self):**  
  *Bug:* Methods were used as static but not decorated as such.  
  *Fix:* Added `@staticmethod` or used class methods properly.

- **Unused Imports:**  
  *Bug:* Unused imports cluttered the file.  
  *Fix:* Removed unused imports for clarity.

- **No Error Handling for PDF Loading:**  
  *Bug:* PDF loading could crash if the file was missing or corrupt.  
  *Fix:* Added try/except around PDF loading.

- **InvestmentTool and RiskTool Not Used:**  
  *Note:* These tools were defined but not integrated.  
  *Fix:* Left as-is for future extension or removed if not needed.

- **No Type Hints:**  
  *Improvement:* Added type hints for clarity.

- **Class Naming Convention:**  
  *Improvement:* Used standard Python class naming conventions.

---

### tools.py

- **Same issues as above for PDF import, async usage, method definition, error handling, and naming conventions.**  
  All addressed as described above.

---

## Additional Notes

- **Import Issues:**  
  There were some import errors due to missing or incorrect imports (such as missing PDF loader imports and incorrect usage of tool classes). These have been fixed by ensuring all necessary libraries and classes are properly imported and referenced throughout the codebase.

- **Library Version Issues:**  
  Some libraries had version incompatibilities or were missing from `requirements.txt`. These issues were resolved by updating the `requirements.txt` file and ensuring all required packages (with compatible versions) are installed.

---

## Live Demo
Try the deployed app here: https://financial-document-analyzer-1-qb10.onrender.com/
