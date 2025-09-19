from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import json
from datetime import datetime

from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document
from db import engine, SessionLocal
from models import Base, AnalysisResult

app = FastAPI(title="Financial Document Analyzer")

# Create the database tables
Base.metadata.create_all(bind=engine)

async def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew asynchronously using kickoff_async"""
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document],
        process=Process.sequential,
    )
    result = await financial_crew.kickoff_async({
        'query': query, 
        'file_path': file_path  # This ensures the file path reaches the task
    })
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""

    data_dir = "data"
    file_id = str(uuid.uuid4())
    file_path = os.path.join(data_dir, f"financial_document_{file_id}.pdf")

    try:
        # Ensure data directory exists
        if not os.path.exists(data_dir):
            try:
                os.makedirs(data_dir, exist_ok=True)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error creating data directory: {str(e)}")
        if not os.access(data_dir, os.W_OK):
            raise HTTPException(status_code=500, detail=f"Data directory is not writable: {data_dir}")

        # Validate the uploaded file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are supported.")

        # Read a small chunk to validate it's a PDF
        header = await file.read(5)
        if header != b"%PDF-":
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid PDF.")

        rest = await file.read()  # read the rest of the file
        content = header + rest  # combine header and rest

        # Save uploaded file
        with open(file_path, "wb") as f:
            f.write(content)

        # Validate query
        if not query:
            query = "Analyze this financial document for investment insights"

        # Process the financial document with all analysts
        response = await run_crew(query=query.strip(), file_path=file_path)

        # Save output to outputs folder
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Create output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_dir}/analysis_{timestamp}_{file_id}.json"
        
        # Set result status
        result_status = "success"

        # Save analysis results
        output_data = {
            "timestamp": timestamp,
            "query": query,
            "file_processed": file.filename,
            "analysis": str(response),
            "file_id": file_id,
            "result": result_status
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        # Save analysis result to database only if success
        if result_status == "success":
            db = SessionLocal()
            try:
                db_result = AnalysisResult(
                    timestamp=timestamp,
                    query=query,
                    file_processed=file.filename,
                    analysis=str(response),
                    file_id=file_id,
                    result=result_status
                )
                db.add(db_result)
                db.commit()
            finally:
                db.close()

        # Clean up uploaded file after processing is complete
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # Ignore cleanup error

        return {
            "status": result_status,
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }

    except Exception as e:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # Ignore cleanup error
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)