from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import aiofiles
from .orchestrator import run_qa_pipeline

app = FastAPI(title="BizOps QA Agent API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class RunResponse(BaseModel):
    run_id: str
    status: str

@app.post("/api/upload")
async def upload_spec(file: UploadFile = File(...)):
    """Endpoint to upload a PDF or docx requirement spec."""
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF or docx files are supported.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
        
    return {"filename": file.filename, "message": "File uploaded successfully", "path": file_path}

@app.post("/api/run", response_model=RunResponse)
async def run_pipeline(file_path: str):
    """Trigger the multi-agent workflow."""
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found. Please upload it first.")
    
    # We will trigger the LangGraph orchestrator here
    run_id = run_qa_pipeline(file_path)
    
    return RunResponse(run_id=run_id, status="Started")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
