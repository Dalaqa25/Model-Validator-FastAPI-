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
    model_frameworks = validate_model_zip(extracted_files)
    unique_frameworks = list(set(model_frameworks.values()))

    return {
        "uploaded": file.filename,
        "frameworks": unique_frameworks
    }
