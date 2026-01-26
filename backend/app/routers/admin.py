from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends
from app.ingest import process_psgc_file
import os
import shutil

router = APIRouter()

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "secret")

def verify_admin(secret: str):
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/upload-psgc")
async def upload_psgc(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    secret: str = Depends(verify_admin)
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload Excel.")
        
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Trigger background processing
    background_tasks.add_task(process_psgc_with_cleanup, temp_file)
    
    return {"status": "Ingestion started", "message": "The file is being processed in the background."}

async def process_psgc_with_cleanup(file_path: str):
    try:
        await process_psgc_file(file_path)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
