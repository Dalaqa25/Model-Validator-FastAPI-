from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import shutil

app = FastAPI()
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    size = len(contents)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size is not supprted (choose blow 10mb)")
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.jion(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)


    return {
        "filename": file.filename,
        "size_bytes": size,
        "content_type": file.content_type,
        "path": file_path
    }