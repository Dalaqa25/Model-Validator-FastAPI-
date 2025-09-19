from fastapi import APIRouter, UploadFile, File, HTTPException
from app import utils
from app.validator import validate_model_zip

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

    # ვალიდაციის ლოგიკა validator.py-დან
    model_files_found = validate_model_zip(extracted_files)

    return {
        "uploaded": file.filename,
        "files_inside": extracted_files,
        "model_files_found": model_files_found
    }
