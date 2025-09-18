from fastapi import FastAPI, UploadFile, File, HTTPException
import os, zipfile, tempfile

app = FastAPI()

@app.post("/model-upload")
async def model_upload(file: UploadFile = File(...)):
    # 1. Check extension
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed")

    # 2. Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    extracted_files = []
    extract_dir = tempfile.mkdtemp()

    # 3. Unzip
    with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        extracted_files = zip_ref.namelist()

    # 4. Clean up uploaded zip (optional, keep extracted dir for validation)
    os.remove(tmp_path)

    return {
        "uploaded": file.filename,
        "extracted_to": extract_dir,
        "files_inside": extracted_files
    }