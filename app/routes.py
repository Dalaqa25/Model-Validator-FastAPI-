from fastapi import APIRouter, UploadFile, File, HTTPException
from app import utils

router = APIRouter()

@router.post("/model-upload")
async def model_upload(file: UploadFile = File(...)):
    # შევამოწმოთ ფაილი არის თუ არა "zip" ფორმატში:
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed")
    
    # თუ ფორმატი "zip" არის წავიკითხოთ ფაილი
    contents = await file.read()

    # ფაილისი ექსტრაქტირება მოხდა utils.py დან
    extracted_files = utils.list_zip_contents(contents)

    return {
        "uploaded": file.filename,
        "files_inside": extracted_files
    }
